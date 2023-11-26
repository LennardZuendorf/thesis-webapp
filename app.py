# main application file initializing the gradio based ui and calling other modules

# external package imports
import gradio as gr
import markdown


# internal imports
from model import mistral
from explanation import interpret as shap


# function to load md files in pthon as a string
def load_md(path):

    # credit: official python-markdown documentation (https://python-markdown.github.io/reference/)
    with open(path, "r") as file:
        text = file.read()

    # return markdown as a string
    return markdown.markdown(text)

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
                Mitral AI 7B Model fine-tuned for instruction and fully open source (see at [HGF](https://huggingface.co/mistralai/Mistral-7B-v0.1))
                """)
        # row with chatbot ui displaying "conversation" with the model (see documentation: https://www.gradio.app/docs/chatbot)
        with gr.Row():
            chatbot = gr.Chatbot(layout="panel", show_copy_button=True,avatar_images=("./public/human.jpg","./public/bot.jpg"))
        # disclaimer information row - data is recorded for shap dashboard and model explanability
        with gr.Row():
            gr.Markdown(
                """
                ##### ⚠️ All Conversations are recorded for qa assurance and explanation functionality!
                """)
        # row with input textbox
        with gr.Row():
                prompt = gr.Textbox(label="Input Message")
        # row with columns for buttons to submit and clear content
        with gr.Row():
            with gr.Column(scale=1):
                # default clear button which clearn the given components (see documentation: https://www.gradio.app/docs/clearbutton)
                clear_btn = gr.ClearButton([prompt, chatbot])
            with gr.Column(scale=1):
                submit_btn = gr.Button("Submit")

        # two functions performing the same action (triggered the model response), when the button is used or the textbox submit function is used (clicking enter).
        submit_btn.click(mistral.chat, [prompt, chatbot], [prompt, chatbot])
        prompt.submit(mistral.chat, [prompt, chatbot], [prompt, chatbot])

    # explanations tab used to provide explanations for a specific conversation
    with gr.Tab("Explanations"):
        with gr.Row():
            gr.Markdown(
                """
                ### Get Explanations for  
                SHAP Visualization Dashboard adopted from [shapash](https://github.com/MAIF/shapash)
                """)

    # shap dashboard tab for shapash inspired dashboard
    with gr.Tab("SHAP Dashboard"):
        with gr.Row():
            gr.Markdown(
                """
                ### SHAP Dashboard
                SHAP Visualization Dashboard adopted from [shapash](https://github.com/MAIF/shapash)
                """)

    # visualize dashboard to display global visualization provided by the BERTViz adoption
    with gr.Tab("Visualize Dashboard"):
        with gr.Row():
            gr.Markdown(
                """
                ### Visualization Dashboard
                Visualization Dashboard adopted from [BERTViz](https://github.com/jessevig/bertviz)
                """)

    # model overview tab for transparency
    with gr.Tab("Model Overview"):
        with gr.Tab("Mistral 7B Instruct"):
            gr.Markdown(value=load_md("./model/mistral.md"))
        with gr.Tab("LlaMa 2 7B Chat"):
            gr.Markdown(value=load_md("./model/llama2.md"))

    # final row to show legal information - credits, data protection and link to the LICENSE on GitHub
    with gr.Row():
        with gr.Accordion("Credits, Data Protection and License", open=False):
            gr.Markdown(value=load_md("./public/credits_dataprotection_license.md"))

# launch function for Gradio Interface
if __name__ == "__main__":
    ui.launch(debug=True)