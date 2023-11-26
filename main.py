from fastapi import FastAPI
import gradio as gr
import app as gradio_app

app = FastAPI()

app = gr.mount_gradio_app(app, gradio_app.ui, path="/")