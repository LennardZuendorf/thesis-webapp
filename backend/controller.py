# controller for the application that calls the model and explanation functions
# and returns the updated conversation history

# external imports
import gradio as gr

# internal imports
from model import mistral, godel
from explanation import interpret, visualize


# main interference function that that calls chat functions depending on selections
def interference(
    prompt,
    history,
    system_prompt,
    model_selection,
    xai_selection,
):
    # if no system prompt is given, use a default one
    if system_prompt == "":
        system_prompt = """
            You are a helpful, respectful and honest assistant.
            Always answer as helpfully as possible, while being safe.
        """

    # grabs the model instance depending on the selection
    match model_selection.lower():
        case "mistral":
            model = mistral
        case "godel":
            model = godel
        case _:
            # use Gradio warning to display error message
            gr.Warning(
                f'There was an error in the selected model. It is "{model_selection}"'
            )
            raise RuntimeError("There was an error in the selected model.")

    # additionally, if the XAI approach is selected, grab the XAI instance
    if xai_selection in ("SHAP", "Visualizer"):
        match xai_selection.lower():
            case "shap":
                xai = interpret
            case "visualizer":
                xai = visualize
            case _:
                # use Gradio warning to display error message
                gr.Warning(
                    f"""
                    There was an error in the selected XAI Approach.
                    It is "{xai_selection}"
                    """
                )
                raise RuntimeError("There was an error in the selected XAI approach.")

        # call the explained chat function
        prompt_output, history_output, xai_graphic, xai_plot = explained_chat(
            model=model,
            xai=xai,
            message=prompt,
            history=history,
            system_prompt=system_prompt,
        )
    # if no (or invalid) XAI approach is selected call the vanilla chat function
    else:
        # call the vanilla chat function
        prompt_output, history_output = vanilla_chat(
            model=model,
            message=prompt,
            history=history,
            system_prompt=system_prompt,
        )
        # set XAI outputs to disclaimer html/none
        xai_graphic, xai_plot = "<div><h1>No Graphic to Display</h1></div>", None

    # return the outputs
    return prompt_output, history_output, xai_graphic, xai_plot


# simple chat function that calls the model
# formats prompts, calls for an answer and returns updated conversation history
def vanilla_chat(model, message: str, history: list, system_prompt: str):
    # formatting the prompt using the model's format_prompt function
    prompt = model.format_prompt(message, history, system_prompt)
    # generating an answer using the model's respond function
    answer = model.respond(prompt)

    # updating the chat history with the new answer
    history.append((prompt, answer))

    # returning the updated history
    return "", history


def explained_chat(model, xai, message: str, history: list, system_prompt: str):
    # formatting the prompt using the model's format_prompt function
    prompt = model.format_prompt(message, history, system_prompt)

    # generating an answer using the xai methods explain and respond function
    answer, xai_graphic, xai_plot = xai.chat_explained(model, prompt)
    # updating the chat history with the new answer
    history.append((prompt, answer))

    # returning the updated history, xai graphic and xai plot elements
    return "", [["", ""]], xai_graphic, xai_plot
