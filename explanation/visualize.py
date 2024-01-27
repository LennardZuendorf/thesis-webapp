# visualization module that creates an attention visualization using BERTViz


# external imports
from bertviz import neuron_view as nv


# internal imports
from utils import formatting as fmt
from .markup import markup_text


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

    averaged_attention = fmt.avg_attention(attention_output)

    # create the response text and marked text for ui
    response_text = fmt.format_output_text(decoder_text)
    xai_graphic = attention_graphic(encoder_text, decoder_text, model)
    marked_text = markup_text(encoder_text, averaged_attention, variant="visualizer")

    return response_text, xai_graphic, marked_text


def attention_graphic(encoder_text, decoder_text, model):

    # set model type to BERT (to fake out BERTViz)
    model_type = "bert"

    # create sentence a and b from list of strings
    sentence_a = " ".join(encoder_text)
    sentence_b = " ".join(decoder_text)

    # display neuron view
    return nv.show(
        model.MODEL,
        model_type,
        model.TOKENIZER,
        sentence_a,
        sentence_b,
        display_mode="light",
        layer=2,
        head=0,
        html_action="return",
    )
