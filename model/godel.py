# GODEL model module for chat interaction and model instance control
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# model and tokenizer instance
TOKENIZER = AutoTokenizer.from_pretrained("microsoft/GODEL-v1_1-large-seq2seq")
MODEL = AutoModelForSeq2SeqLM.from_pretrained("microsoft/GODEL-v1_1-large-seq2seq")
GODEL_CONFIG = {"max_new_tokens": 50, "min_length": 8, "top_p": 0.9, "do_sample": True}


# formatting class to formatting input for the model
# CREDIT: Adapted from official interference example on Huggingface
## see https://huggingface.co/microsoft/GODEL-v1_1-large-seq2seq
def format_prompt(message: str, history: list, system_prompt: str, knowledge: str = ""):
    prompt = ""

    # adds knowledge text if not empty
    if knowledge != "":
        knowledge = "[KNOWLEDGE] " + knowledge

    history.append([message])
    for user_prompt, bot_response in history:
        prompt += f"EOS {user_prompt} EOS {bot_response}"

    prompt = f"{system_prompt} [CONTEXT] {prompt} {knowledge}"

    # returns the full combined prompt for the model
    return prompt


# response class calling the model and returning the model output message
# CREDIT: Copied from official interference example on Huggingface
## see https://huggingface.co/microsoft/GODEL-v1_1-large-seq2seq
def respond(prompt):
    input_ids = TOKENIZER(f"{prompt}", return_tensors="pt").input_ids
    outputs = MODEL.generate(input_ids, **GODEL_CONFIG)
    output = TOKENIZER.decode(outputs[0], skip_special_tokens=True)

    return output
