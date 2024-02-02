# controller for the application that calls the model and explanation functions
# returns the updated conversation history and extra elements

# external imports
import gradio as gr

# internal imports
from model import godel
from model import mistral
from explanation import interpret_shap as shap_int, visualize as viz


# main interference function that that calls chat functions depending on selections
# is getting called on every chat submit
def interference(
    prompt: str,
    history: list,
    knowledge: str,
    system_prompt: str,
    xai_selection: str,
    model_selection: str,
):
    # if no proper system prompt is given, use a default one
    if system_prompt in ("", " "):
        system_prompt = """
            You are a helpful, respectful and honest assistant.
            Always answer as helpfully as possible, while being safe.
        """

    if model_selection.lower == "mistral":
        model = mistral
    else:
        model = godel

    # if a XAI approach is selected, grab the XAI module instance
    if xai_selection in ("SHAP", "Attention"):
        # matching selection
        match xai_selection.lower():
            case "shap":
                xai = shap_int
            case "attention":
                xai = viz
            case _:
                # use Gradio warning to display error message
                gr.Warning(f"""
                    There was an error in the selected XAI Approach.
                    It is "{xai_selection}"
                    """)
                # raise runtime exception
                raise RuntimeError("There was an error in the selected XAI approach.")

        # call the explained chat function with the model instance
        prompt_output, history_output, xai_graphic, xai_markup = explained_chat(
            model=model,
            xai=xai,
            message=prompt,
            history=history,
            system_prompt=system_prompt,
            knowledge=knowledge,
        )
    # if no XAI approach is selected call the vanilla chat function
    else:
        # call the vanilla chat function
        prompt_output, history_output = vanilla_chat(
            model=model,
            message=prompt,
            history=history,
            system_prompt=system_prompt,
            knowledge=knowledge,
        )
        # set XAI outputs to disclaimer html/none
        xai_graphic, xai_markup = (
            """
            <div style="text-align: center"><h4>Without Selected XAI Approach,
            no graphic will be displayed</h4></div>
            """,
            [("", "")],
        )

    # return the outputs
    return prompt_output, history_output, xai_graphic, xai_markup


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
    #message, history, system_prompt, knowledge = mdl.prompt_limiter(
    #    message, history, system_prompt, knowledge
    #)
    prompt = model.format_prompt(message, history, system_prompt, knowledge)

    # generating an answer using the methods chat function
    answer, xai_graphic, xai_markup = xai.chat_explained(model, prompt)

    # updating the chat history with the new answer
    history.append((message, answer))

    # returning the updated history, xai graphic and xai plot elements
    return "", history, xai_graphic, xai_markup
