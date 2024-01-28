# formatting util module providing formatting functions for the model input and output

# external imports
import re
import numpy as np
from numpy import ndarray


# function to format the model reponse nicely
# takes a list of strings and returnings a combined string
def format_output_text(output: list):

    # remove special tokens from list using other function
    formatted_output = format_tokens(output)

    # start string with first list item if it is not empty
    if formatted_output[0] != "":
        output_str = formatted_output[0]
    else:
        # alternatively start with second list item
        output_str = formatted_output[1]

    # add all other list items with a space in between
    for txt in formatted_output[1:]:
        # check if the token is a punctuation mark
        if txt in [".", ",", "!", "?"]:
            # add punctuation mark without space
            output_str += txt
        # add token with space if not empty
        elif txt != "":
            output_str += " " + txt

    # return the combined string with multiple spaces removed
    return re.sub(" +", " ", output_str)


# format the tokens by removing special tokens and special characters
def format_tokens(tokens: list):
    # define special tokens to remove
    special_tokens = ["[CLS]", "[SEP]", "[PAD]", "[UNK]", "[MASK]", "▁", "Ġ", "</w>"]

    # initialize empty list
    updated_tokens = []

    # loop through tokens
    for t in tokens:
        # remove special token from start of token if found
        if t.startswith("▁"):
            t = t.lstrip("▁")

        # loop through special tokens list and remove from current token if matched
        for s in special_tokens:
            t = t.replace(s, "")

        # add token to list
        updated_tokens.append(t)

    # return the list of tokens
    return updated_tokens


# function to flatten shap values into a 2d list by summing them up
def flatten_attribution(values: ndarray, axis: int = 0):
    return np.sum(values, axis=axis)


# function to flatten values into a 2d list by averaging the attention values
def flatten_attention(values: ndarray, axis: int = 0):
    return np.mean(values, axis=axis)


# function to get averaged decoder attention from attention values
def avg_attention(attention_values):
    attention = attention_values.decoder_attentions[0][0].detach().numpy()
    return np.mean(attention, axis=0)
