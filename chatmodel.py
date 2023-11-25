from transformers import pipeline
import torch
from transformers import AutoTokenizer
import os

token = os.environ.get("HGFTOKEN")

model = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model, token=token)

llama_pipeline = pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float32,
    device_map="auto",
)

# Formatting function for message and history
def format_message(message: str, history: list, system_prompt:str, memory_limit: int = 3) -> str:

    if len(history) > memory_limit:
        history = history[-memory_limit:]

    system_prompt="<s>[INST] <<SYS>>\n"+system_prompt+"\n<</SYS>>"

    if len(history) == 0:
        return system_prompt + f"{message} [/INST]"

    formatted_message = system_prompt + f"{history[0][0]} [/INST] {history[0][1]} </s>"

    # Handle conversation history
    for user_msg, model_answer in history[1:]:
        formatted_message += f"<s>[INST] {user_msg} [/INST] {model_answer} </s>"

    # Handle the current message
    formatted_message += f"<s>[INST] {message} [/INST]"

    return formatted_message

# Generate a response from the Llama model
def interference(message: str, history: list, ) -> str:
    system_prompt="You are a helpful assistant providing reasonable answers."

    query = format_message(message, history, system_prompt)
    response = ""

    sequences = llama_pipeline(
        query,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=1024,
    )

    generated_text = sequences[0]['generated_text']
    response = generated_text[len(query):]  # Remove the prompt from the output

    print("Chatbot:", response.strip())
    return response.strip()