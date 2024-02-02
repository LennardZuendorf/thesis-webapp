# Mistral model module for chat interaction and model instance control

# external imports
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch
import gradio as gr

# internal imports
from utils import modelling as mdl
from utils import formatting as fmt

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
TOKENIZER.pad_token=TOKENIZER.eos_token

# default model config
CONFIG = GenerationConfig.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
CONFIG.update(**{
        "temperature": 0.7,
        "max_new_tokens": 50,
        "top_p": 0.9,
        "repetition_penalty": 1.2,
        "do_sample": True,
        "seed": 42
})


# function to (re) set config
def set_config(config: dict):
    global CONFIG

    # if config dict is given, update it
    if config != {}:
        CONFIG.update(**dict)
    else:
        CONFIG.update(**{
                "temperature": 0.7,
                "max_new_tokens": 50,
                "top_p": 0.9,
                "repetition_penalty": 1.2,
                "do_sample": True,
                "seed": 42
        })


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

    if type(answer) == list:
        answer = fmt.format_output_text(answer)

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
    input_ids = TOKENIZER(f"{prompt}", return_tensors="pt")["input_ids"].to(device)

    # generating text with tokenized input, returning output
    output_ids = MODEL.generate(input_ids, generation_config=CONFIG)
    output_text = TOKENIZER.batch_decode(output_ids)

    return fmt.format_output_text(output_text)
