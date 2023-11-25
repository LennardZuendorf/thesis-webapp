import gradio as gr
import chatmodel as chat
import interpret as shap
import visualize as viz

with gr.Blocks() as ui:
    with gr.Row():
        gr.Markdown(
            """
            # Thesis Demo - AI Chat Application with XAI
            ### Select between tabs below for the different views.
            """)
    with gr.Tab("LlaMa 2 ChatBot"):
        with gr.Row():
            gr.Markdown(
                """
                ### ChatBot Demo
                LlaMa 2 7B Model fine-tuned for chat and transformed to huggingface format (see at [HGF](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf))
                """)
        with gr.Row():
            gr.ChatInterface(chat.interference)

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

    with gr.Tab("LlaMa 2 Model Overview"):
        with gr.Row():
            gr.Markdown(
                """
                ### LlaMa 2 Model & Data Overview for Transparency
                Adopted from official [model paper](https://arxiv.org/abs/2307.09288) by Meta AI
                """)


if __name__ == "__main__":
    ui.launch(debug=True)