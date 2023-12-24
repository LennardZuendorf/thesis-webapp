from huggingface_hub import InferenceClient
import os

# huggingface token used to load closed off models
token = os.environ.get("HGFTOKEN")

# interference client created from mistral 7b instruction fine tuned model
# credit: copied 1:1 from Hugging Face, Inc/ Omar Sanseviero (see https://huggingface.co/spaces/osanseviero/mistral-super-fast/)
interference = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.1"
)

temperature = 0.7
max_new_tokens = 100
top_p = 0.95
repetition_penalty = 1.1

# chat function - basically the main function calling other functions and returning a response to showcase in chatbot ui
def chat (prompt,history,system_prompt):

    # creating formatted prompt and calling for an answer from the model
    formatted_prompt = format_prompt(prompt, history)
    answer=respond(formatted_prompt,system_prompt)

    # updating the chat history with the new answer
    history.append((prompt, answer))

    # returning the chat history to be displayed in the chatbot ui
    return "",history

# function to format prompt in a way that is understandable for the text generation model
# credit: copied 1:1 from Hugging Face, Inc/ Omar Sanseviero (see https://huggingface.co/spaces/osanseviero/mistral-super-fast/)
def format_prompt(message, history):
    prompt = "<s>"

    # labeling each message in the history as bot or user
    for user_prompt, bot_response in history:
        prompt += f"[INST] {user_prompt} [/INST]"
        prompt += f" {bot_response}</s> "
    prompt += f"[INST] {message} [/INST]"
    return prompt

# function to get the response
# credit: minimally changed from Hugging Face, Inc/ Omar Sanseviero (see https://huggingface.co/spaces/osanseviero/mistral-super-fast/)
def respond(formatted_prompt, system_prompt):
    global temperature, max_new_tokens, top_p, repetition_penalty

    # setting model temperature and
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)

    # creating model arguments/settings
    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        seed=42,
    )

    # calling for model output and returning it
    output = interference.text_generation(formatted_prompt, **generate_kwargs, stream=False, details=True, return_full_text=False).generated_text
    return output