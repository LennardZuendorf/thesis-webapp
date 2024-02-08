# main application file initializing the gradio based ui and calling other

# standard imports
import os

# external imports
from fastapi import FastAPI
import markdown
import gradio as gr
from uvicorn import run
from gradio_iframe import iFrame

# internal imports
from backend.controller import interference
from explanation.markup import color_codes


# global Variables and js/css
# creating FastAPI app and getting color codes
app = FastAPI()
coloring = color_codes()


# defining custom css and js for certain environments
css = """
    .examples {text-align: start;}
    .seperatedRow {border-top: 1rem solid;}",
    """
# custom js to force lightmode in custom environments
if os.environ["HOSTING"].lower() != "spaces":
    js = """
    function () {
        gradioURL = window.location.href
        if (!gradioURL.endsWith('?__theme=light')) {
        window.location.replace(gradioURL + '?__theme=light');
        }
    }
    """
else:
    js = ""


# different functions to provide frontend abilities
# function to load markdown files
def load_md(path):
    # CREDIT: official python-markdown documentation
    ## see https://python-markdown.github.io/reference/)
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
    return markdown.markdown(text)


# function to display the system prompt info
def system_prompt_info(sys_prompt_txt):
    # display the system prompt using the Gradio Info component
    gr.Info(f"The system prompt was set to:\n {sys_prompt_txt}")


# function to display the xai info
def xai_info(xai_radio):
    # display the xai method using the Gradio Info component
    if xai_radio != "None":
        gr.Info(f"The XAI was set to:\n {xai_radio}")
    else:
        gr.Info("No XAI method was selected.")


def model_info(model_radio):
    # displays the selected model using the Gradio Info component
    gr.Info(f"The following model was selected:\n {model_radio} ")


