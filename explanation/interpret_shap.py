# interpret module that implements the interpretability method
# external imports
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from shap import models, maskers, plots, PartitionExplainer
import torch

# internal imports
from utils import formatting as fmt
from .markup import markup_text

# global variables
TEACHER_FORCING = None
TEXT_MASKER = None


# main explain function that returns a chat with explanations
def chat_explained(model, prompt):
    model.set_config()

    # create the shap explainer
    shap_explainer = PartitionExplainer(model.MODEL, model.TOKENIZER)
    # get the shap values for the prompt
    shap_values = shap_explainer([prompt])

    # create the explanation graphic and plot
    graphic = create_graphic(shap_values)
    marked_text = markup_text(
        shap_values.data[0], shap_values.values[0], variant="shap"
    )

    # create the response text
    response_text = fmt.format_output_text(shap_values.output_names)
    return response_text, graphic, marked_text


def wrap_shap(model):
    global TEXT_MASKER, TEACHER_FORCING

    # set the device to cuda if gpu is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # updating the model settings again
    model.set_config()

    # (re)initialize the shap models and masker
    text_generation = models.TextGeneration(model.MODEL, model.TOKENIZER)
    TEACHER_FORCING = models.TeacherForcing(
        text_generation,
        model.TOKENIZER,
        device=str(device),
        similarity_model=model.MODEL,
        similarity_tokenizer=model.TOKENIZER,
    )
    TEXT_MASKER = maskers.Text(model.TOKENIZER, " ", collapse_mask_token=True)


# graphic plotting function that creates a html graphic (as string) for the explanation
def create_graphic(shap_values):
    # create the html graphic using shap text plot function
    graphic_html = plots.text(shap_values, display=False)

    # return the html graphic as string
    return str(graphic_html)