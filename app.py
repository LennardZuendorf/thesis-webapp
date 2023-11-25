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
    with gr.Tab("Mistral AI ChatBot"):
        with gr.Row():
            gr.Markdown(
                """
                ### ChatBot Demo
                Mitral AI 7B Model fine-tuned for instruction and fully open source (see at [HGF](https://huggingface.co/mistralai/Mistral-7B-v0.1))
                """)
        with gr.Row():
            gr.ChatInterface(
                chat.interference
            )
        with gr.Row():
            gr.Slider(
                label="Temperature",
                value=0.7,
                minimum=0.0,
                maximum=1.0,
                step=0.05,
                interactive=True,
                info="Higher values produce more diverse outputs",
            ),
            gr.Slider(
                label="Max new tokens",
                value=256,
                minimum=0,
                maximum=1024,
                step=64,
                interactive=True,
                info="The maximum numbers of new tokens",
            ),
            gr.Slider(
                label="Top-p (nucleus sampling)",
                value=0.95,
                minimum=0.0,
                maximum=1,
                step=0.05,
                interactive=True,
                info="Higher values sample more low-probability tokens",
            ),
            gr.Slider(
                label="Repetition penalty",
                value=1.1,
                minimum=1.0,
                maximum=2.0,
                step=0.05,
                interactive=True,
                info="Penalize repeated tokens",
            )

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


if __name__ == "__main__":
    ui.launch(debug=True)