# ui interface based on Gradio Blocks
# see https://www.gradio.app/docs/interface)
with gr.Blocks(
    css=css,
    js=js,
    title="Thesis Webapp Showcase",
    head="<head>",
) as ui:
    # header row with markdown based text
    with gr.Row():
        # markdown component to display the header
        gr.Markdown("""
            # Thesis Demo - AI Chat Application with GODEL
            Interpretability powered by shap and attention visualization,
            ### Select between tabs below for the different views.
            """)
    # ChatBot tab used to chat with the AI chatbot
    with gr.Tab("AI ChatBot"):
        with gr.Row():
            # markdown component to display the header of the current tab
            gr.Markdown("""
                ### ChatBot Demo
                Chat with the AI ChatBot using the textbox below.
                Manipulate the settings in the row above,
                including the selection of the model,
                the system prompt and the XAI method.

                **See Explanations in the accordion above the chat.**

                """)
        # row with columns for the different settings
        with gr.Row(equal_height=True):
            with gr.Accordion("Application Settings", open=False):
                # column that takes up 3/4 of the row
                with gr.Column(scale=2):
                    # textbox to enter the system prompt
                    system_prompt = gr.Textbox(
                        label="System Prompt",
                        info="Set the models system prompt, dictating how it answers.",
                        # default system prompt is set to this in the backend
                        placeholder="""
                            You are a helpful, respectful and honest assistant. Always
                            answer as helpfully as possible, while being safe.
                            """,
                    )
                # column that takes up 1/4 of the row
                with gr.Column(scale=1):
                    # checkbox group to select the xai method
                    xai_selection = gr.Radio(
                        ["None", "SHAP", "Attention"],
                        label="Interpretability Settings",
                        info=(
                            "Select a Interpretability Approach Implementation to use."
                        ),
                        value="None",
                        interactive=True,
                        show_label=True,
                    )
                # column that takes up 1/4 of the row
                with gr.Column(scale=1):
                    # checkbox group to select the xai method
                    model_selection = gr.Radio(
                        ["GODEL", "Mistral"],
                        label="Model Settings",
                        info="Select a Model to use.",
                        value="Mistral",
                        interactive=True,
                        show_label=True,
                    )

                # calling info functions on inputs/submits for different settings
                system_prompt.change(system_prompt_info, [system_prompt])
                xai_selection.change(xai_info, [xai_selection])
                model_selection.change(model_info, [model_selection])

        # row with chatbot ui displaying "conversation" with the model
        with gr.Row(equal_height=True):
            # group to display components closely together
            with gr.Group(elem_classes="border: 1px solid black;"):
                # accordion to display the normalized input explanation
                with gr.Accordion(label="Input Explanation", open=False):
                    gr.Markdown("""
                    The explanations are based on 10 buckets that range between the
                    lowest negative value (1 to 5) and the highest positive attribution value (6 to 10).
                    **The legend shows the color for each bucket.**
                                
                    *HINT*: This works best in light mode.
                    """)
                    xai_text = gr.HighlightedText(
                        color_map=coloring,
                        label="Input Explanation",
                        show_legend=True,
                        show_label=False,
                    )
                # out of the  box chatbot component with avatar images
                # see documentation: https://www.gradio.app/docs/chatbot
                chatbot = gr.Chatbot(
                    layout="panel",
                    show_copy_button=True,
                    avatar_images=("./public/human.jpg", "./public/bot.jpg"),
                )
                # extenable components for extra knowledge
                with gr.Accordion(label="Additional Knowledge", open=False):
                    gr.Markdown("""
                        *Hint:* Add extra knowledge to see GODEL work the best.
                        Knowledge doesn't work mith Mistral and will be ignored.
                        """)
                    # textbox to enter the knowledge
                    knowledge_input = gr.Textbox(
                        value="",
                        label="Knowledge",
                        max_lines=5,
                        info="Add additional context knowledge.",
                        show_label=True,
                    )
                user_prompt = gr.Textbox(
                    label="Input Message",
                    max_lines=5,
                    info="""
                    Ask the ChatBot a question.
                    """,
                    show_label=True,
                )
        # row with columns for buttons to submit and clear content
        with gr.Row(elem_classes=""):
            with gr.Column():
                # out of the box clear button which clearn the given components (see
                # see: https://www.gradio.app/docs/clearbutton)
                clear_btn = gr.ClearButton([user_prompt, chatbot])
            with gr.Column():
                # submit button that calls the backend functions on click
                submit_btn = gr.Button("Submit", variant="primary")
        # row with content examples that get autofilled on click
        with gr.Row(elem_classes="examples"):
            with gr.Accordion("Mistral Model Examples", open=False):
                # examples util component
                # see: https://www.gradio.app/docs/examples
                gr.Examples(
                    label="Example Questions",
                    examples=[
                        ["Does money buy happiness?", "", "Mistral", "SHAP"],
                        ["Does money buy happiness?", "", "Mistral", "Attention"],
                    ],
                    inputs=[
                        user_prompt,
                        knowledge_input,
                        model_selection,
                        xai_selection,
                    ],
                )
            with gr.Accordion("GODEL Model Examples", open=False):
                # examples util component
                # see: https://www.gradio.app/docs/examples
                gr.Examples(
                    label="Example Questions",
                    examples=[
                        [
                            "How does a black hole form in space?",
                            (
                                "Black holes are created when a massive star's core"
                                " collapses after a supernova, forming an object with"
                                " gravity so intense that even light cannot escape."
                            ),
                            "GODEL",
                            "SHAP",
                        ],
                        [
                            (
                                "Explain the importance of the Rosetta Stone in"
                                " understanding ancient languages."
                            ),
                            (
                                "The Rosetta Stone, an ancient Egyptian artifact, was"
                                " key in decoding hieroglyphs, featuring the same text"
                                " in three scripts: hieroglyphs, Demotic, and Greek."
                            ),
                            "GODEL",
                            "Attention",
                        ],
                    ],
                    inputs=[
                        user_prompt,
                        knowledge_input,
                        model_selection,
                        xai_selection,
                    ],
                )

    # explanations tab used to provide explanations for a specific conversation
    with gr.Tab("Explanations"):
        # row with markdown component to display the header of the current tab
        with gr.Row():
            gr.Markdown("""
                ### Get Explanations for Conversations
                Get additional explanations for the last conversation you had with the AI ChatBot.
                Depending on the selected XAI method, different explanations are available.
                """)
        # row that displays the generated explanation of the model (if applicable)
        with gr.Row():
            # wraps the explanation html to display it statically
            xai_interactive = iFrame(
                label="Interactive Explanation",
                value=(
                    '<div style="text-align: center; font-family:arial;"><h4>No Graphic'
                    " to Display (Yet)</h4></div>"
                ),
                show_label=True,
                height="400px",
            )
        with gr.Row():
            with gr.Accordion("Explanation Plot", open=False):
                xai_plot = gr.Plot(
                    label="Input Sequence Attribution Plot", show_label=True
                )

    # functions to trigger the controller
    ## takes information for the chat and the xai selection
    ## returns prompt, history and xai data
    ## see backend/controller.py for more information
    submit_btn.click(
        interference,
        [
            user_prompt,
            chatbot,
            knowledge_input,
            system_prompt,
            xai_selection,
            model_selection,
        ],
        [user_prompt, chatbot, xai_interactive, xai_text, xai_plot],
    )
    # function triggered by the enter key
    user_prompt.submit(
        interference,
        [
            user_prompt,
            chatbot,
            knowledge_input,
            system_prompt,
            xai_selection,
            model_selection,
        ],
        [user_prompt, chatbot, xai_interactive, xai_text, xai_plot],
    )

    # final row to show legal information
    ## - credits, data protection and link to the License
    with gr.Tab(label="About"):
        # load about.md markdown
        gr.Markdown(value=load_md("public/about.md"))
        with gr.Accordion(label="Credits, Data Protection, License"):
            # load credits and dataprotection markdown
            gr.Markdown(value=load_md("public/credits_dataprotection_license.md"))

# mount function for fastAPI Application
app = gr.mount_gradio_app(app, ui, path="/")

# launch function to launch the application
if __name__ == "__main__":

    # use standard gradio launch option for hgf spaces
    if os.environ["HOSTING"].lower() == "spaces":
        # set password to deny public access
        ui.launch(auth=("htw", "berlin@123"))

    # otherwise run the application on port 8080 in reload mode
    ## for local development, uses Docker for Prod deployment
    run("main:app", port=8080, reload=True)
