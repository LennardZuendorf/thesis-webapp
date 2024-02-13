# visualization module that creates an attention visualization


# internal imports
from utils import formatting as fmt, modelling as mdl
from model import mistral
from .markup import markup_text


# chat function that returns an answer
# and marked text based on attention
def chat_explained(model, prompt):

    print(f"Running explained chat with prompt {prompt}.")

    # get encoded input
    input_ids = model.TOKENIZER(
        prompt, return_tensors="pt", add_special_tokens=True
    ).input_ids

    # generate output of the  model
    decoder_ids = model.MODEL.generate(input_ids, generation_config=model.CONFIG)

    # get input and output text as list of strings
    input_text = fmt.format_tokens(model.TOKENIZER.convert_ids_to_tokens(input_ids[0]))
    output_text = fmt.format_tokens(
        model.TOKENIZER.convert_ids_to_tokens(decoder_ids[0])
    )

    # checking if model is mistral
    if type(model.MODEL) == type(mistral.MODEL):

        # get attention values for the input vectors, specific to mistral
        attention_output = model.MODEL(input_ids, output_attentions=True).attentions

        # averaging attention across layers and heads
        attention_output = mdl.format_mistral_attention(attention_output)
        averaged_attention = fmt.avg_attention(attention_output, model="mistral")

    # otherwise use attention visualization for godel
    else:
        # get attention values for the input and output vectors
        # using already generated input and output
        attention_output = model.MODEL(
            input_ids=input_ids,
            decoder_input_ids=decoder_ids,
            output_attentions=True,
        )

        # averaging attention across layers
        averaged_attention = fmt.avg_attention(attention_output, model="godel")

    # format response text for clean output
    response_text = fmt.format_output_text(output_text)
    # setting placeholder for iFrame graphic
    graphic = (
        "<div style='text-align: center; font-family:arial;'><h4>Attention"
        " Visualization doesn't support an interactive graphic.</h4></div>"
    )
    # creating marked text using markup_text function and attention
    print(f"Creating marked text with {input_text}.")
    marked_text = markup_text(input_text, averaged_attention, variant="visualizer")

    # returning response, graphic and marked text array
    return response_text, graphic, marked_text, None
