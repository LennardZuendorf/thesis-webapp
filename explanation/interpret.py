# interpret module that implements the interpretability method
# external imports
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from shap import models, maskers, plots, PartitionExplainer
import torch

# internal imports
from utils import formatting as fmt

# global variables
TEACHER_FORCING = None
TEXT_MASKER = None


# main explain function that returns a chat with explanations
def chat_explained(model, prompt):
    model.set_config()

    # create the shap explainer
    shap_explainer = PartitionExplainer(model.MODEL, model.TOKENIZER)
    # get the shap values for the prompt
    shap_values = shap_explainer([prompt])

    # create the explanation graphic and plot
    graphic = create_graphic(shap_values)
    plot = create_plot(shap_values)

    # create the response text
    response_text = fmt.format_output_text(shap_values.output_names)
    return response_text, graphic, plot


def wrap_shap(model):
    global TEXT_MASKER, TEACHER_FORCING

    # set the device to cuda if gpu is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # updating the model settings again
    model.set_config()

    # (re)initialize the shap models and masker
    text_generation = models.TextGeneration(model.MODEL, model.TOKENIZER)
    TEACHER_FORCING = models.TeacherForcing(
        text_generation,
        model.TOKENIZER,
        device=str(device),
        similarity_model=model.MODEL,
        similarity_tokenizer=model.TOKENIZER,
    )
    TEXT_MASKER = maskers.Text(model.TOKENIZER, " ", collapse_mask_token=True)


# graphic plotting function that creates a html graphic (as string) for the explanation
def create_graphic(shap_values):
    # create the html graphic using shap text plot function
    graphic_html = plots.text(shap_values, display=False)

    # return the html graphic as string
    return str(graphic_html)


# plotting function that creates a heatmap style explanation plot
def create_plot(shap_values):
    values = shap_values.values[0]
    output_names = shap_values.output_names
    input_names = shap_values.data[0]

    # Transpose the values for horizontal input names
    transposed_values = np.transpose(values)

    # Set seaborn style to dark
    sns.set(style="dark")

    fig, ax = plt.subplots()

    # Making background transparent
    ax.set_alpha(0)
    fig.patch.set_alpha(0)

    # Setting figure size
    fig.set_size_inches(
        max(transposed_values.shape[1] * 2, 10),
        max(transposed_values.shape[0] / 1.5, 5),
    )

    # Plotting the heatmap with Seaborn's color palette
    im = ax.imshow(
        transposed_values,
        vmax=transposed_values.max(),
        vmin=-transposed_values.min(),
        cmap=sns.color_palette("vlag_r", as_cmap=True),
        aspect="auto",
    )

    # Creating colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Token Attribution", rotation=-90, va="bottom")
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="white")

    # Setting ticks and labels with white color for visibility
    ax.set_xticks(np.arange(len(input_names)), labels=input_names)
    ax.set_yticks(np.arange(len(output_names)), labels=output_names)
    plt.setp(ax.get_xticklabels(), color="white", rotation=45, ha="right")
    plt.setp(ax.get_yticklabels(), color="white")

    # Adjusting tick labels
    ax.tick_params(
        top=True, bottom=False, labeltop=False, labelbottom=True, color="white"
    )

    # Adding text annotations - not used for readability
    # for i in range(transposed_values.shape[0]):
    #    for j in range(transposed_values.shape[1]):
    #        val = transposed_values[i, j]
    #        color = "black" if 0.2 < im.norm(val) < 0.8 else "white"
    #        ax.text(j, i, f"{val:.4f}", ha="center", va="center", color=color)

    return plt
