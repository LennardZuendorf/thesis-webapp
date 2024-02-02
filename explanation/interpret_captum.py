# external imports
from captum.attr import LLMAttribution, TextTokenInput, KernelShap
import torch

# internal imports
from utils import formatting as fmt
from .markup import markup_text


# main explain function that returns a chat with explanations
def chat_explained(model, prompt):
    model.set_config({})

    # creating llm attribution class with KernelSHAP and Mistal Model, Tokenizer
    llm_attribution = LLMAttribution(KernelShap(model.MODEL), model.TOKENIZER)

    # generation attribution
    attribution_input = TextTokenInput(prompt, model.TOKENIZER)
    attribution_result = llm_attribution.attribute(attribution_input, gen_args=model.CONFIG.to_dict())

    # extracting values and input tokens
    values = attribution_result.seq_attr.to(torch.device("cpu")).numpy()
    input_tokens = fmt.format_tokens(attribution_result.input_tokens)

    # raising error if mismatch occurs
    if len(attribution_result.input_tokens) != len(values):
        raise RuntimeError("values and input len mismatch")

    # getting response text, graphic placeholder and marked text object
    response_text = fmt.format_output_text(attribution_result.output_tokens)
    graphic = (
        "<div style='text-align: center; font-family:arial;'><h4>Attention"
        "Intepretation with Captum doesn't support an interactive graphic.</h4></div>"
    )
    marked_text = markup_text(input_tokens, values, variant="captum")

    # return response, graphic and marked_text array
    return response_text, graphic, marked_text
