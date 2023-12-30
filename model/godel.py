# GODEL model module for chat interaction and model instance control

# external imports
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# internal imports
from utils import modelling as mdl

# model and tokenizer instance
TOKENIZER = AutoTokenizer.from_pretrained("microsoft/GODEL-v1_1-large-seq2seq")
MODEL = AutoModelForSeq2SeqLM.from_pretrained("microsoft/GODEL-v1_1-large-seq2seq")
CONFIG = {"max_new_tokens": 50, "min_length": 8, "top_p": 0.9, "do_sample": True}


# TODO: Make config variable
def set_config(config: dict = None):
    if config is None:
        config = {}

    MODEL.config.max_new_tokens = 50
    MODEL.config.min_length = 8
    MODEL.config.top_p = 0.9
    MODEL.config.do_sample = True


# formatting class to formatting input for the model
# CREDIT: Adapted from official interference example on Huggingface
## see https://huggingface.co/microsoft/GODEL-v1_1-large-seq2seq
def format_prompt(message: str, history: list, system_prompt: str, knowledge: str = ""):
    # user input prompt initialization
    prompt = ""

    # limits the prompt elements to the maximum token count
    message, history, system_prompt, knowledge = mdl.prompt_limiter(
        TOKENIZER, message, history, system_prompt, knowledge
    )

    # adds knowledge text if not empty
    if knowledge != "":
        knowledge = "[KNOWLEDGE] " + knowledge

    # adds conversation history to the prompt
    for conversation in history:
        prompt += f"EOS {conversation[0]} EOS {conversation[1]}"

    # adds the message to the prompt
    prompt += f" {message}"
    # combines the entire prompt
    full_prompt = f"{system_prompt} [CONTEXT] {prompt} {knowledge}"

    # returns the formatted prompt
    return full_prompt


# response class calling the model and returning the model output message
# CREDIT: Copied from official interference example on Huggingface
## see https://huggingface.co/microsoft/GODEL-v1_1-large-seq2seq
def respond(prompt):
    input_ids = TOKENIZER(f"{prompt}", return_tensors="pt").input_ids
    outputs = MODEL.generate(input_ids, **CONFIG)
    output = TOKENIZER.decode(outputs[0], skip_special_tokens=True)

    return output
