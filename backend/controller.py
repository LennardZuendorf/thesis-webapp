# package imports
import gradio as gr

# internal imports
from model import mistral, llama2 as llama


def interference(
    prompt,
    history,
    system_prompt,
    model,
    xai,
):
    if system_prompt == "":
        system_prompt = """You are a helpful, respectful and honest assistant.
                         Always answer as helpfully as possible, while being safe."""

    if xai == "None":
        match model:
            case "Mistral":
                prompt_output, history_output = mistral.chat(
                    prompt, history, system_prompt
                )
            case "LlaMa 2":
                prompt_output, history_output = llama.chat(
                    prompt, history, system_prompt
                )
            case _:
                gr.Warning("There was an error in the selected model.")
                return "", "", ""

        xai_output = ""

    elif xai in ("SHAP", "Visualizer"):
        match model:
            case "Mistral":
                prompt_output, history_output, xai_output = "", "", ""

            case "LlaMa 2":
                prompt_output, history_output, xai_output = "", "", ""

            case _:
                gr.Warning(f'There was an error in the selected model. It is "{model}"')
                return "", "", ""

    else:
        gr.Warning(f'There was an error in the selected XAI Approach. It is "{xai}"')
        return "", "", ""

    return prompt_output, history_output, xai_output
