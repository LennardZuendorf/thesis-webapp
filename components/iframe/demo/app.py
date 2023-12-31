import gradio as gr
from gradio_iframe import iframe


example = iframe().example_inputs()

with gr.Blocks() as demo:
    with gr.Row():
        iframe(label="Blank")  # blank component
        iframe(value=example, label="Populated")  # populated component


demo.launch()
