# modelling util module providing formatting functions for model functionalities

# external imports
import torch
import gradio as gr
from transformers import BitsAndBytesConfig


# function that limits the prompt to contain model runtime
# tries to keep as much as possible, always keeping at least message and system prompt
def prompt_limiter(
    tokenizer, message: str, history: list, system_prompt: str, knowledge: str = ""
):
    # initializing the new prompt history empty
    prompt_history = []
    # getting the current token count for the message, system prompt, and knowledge
    pre_count = (
        token_counter(tokenizer, message)
        + token_counter(tokenizer, system_prompt)
        + token_counter(tokenizer, knowledge)
    )

    # validating the token count against threshold of 1024
    # check if token count already too high without history
    if pre_count > 1024:

        # check if token count too high even without knowledge and history
        if (
            token_counter(tokenizer, message) + token_counter(tokenizer, system_prompt)
            > 1024
        ):

            # show warning and raise error
            gr.Warning("Message and system prompt are too long. Please shorten them.")
            raise RuntimeError(
                "Message and system prompt are too long. Please shorten them."
            )

        # show warning and return with empty history and empty knowledge
        gr.Warning("""
                   Input too long.
                   Knowledge and conversation history have been removed to keep model running.
                   """)
        return message, prompt_history, system_prompt, ""

    # if token count small enough, adding history bit by bit
    if pre_count < 800:
        # setting the count to the precount
        count = pre_count
        # reversing the history to prioritize recent conversations
        history.reverse()

        # iterating through the history
        for conversation in history:

            # checking the token count i´with the current conversation
            count += token_counter(tokenizer, conversation[0]) + token_counter(
                tokenizer, conversation[1]
            )

            # add conversation or break loop depending on token count
            if count < 1024:
                prompt_history.append(conversation)
            else:
                break

    # return the message, adapted, system prompt, and knowledge
    return message, prompt_history, system_prompt, knowledge


# token counter function using the model tokenizer
def token_counter(tokenizer, text: str):
    # tokenize the text
    tokens = tokenizer(text, return_tensors="pt").input_ids
    # return the token count
    return len(tokens[0])


def get_device():
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    return device


# setting device based on available hardware
def gpu_loading_config(max_memory: str = "15000MB"):
    n_gpus = torch.cuda.device_count()

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    return n_gpus, max_memory, bnb_config


# formatting mistral attention values
# CREDIT: copied and adapted from BERTViz
# see https://github.com/jessevig/bertviz
def format_mistral_attention(attention_values):
    squeezed = []
    for layer_attention in attention_values:
        layer_attention = layer_attention.squeeze(0)
        squeezed.append(layer_attention)
    return torch.stack(squeezed)
