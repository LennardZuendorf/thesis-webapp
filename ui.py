import gradio as gr
import chatmodel as chat
import interpret as shap
import visualize as viz

with gr.Blocks() as ui:
    with gr.Row():
        gr.Markdown(
            """
            # Thesis Demo - AI Chat Application with XAI
            Select between tabs below for the different views.
            """)
    with gr.Tab("LlaMa 2 ChatBot"):
        with gr.Row():
            gr.Markdown(
                """
                ### ChatBot Demo
                #### Standard LlaMa 2 7B Model fine-tuned for chat and transformed to huggingface format.
                """)
        with gr.Row():
            gr.ChatInterface(chat.interference)

    with gr.Tab("SHAP Backend"):
        with gr.Row():
            gr.Markdown(
                """
                ### SHAP Dashboard
                #### SHAP Visualization Dashboard adopted from shapash
                """)

    with gr.Tab("LlaMa 2 Model Overview"):
        with gr.Row():
            gr.Markdown(
                """
                ### LlaMa 2 Model Overview for Transparency
                """)


if __name__ == "__main__":
    ui.launch(debug=True)