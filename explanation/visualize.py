# visualization module that creates an attention visualization using BERTViz

# external imports
from bertviz import head_view
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# internal imports
from utils import formatting as fmt


# plotting function that plots the attention values in a heatmap
def chat_explained(model, prompt):

    model.set_config()

    # get encoded input and output vectors
    encoder_input_ids = model.TOKENIZER(
        prompt, return_tensors="pt", add_special_tokens=True
    ).input_ids
    decoder_input_ids = model.MODEL.generate(encoder_input_ids, output_attentions=True)
    encoder_text = fmt.format_tokens(
        model.TOKENIZER.convert_ids_to_tokens(encoder_input_ids[0])
    )
    decoder_text = fmt.format_tokens(
        model.TOKENIZER.convert_ids_to_tokens(decoder_input_ids[0])
    )

    # get attention values for the input and output vectors
    attention_output = model.MODEL(
        input_ids=encoder_input_ids,
        decoder_input_ids=decoder_input_ids,
        output_attentions=True,
    )

    # create the response text, graphic and plot
    response_text = fmt.format_output_text(decoder_text)
    graphic = create_graphic(attention_output, (encoder_text, decoder_text))
    plot = create_plot(attention_output, (encoder_text, decoder_text))
    return response_text, graphic, plot


# creating a html graphic using BERTViz
def create_graphic(attention_output, enc_dec_texts: tuple):

    # calls the head_view function of BERTViz to return html graphic
    hview = head_view(
        encoder_attention=attention_output.encoder_attentions,
        decoder_attention=attention_output.decoder_attentions,
        cross_attention=attention_output.cross_attentions,
        encoder_tokens=enc_dec_texts[0],
        decoder_tokens=enc_dec_texts[1],
        html_action="return",
    )

    return str(hview.data)


# creating an attention heatmap plot using matplotlib/seaborn
# CREDIT: adopted from official Matplotlib documentation
## see https://matplotlib.org/stable/
def create_plot(attention_output, enc_dec_texts: tuple):
    # get the averaged attention weights
    attention = attention_output.cross_attentions[0][0].detach().numpy()
    averaged_attention_weights = np.mean(attention, axis=0)
    averaged_attention_weights = np.transpose(averaged_attention_weights)

    # get the encoder and decoder tokens in text form
    encoder_tokens = enc_dec_texts[0]
    decoder_tokens = enc_dec_texts[1]

    # set seaborn style to dark and initialize figure and axis
    sns.set(style="white")
    fig, ax = plt.subplots()

    # Setting figure size
    fig.set_size_inches(
        max(averaged_attention_weights.shape[1] * 2, 10),
        max(averaged_attention_weights.shape[0] * 1, 5),
    )

    # Plotting the heatmap with seaborn's color palette
    im = ax.imshow(
        averaged_attention_weights,
        vmax=averaged_attention_weights.max(),
        vmin=-averaged_attention_weights.min(),
        cmap=sns.color_palette("rocket", as_cmap=True),
        aspect="auto",
    )

    # Creating colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Attention Weight Scale", rotation=-90, va="bottom")
    cbar.ax.yaxis.set_tick_params(color="black")
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="black")

    # Setting ticks and labels with black color for visibility
    ax.set_yticks(np.arange(len(encoder_tokens)), labels=encoder_tokens)
    ax.set_xticks(np.arange(len(decoder_tokens)), labels=decoder_tokens)
    ax.set_title("Attention Weights by Token")
    plt.setp(ax.get_xticklabels(), color="black", rotation=45, ha="right")
    plt.setp(ax.get_yticklabels(), color="black")

    # Adding text annotations with appropriate contrast
    for i in range(averaged_attention_weights.shape[0]):
        for j in range(averaged_attention_weights.shape[1]):
            val = averaged_attention_weights[i, j]
            color = (
                "white"
                if im.norm(averaged_attention_weights.max()) / 2 > im.norm(val)
                else "black"
            )
            ax.text(j, i, f"{val:.4f}", ha="center", va="center", color=color)

    # return the plot
    return plt
