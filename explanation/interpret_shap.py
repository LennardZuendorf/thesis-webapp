# interpret module that implements the interpretability method

# external imports
from shap import models, maskers, plots, PartitionExplainer
import torch

# internal imports
from utils import formatting as fmt
from .markup import markup_text

# global variables
TEACHER_FORCING = None
TEXT_MASKER = None


# function to extract summarized sequence wise attribution
def extract_seq_att(shap_values):

    # extracting summed up shap values
    values = fmt.flatten_attribution(shap_values.values[0], 1)

    # returning list of tuples of token and value
    return list(zip(shap_values.data[0], values))


# function used to wrap the model with a shap model
def wrap_shap(model):
    # calling global variants
    global TEXT_MASKER, TEACHER_FORCING

    # set the device to cuda if gpu is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # updating the model settings
    model.set_config({})

    # (re)initialize the shap models and masker
    # creating a shap text_generation model
    text_generation = models.TextGeneration(model.MODEL, model.TOKENIZER)
    # wrapping the text generation model in a teacher forcing model
    TEACHER_FORCING = models.TeacherForcing(
        text_generation,
        model.TOKENIZER,
        device=str(device),
        similarity_model=model.MODEL,
        similarity_tokenizer=model.TOKENIZER,
    )
    # setting the text masker as an empty string
    TEXT_MASKER = maskers.Text(model.TOKENIZER, " ", collapse_mask_token=True)


# graphic plotting function that creates a html graphic (as string) for the explanation
def create_graphic(shap_values):

    # create the html graphic using shap text plot function
    graphic_html = plots.text(shap_values, display=False)

    # return the html graphic as string to display in iFrame
    return str(graphic_html)


# main explain function that returns a chat with explanations
def chat_explained(model, prompt):
    model.set_config({})

    # create the shap explainer
    shap_explainer = PartitionExplainer(model.MODEL, model.TOKENIZER)

    # get the shap values for the prompt
    shap_values = shap_explainer([prompt])

    # create the explanation graphic and marked text array
    graphic = create_graphic(shap_values)
    marked_text = markup_text(
        shap_values.data[0], shap_values.values[0], variant="shap"
    )

    # create the response text
    response_text = fmt.format_output_text(shap_values.output_names)

    # return response, graphic and marked_text array
    return response_text, graphic, marked_text, None
