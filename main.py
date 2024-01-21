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

# Global Variables and css
app = FastAPI()
css = "body {text-align: start !important;}"
coloring = color_codes()


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


# ui interface based on Gradio Blocks (see documentation:
# https://www.gradio.app/docs/interface)
with gr.Blocks(
    css="""
    .examples {text-align: start;}
    .seperatedRow {border-top: 1rem solid;}",
    """,
    title="Thesis Webapp Showcase",
    head="<head>",
) as ui:
    # header row with markdown based text
    with gr.Row():
        # markdown component to display the header
        gr.Markdown("""
            # Thesis Demo - AI Chat Application with GODEL
            ## Interpretability powered by SHAP and BERTVIZ
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
            # column that takes up 3/5 of the row
            with gr.Column(scale=3):
                # textbox to enter the system prompt
                system_prompt = gr.Textbox(
                    label="System Prompt",
                    info="Set the models system prompt, dictating how it answers.",
                    placeholder=(
                        "You are a helpful, respectful and honest assistant. Always"
                        " answer as helpfully as possible, while being safe."
                    ),
                )
            with gr.Column(scale=1):
                # checkbox group to select the xai method
                xai_selection = gr.Radio(
                    ["None", "SHAP", "Attention"],
                    label="XAI Settings",
                    info="Select a XAI Implementation to use.",
                    value="None",
                    interactive=True,
                    show_label=True,
                )

            # calling info functions on inputs for different settings
            system_prompt.submit(system_prompt_info, [system_prompt])
            xai_selection.input(xai_info, [xai_selection])

        # row with chatbot ui displaying "conversation" with the model
        with gr.Row(equal_height=True):
            with gr.Group(elem_classes="border: 1px solid black;"):
                # accordion to display the normalized input explanation
                with gr.Accordion(label="Input Explanation", open=False):
                    gr.Markdown("""
                    The explanations are based on 10 buckets that range between the
                    lowest negative value (1 to 5) and the highest positive attribution value (6 to 10).
                    **The legend show the color for each bucket.**
                    """)
                    xai_text = gr.HighlightedText(
                        color_map=coloring,
                        label="Input Explanation",
                        show_legend=True,
                        show_label=False,
                    )
                # out of the  box chatbot component
                # see documentation: https://www.gradio.app/docs/chatbot
                chatbot = gr.Chatbot(
                    layout="panel",
                    show_copy_button=True,
                    avatar_images=("./public/human.jpg", "./public/bot.jpg"),
                )
                # textbox to enter the knowledge
                with gr.Accordion(label="Additional Knowledge", open=False):
                    knowledge_input = gr.Textbox(
                        value="",
                        label="Knowledge",
                        max_lines=5,
                        info="Add additional context knowledge.",
                        show_label=True,
                    )
                # textbox to enter the user prompt
                user_prompt = gr.Textbox(
                    label="Input Message",
                    max_lines=5,
                    info="""
                    Ask the ChatBot a question.
                    Hint: More complicated question give better explanation insights!
                    """,
                    show_label=True,
                )
        # row with columns for buttons to submit and clear content
        with gr.Row(elem_classes=""):
            with gr.Column(scale=1):
                # out of the box clear button which clearn the given components (see
                # documentation: https://www.gradio.app/docs/clearbutton)
                clear_btn = gr.ClearButton([user_prompt, chatbot])
            with gr.Column(scale=1):
                submit_btn = gr.Button("Submit", variant="primary")
        with gr.Row(elem_classes="examples"):
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
                    ],
                    [
                        (
                            "Explain the importance of the Rosetta Stone in"
                            " understanding ancient languages."
                        ),
                        (
                            "The Rosetta Stone, an ancient Egyptian artifact, was key"
                            " in decoding hieroglyphs, featuring the same text in three"
                            " scripts: hieroglyphs, Demotic, and Greek."
                        ),
                    ],
                ],
                inputs=[user_prompt, knowledge_input],
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
        with gr.Row(variant="panel"):
            # wraps the explanation html to display it statically
            xai_interactive = iFrame(
                label="Static Explanation",
                value=(
                    '<div style="text-align: center"><h4>No Graphic to Display'
                    " (Yet)</h4></div>"
                ),
                show_label=True,
            )
        # row and accordion to display an explanation plot (if applicable)
        with gr.Row():
            with gr.Accordion("Token Wise Explanation Plot", open=False):
                gr.Markdown("""
                #### Plotted Values
                Values have been excluded for readability. See colorbar for value indication.
                """)
                # plot component that takes a matplotlib figure as input
                xai_plot = gr.Plot(label="Token Level Explanation")

    # functions to trigger the controller
    ## takes information for the chat and the xai selection
    ## returns prompt, history and xai data
    ## see backend/controller.py for more information
    submit_btn.click(
        interference,
        [user_prompt, chatbot, knowledge_input, system_prompt, xai_selection],
        [user_prompt, chatbot, xai_interactive, xai_plot, xai_text],
    )
    # function triggered by the enter key
    user_prompt.submit(
        interference,
        [user_prompt, chatbot, knowledge_input, system_prompt, xai_selection],
        [user_prompt, chatbot, xai_interactive, xai_plot, xai_text],
    )

    # final row to show legal information
    ## - credits, data protection and link to the License
    with gr.Tab(label="About"):
        gr.Markdown(value=load_md("public/about.md"))
        with gr.Accordion(label="Credits, Data Protection, License"):
            gr.Markdown(value=load_md("public/credits_dataprotection_license.md"))

# mount function for fastAPI Application
app = gr.mount_gradio_app(app, ui, path="/")

# launch function using uvicorn to launch the fastAPI application
if __name__ == "__main__":

    # use standard gradio launch option for hgf spaces
    if os.environ["HOSTING"].lower() == "spaces":
        ui.launch(auth=("htw", "berlin@123"))

    # otherwise run the application on port 8080 in reload mode
    ## for local development, uses Docker for Prod deployment
    run("main:app", port=8080, reload=True)
