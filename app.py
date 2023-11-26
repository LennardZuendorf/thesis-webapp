import gradio as gr
import mistral
import interpret as shap
import visualize as viz
import markdown

def load_md(filename):
    path = "./public/"+str(filename)

    # credit: official python-markdown documentation (https://python-markdown.github.io/reference/)
    with open(path, "r") as file:
        text = file.read()

    return markdown.markdown(text)

with gr.Blocks() as ui:
    with gr.Row():
        gr.Markdown(
            """
            # Thesis Demo - AI Chat Application with XAI
            ### Select between tabs below for the different views.
            """)
    with gr.Tab("Mistral AI ChatBot"):
        with gr.Row():
            gr.Markdown(
                """
                ### ChatBot Demo
                Mitral AI 7B Model fine-tuned for instruction and fully open source (see at [HGF](https://huggingface.co/mistralai/Mistral-7B-v0.1))
                """)

        with gr.Row():
            chatbot = gr.Chatbot(layout="panel", show_copy_button=True,avatar_images=("./public/human.jpg","./public/bot.jpg"))
        with gr.Row():
            gr.Markdown(
                """
                ##### ⚠️ All Conversations are recorded for qa assurance and explanation functionality!
                """)
        with gr.Row():
                prompt = gr.Textbox(label="Input Message")
        with gr.Row():
            with gr.Column(scale=1):
                clear_btn = gr.ClearButton([prompt, chatbot])
            with gr.Column(scale=1):
                submit_btn = gr.Button("Submit")

        submit_btn.click(mistral.chat, [prompt, chatbot], [prompt, chatbot])
        prompt.submit(mistral.chat, [prompt, chatbot], [prompt, chatbot])

    with gr.Tab("Explanations"):
        with gr.Row():
            gr.Markdown(
                """
                ### Get Explanations for  
                SHAP Visualization Dashboard adopted from [shapash](https://github.com/MAIF/shapash)
                """)


    with gr.Tab("SHAP Dashboard"):
        with gr.Row():
            gr.Markdown(
                """
                ### SHAP Dashboard
                SHAP Visualization Dashboard adopted from [shapash](https://github.com/MAIF/shapash)
                """)

    with gr.Tab("Visualize Dashboard"):
        with gr.Row():
            gr.Markdown(
                """
                ### Visualization Dashboard
                Visualization Dashboard adopted from [BERTViz](https://github.com/jessevig/bertviz)
                """)

    with gr.Tab("Mitral Model Overview"):
        with gr.Row():
            gr.Markdown(
                """
                ### Mistral 7B Model & Data Overview for Transparency
                Adopted from official [model paper](https://arxiv.org/abs/2310.06825) by Mistral AI
                """)

    with gr.Row():
        with gr.Accordion("Credits, Data Protection and License", open=False):
            gr.Markdown(value=load_md("credits_dataprotection_license.md"))

if __name__ == "__main__":
    ui.launch(debug=True)