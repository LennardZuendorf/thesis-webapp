# package imports
import gradio as gr

# internal imports
from model import mistral, llama2 as llama

# default model settings
model_temperature = 0.7
model_max_new_tokens = 100
model_top_p = 0.95
model_repetition_penalty = 1.1

def interference(prompt, history,system_prompt, model, xai, ):
    global model_temperature, model_max_new_tokens, model_top_p, model_repetition_penalty

    if system_prompt == "":
        system_prompt = "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe."

    if xai =="None":

        match model:
            case "Mistral":
                prompt_output, history_output = mistral.chat(prompt, history, model_temperature, model_max_new_tokens,
                                                             model_top_p, model_repetition_penalty, system_prompt)
            case "LlaMa 2":
                prompt_output, history_output = llama.chat(prompt, history, model_temperature, model_max_new_tokens,
                                                           model_top_p, model_repetition_penalty, system_prompt)
            case _:
                gr.Warning(f"There was an error in the selected model. It is \"{model}\"")
                return "", "", ""

        xai_output = ""

    elif xai == "SHAP" or xai == "Visualizer":

        match model:
            case "Mistral":
                prompt_output, history_output, xai_output = "", "", ""

            case "LlaMa 2":
                prompt_output, history_output, xai_output = "", "", ""

            case _:
                gr.Warning(f"There was an error in the selected model. It is \"{model}\"")
                return "", "", ""

    else:
        gr.Warning(f"There was an error in the selected XAI Approach. It is \"{xai}\"")
        return "", "", ""

    return prompt_output, history_output