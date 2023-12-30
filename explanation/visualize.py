# visualization module that creates an attention visualization using BERTViz

# external imports
from bertviz import head_view


# plotting function that plots the attention values in a heatmap
def chat_explained(model, prompt):
    inputs = model.TOKENIZER(prompt, return_tensors="pt")
    out = model.MODEL(**inputs, output_attentions=True)

    attention = out["attentions"]  # Retrieve attention from model outputs
    tokens = model.TOKENIZER.convert_ids_to_tokens(
        inputs["input_ids"][0]
    )  # Convert input ids to token strings

    graphic = head_view(attention, tokens)
    response_text = out[0]
    plot = None

    return response_text, graphic, plot
