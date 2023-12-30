# Mistral 7B model module for chat interaction and model instance control

# external imports
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch
import gradio as gr

# global variables for model and tokenizer, config
MODEL = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
TOKENIZER = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
MISTRAL_CONFIG = GenerationConfig.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")

MISTRAL_CONFIG.update(
    **{
        "temperature": 0.7,
        "max_new_tokens": 50,
        "top_p": 0.9,
        "repetition_penalty": 1.2,
        "do_sample": True,
        "seed": 42,
    }
)


# function to format the prompt to include chat history, message
# CREDIT: adapted from Venkata Bhanu Teja Pallakonda in Huggingface discussions
## see https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1/discussions/


def format_prompt(message: str, history: list, system_prompt: str, knowledge: str = ""):
    prompt = ""
    if knowledge != "":
        gr.Warning(
            """Mistral does not support
            additionally knowledge!"""
        )

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


# generation class returning the model response based on the input
# CREDIT: adapted from official Mistral Ai 7B Instruct documentation on Huggingface
## see https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1
def respond(prompt):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # tokenizing inputs and configuring model
    input_ids = TOKENIZER(f"{prompt}", return_tensors="pt")
    model_input = input_ids.to(device)
    MODEL.to(device)

    # generating text with tokenized input, returning output
    output_ids = MODEL.generate(model_input, generation_config=MISTRAL_CONFIG)
    output_text = TOKENIZER.batch_decode(output_ids)
    return output_text[0]
