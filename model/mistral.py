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

# default model config
CONFIG = GenerationConfig.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
CONFIG.update(**{
    "temperature": 0.7,
    "max_new_tokens": 50,
    "max_length": 50,
    "top_p": 0.9,
    "repetition_penalty": 1.2,
    "do_sample": True,
    "seed": 42,
})


# function to (re) set config
def set_config(config_dict: dict):

    # if config dict is not given, set to default
    if config_dict == {}:
        config_dict = {
            "temperature": 0.7,
            "max_new_tokens": 50,
            "max_length": 50,
            "top_p": 0.9,
            "repetition_penalty": 1.2,
            "do_sample": True,
            "seed": 42,
        }

    CONFIG.update(**dict)


# advanced formatting function that takes into a account a conversation history
# CREDIT: adapated from the Mistral AI Instruct chat template
# see https://github.com/chujiezheng/chat_templates/blob/main/chat_templates/mistral-instruct.jinja 
def format_prompt(message: str, history: list, system_prompt: str, knowledge: str = ""):
    prompt = ""

    if knowledge != "":
        gr.Info("""
            Mistral doesn't support additional knowledge, it's gonna be ignored.
            """)

    # if no history, use system prompt and example message
    if len(history) == 0:
        prompt = f"""
            <s>[INST] {system_prompt} [/INST] How can I help you today? </s>
            [INST] {message} [/INST]
            """
    else:
        # takes the very first exchange and the system prompt as base
        prompt = f"""
            <s>[INST] {system_prompt} {history[0][0]} [/INST] {history[0][1]}</s>
            """

        # adds conversation history to the prompt
        for conversation in history[1:]:
            # takes all the following conversations and adds them as context
            prompt += "".join(
                f"\n[INST] {conversation[0]} [/INST] {conversation[1]}</s>"
            )

        prompt += """\n[INST] {message} [/INST]"""

    # returns full prompt
    return prompt


# function to extract real answer because mistral always returns the full prompt
def format_answer(answer: str):
    # empty answer string
    formatted_answer = ""

    # splitting answer by instruction tokens
    segments = answer.split("[/INST]")

    # checking if proper history got returned
    if len(segments) > 1:
        # return text after the last ['/INST'] - reponse to last message
        formatted_answer = segments[-1].strip()
    else:
        # return warning and full answer if not enough [/INST] tokens found
        gr.Warning("""
                   There was an issue with answer formatting...\n
                   returning the full answer.
                   """)
        formatted_answer = answer

    print(f"CUT:\n {answer}\nINTO:\n{formatted_answer}")
    return formatted_answer


def respond(prompt: str):

    # tokenizing inputs and configuring model
    input_ids = TOKENIZER(f"{prompt}", return_tensors="pt")["input_ids"].to(device)

    # generating text with tokenized input, returning output
    output_ids = MODEL.generate(input_ids, generation_config=CONFIG)
    output_text = TOKENIZER.batch_decode(output_ids)
    output_text = fmt.format_output_text(output_text)

    return format_answer(output_text)
