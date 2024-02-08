# visualization module that creates an attention visualization


# internal imports
from utils import formatting as fmt
from model import godel
from .markup import markup_text


# chat function that returns an answer
# and marked text based on attention
def chat_explained(model, prompt):

    model.set_config({"return_dict": True})

    # get encoded input
    encoder_input_ids = model.TOKENIZER(
        prompt, return_tensors="pt", add_special_tokens=True
    ).input_ids
    # generate output together with attentions of the model
    decoder_input_ids = model.MODEL.generate(
        encoder_input_ids, output_attentions=True, generation_config=model.CONFIG
    )

    # get input and output text as list of strings
    encoder_text = fmt.format_tokens(
        model.TOKENIZER.convert_ids_to_tokens(encoder_input_ids[0])
    )
    decoder_text = fmt.format_tokens(
        model.TOKENIZER.convert_ids_to_tokens(decoder_input_ids[0])
    )

    # getting attention if model is godel
    if isinstance(model, godel):
        print("attention.py: Model detected to be GODEL")

        # get attention values for the input and output vectors
        # using already generated input and output
        attention_output = model.MODEL.generate(
            input_ids=encoder_input_ids,
            decoder_input_ids=decoder_input_ids,
            output_attentions=True,
        )

        # averaging attention across layers
        averaged_attention = fmt.avg_attention(attention_output)

    # getting attention is model is mistral
    else:
        averaged_attention = fmt.avg_attention(decoder_input_ids)

    # format response text for clean output
    response_text = fmt.format_output_text(decoder_text)
    # setting placeholder for iFrame graphic
    graphic = (
        "<div style='text-align: center; font-family:arial;'><h4>Attention"
        " Visualization doesn't support an interactive graphic.</h4></div>"
    )
    # creating marked text using markup_text function and attention
    marked_text = markup_text(encoder_text, averaged_attention, variant="visualizer")

    # returning response, graphic and marked text array
    return response_text, graphic, marked_text, None
