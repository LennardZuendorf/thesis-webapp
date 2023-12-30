# formatting util module providing formatting functions for the model input and output

# external imports
import re


# function to format the model reponse nicely
def format_output_text(output: list):
    # remove special tokens from list
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
    # define special tokens to remove and initialize empty list
    special_tokens = ["[CLS]", "[SEP]", "[PAD]", "[UNK]", "[MASK]", "▁", "Ġ", "</w>"]
    updated_tokens = []

    # loop through tokens
    for t in tokens:
        # remove special token from start of token if found
        if t.startswith("▁"):
            t = t.lstrip("▁")

        # loop through special tokens and remove them if found
        for s in special_tokens:
            t = t.replace(s, "")

        # add token to list
        updated_tokens.append(t)

    # return the list of tokens
    return updated_tokens