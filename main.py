# main application file initializing the gradio based ui and calling other modules

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "./components/testinghtml/dist/gradio_testinghtml-0.0.1-py3-none-any.whl"])

from gradio_testinghtml import testingHTML

# external package imports
import gradio as gr
import markdown
from fastapi import FastAPI

# internal imports
from backend.controller import interference

# Global Variables
app = FastAPI()

# different functions to provide frontend abilities

# function to load markdown files
def load_md(path):
    # credit: official python-markdown documentation (https://python-markdown.github.io/reference/)
    with open(path, "r") as file:
        text = file.read()
    return markdown.markdown(text)

# function to display the system prompt info
def system_prompt_info(sys_prompt_txt):
    gr.Info(f"The system prompt was set to:\n {sys_prompt_txt}")

# function to display the xai info
def xai_info(xai_radio):
    if xai_radio != "None":
        gr.Info(f"The XAI was set to:\n {xai_radio}")
    else:
        gr.Info(f"No XAI method was selected.")

# function to display the model info
def model_info(model_radio):
    gr.Info(f"The model was set to:\n {model_radio}")


# ui interface based on Gradio Blocks (see documentation: https://www.gradio.app/docs/interface)
with gr.Blocks() as ui:
    # header row with markdown based text
    with gr.Row():
        gr.Markdown(
            """
            # Thesis Demo - AI Chat Application with XAI
            ### Select between tabs below for the different views.
            """)
    # ChatBot tab used to chat with the AI chatbot
    with gr.Tab("AI ChatBot"):
        with gr.Row():
            gr.Markdown(
                """
                ### ChatBot Demo
                Chat with the AI ChatBot using the textbox below. Manipulate the settings in the row above, including the selection of the model, the system prompt and the XAI method.
                """)
        # row with textbox to enter the system prompt, which is handed over to the model at every turn
        with gr.Row(equal_height=True):
            with gr.Column(scale=3):
                system_prompt = gr.Textbox(label="System Prompt",info= "Set the models system prompt, dictating how it answers.", placeholder="You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.")
            with gr.Column(scale=1):
                model = gr.Radio(["Mistral", "Llama 2"], label="Model Selection", info="Select Model to use for chat.", value="Mistral", interactive=True, show_label=True)
            with gr.Column(scale=1):
                xai = gr.Radio(["None", "SHAP", "Visualizer"], label="XAI Settings", info="XAI Functionalities to use.", value="None", interactive=True, show_label=True)

            # calling info functions on inputs for different settings
            system_prompt.submit(system_prompt_info, [system_prompt])
            model.input(model_info, [model])
            xai.input(xai_info, [xai])

        # row with chatbot ui displaying "conversation" with the model (see documentation: https://www.gradio.app/docs/chatbot)
        with gr.Row():
            chatbot = gr.Chatbot(layout="panel", show_copy_button=True,avatar_images=("./public/human.jpg","./public/bot.jpg"))
        # row with input textbox
        with gr.Row():
                user_prompt = gr.Textbox(label="Input Message")
        # row with columns for buttons to submit and clear content
        with gr.Row():
            with gr.Column(scale=1):
                # default clear button which clearn the given components (see documentation: https://www.gradio.app/docs/clearbutton)
                clear_btn = gr.ClearButton([user_prompt, chatbot])
            with gr.Column(scale=1):
                submit_btn = gr.Button("Submit", variant="primary")

        # two functions performing the same action (triggered the model response), when the button is used or the textbox submit function is used (clicking enter).
        # hands over the information needed for the chat (prompt, history, and system prompt) and the information needed to call the right model and xai function (model, xai)
        # returns the prompt and history to be displayed in the chatbot ui
        submit_btn.click(interference, [user_prompt, chatbot, system_prompt, model, xai], [user_prompt, chatbot])
        user_prompt.submit(interference, [user_prompt, chatbot, system_prompt, model, xai], [user_prompt, chatbot])

    # explanations tab used to provide explanations for a specific conversation
    with gr.Tab("Explanations"):
        with gr.Row():
            gr.Markdown(
                """
                ### Get Explanations for Conversations
                Using your selected XAI method, you can get explanations for the conversation you had with the AI ChatBot. The explanations are based on the last message you sent to the AI ChatBot.
                """)
        with gr.Row():
            gr.HTML(load_md("public/explanations.md"))
        with gr.Row():
            with gr.Accordion("Full Size Plot of All SHAP Values", open=False):
                gr.Plot(label="SHAP Values Plot")


    # final row to show legal information - credits, data protection and link to the LICENSE on GitHub
    with gr.Row():
        with gr.Accordion("Credits, Data Protection and License", open=False):
            gr.Markdown(value=load_md("public/credits_dataprotection_license.md"))

# mount function for fastAPI Application
app = gr.mount_gradio_app(app, ui, path="/")

# launch function using uvicorn to launch the fastAPI application
if __name__ == "__main__":
    from uvicorn import run
    run("main:app", port=8080, reload=True)