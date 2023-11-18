import gradio as gr
from transformers import pipeline

gbert_pipeline = pipeline("text-classification", model="LennardZuendorf/bert-base-german-cased", top_k=None, token="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")
leolm_pipeline = pipeline("text-classification", model="LennardZuendorf/interpretor", top_k=None, token="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")
chat_pipeline = pipeline("conversational", model="meta-llama/Llama-2-7b-chat-hf", top_k=None, token="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")

with gr.Blocks() as ui:
    with gr.Row():
        gr.Markdown(
            """
            # Thesis Model Demos
            Select between tabs below for try the different models.
            """)
    with gr.Tab("GBERT HateSpeech Detection"):
        with gr.Row():
            gr.Markdown(
                """
                ### GBERT (German Language BERT by Deepset) Demo
                #### Model finetuned on German Hate Speech dataset (~3,5k sequences)
                """)
        with gr.Row():
            gr.Interface.from_pipeline(gbert_pipeline)

    with gr.Tab("LeoLM HateSpeech Detection"):
        with gr.Row():
            gr.Markdown(
                """
                ### LeoLM (German Language FineTuned LlaMa2 Model) Demo
                #### Model finetuned on German Hate Speech dataset (~3,5k sequences)
                """)
        with gr.Row():
            gr.Button("New Tiger")

    with gr.Tab("Chat Model Interface"):
        with gr.Row():
            gr.Markdown(
                """
                ### LlaMa 2 Chat Demo
                """)
        with gr.Row():
            gr.Interface.from_pipeline(chat_pipeline)

if __name__ == "__main__":
    ui.launch()