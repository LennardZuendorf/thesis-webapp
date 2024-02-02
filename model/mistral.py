# Mistral model module for chat interaction and model instance control

# external imports
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import gradio as gr

# internal imports
from utils import modelling as mdl

# global model and tokenizer instance (created on inital build)
device = mdl.get_device()
if device == torch.device("cuda"):
    n_gpus, max_memory, bnb_config = mdl.gpu_loading_config()

    MODEL = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-7B-Instruct-v0.2",
        quantization_config=bnb_config,
        device_map="auto",  # dispatch efficiently the model on the available ressources
        max_memory={i: max_memory for i in range(n_gpus)},
    )

else:
    MODEL = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
    MODEL.to(device)
TOKENIZER = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

# default model config
CONFIG = {"max_new_tokens": 50, "min_length": 8, "top_p": 0.9, "do_sample": True}


# function to (re) set config
def set_config(config: dict):
    global CONFIG

    # if config dict is given, update it
    if config != {}:
        CONFIG = config
    else:
        # hard setting model config to default
        # needed for shap
        MODEL.config.max_new_tokens = 50
        MODEL.config.min_length = 8
        MODEL.config.top_p = 0.9
        MODEL.config.do_sample = True


# advanced formatting function that takes into a account a conversation history
# CREDIT: adapted from Venkata Bhanu Teja Pallakonda in Huggingface discussions
## see https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1/discussions/
def format_prompt(message: str, history: list, system_prompt: str, knowledge: str = ""):
    prompt = ""

    if knowledge != "":
        gr.Info("""
    Mistral doesn't support additional knowledge, it's gonna be ignored.
    """)

    # if no history, use system prompt and example message
    if len(history) == 0:
        prompt = f"""<s>[INST] {system_prompt} [/INST] How can I help you today? </s>
      [INST] {message} [/INST]"""
    else:
        # takes the very first exchange and the system prompt as base
        for user_prompt, bot_response in history[0]:
            prompt = (
                f"<s>[INST] {system_prompt} {user_prompt} [/INST] {bot_response}</s>"
            )

        # takes all the following conversations and adds them as context
        prompt += "".join(
            f"[INST] {user_prompt} [/INST] {bot_response}</s>"
            for user_prompt, bot_response in history[1:]
        )

    return prompt


# function to extract real answer because mistral always returns the full prompt
def format_answer(answer: str):
    # empty answer string
    formatted_answer = ""

    # extracting text after INST tokens
    parts = answer.split("[/INST]")
    if len(parts) >= 3:
        # Return the text after the second occurrence of [/INST]
        formatted_answer = parts[2].strip()
    else:
        # Return an empty string if there are fewer than two occurrences of [/INST]
        formatted_answer = ""

    return formatted_answer


def respond(prompt: str):

    # tokenizing inputs and configuring model
    input_ids = TOKENIZER(f"{prompt}", return_tensors="pt")["input_ids"]

    # generating text with tokenized input, returning output
    output_ids = MODEL.generate(input_ids, max_new_tokens=50, generation_config=CONFIG)
    output_text = TOKENIZER.batch_decode(output_ids)

    return format_answer(output_text)
