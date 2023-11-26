from huggingface_hub import InferenceClient
import os
import gradio as gr

token = os.environ.get("HGFTOKEN")

interference = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.1"
)

model_temperature = 0.7
model_max_new_tokens = 256
model_top_p = 0.95
model_repetition_penalty = 1.1

def chat (prompt, history,):

    formatted_prompt = format_prompt(prompt, history)
    answer=respond(formatted_prompt)

    history.append((prompt, answer))

    return "",history

def format_prompt(message, history):
    prompt = "<s>"
    for user_prompt, bot_response in history:
        prompt += f"[INST] {user_prompt} [/INST]"
        prompt += f" {bot_response}</s> "
    prompt += f"[INST] {message} [/INST]"
    return prompt

def respond(formatted_prompt):
    temperature = float(model_temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(model_top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=model_max_new_tokens,
        top_p=top_p,
        repetition_penalty=model_repetition_penalty,
        do_sample=True,
        seed=42,
    )

    output = interference.text_generation(formatted_prompt, **generate_kwargs, stream=False, details=True, return_full_text=False).generated_text
    return output