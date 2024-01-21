# controller for the application that calls the model and explanation functions
# and returns the updated conversation history

# external imports
import gradio as gr

# internal imports
from model import godel
from explanation import interpret_shap as sint, visualize as viz


# main interference function that that calls chat functions depending on selections
def interference(
    prompt: str,
    history: list,
    knowledge: str,
    system_prompt: str,
    xai_selection: str,
):
    # if no system prompt is given, use a default one
    if system_prompt == "":
        system_prompt = """
            You are a helpful, respectful and honest assistant.
            Always answer as helpfully as possible, while being safe.
        """

    # if a XAI approach is selected, grab the XAI instance
    if xai_selection in ("SHAP", "Attention"):
        match xai_selection.lower():
            case "shap":
                xai = sint
            case "attention":
                xai = viz
            case _:
                # use Gradio warning to display error message
                gr.Warning(f"""
                    There was an error in the selected XAI Approach.
                    It is "{xai_selection}"
                    """)
                raise RuntimeError("There was an error in the selected XAI approach.")

        # call the explained chat function
        prompt_output, history_output, xai_graphic, xai_plot, xai_markup = (
            explained_chat(
                model=godel,
                xai=xai,
                message=prompt,
                history=history,
                system_prompt=system_prompt,
                knowledge=knowledge,
            )
        )
    # if no (or invalid) XAI approach is selected call the vanilla chat function
    else:
        # call the vanilla chat function
        prompt_output, history_output = vanilla_chat(
            model=godel,
            message=prompt,
            history=history,
            system_prompt=system_prompt,
            knowledge=knowledge,
        )
        # set XAI outputs to disclaimer html/none
        xai_graphic, xai_plot, xai_markup = (
            """
            <div style="text-align: center"><h4>Without Selected XAI Approach,
            no graphic will be displayed</h4></div>
            """,
            None,
            [("", "")],
        )

    # return the outputs
    return prompt_output, history_output, xai_graphic, xai_plot, xai_markup


# simple chat function that calls the model
# formats prompts, calls for an answer and returns updated conversation history
def vanilla_chat(
    model, message: str, history: list, system_prompt: str, knowledge: str = ""
):
    # formatting the prompt using the model's format_prompt function
    prompt = model.format_prompt(message, history, system_prompt, knowledge)
    # generating an answer using the model's respond function
    answer = model.respond(prompt)

    # updating the chat history with the new answer
    history.append((message, answer))

    # returning the updated history
    return "", history


def explained_chat(
    model, xai, message: str, history: list, system_prompt: str, knowledge: str = ""
):
    # formatting the prompt using the model's format_prompt function
    prompt = model.format_prompt(message, history, system_prompt, knowledge)

    # generating an answer using the xai methods explain and respond function
    answer, xai_graphic, xai_plot, xai_markup = xai.chat_explained(model, prompt)

    # updating the chat history with the new answer
    history.append((message, answer))

    # returning the updated history, xai graphic and xai plot elements
    return "", history, xai_graphic, xai_plot, xai_markup
