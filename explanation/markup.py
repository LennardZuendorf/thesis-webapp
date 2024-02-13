# markup module that provides marked up text as an array

# external imports
import numpy as np
from numpy import ndarray

# internal imports
from utils import formatting as fmt


# main function that assigns each text snipped a marked bucket
def markup_text(input_text: list, text_values: ndarray, variant: str):
    print(f"Marking up text {input_text} and {text_values} for {variant}.")

    # naming of the 11 buckets
    bucket_tags = ["-5", "-4", "-3", "-2", "-1", "0", "+1", "+2", "+3", "+4", "+5"]

    # flatten the values depending on the source
    # attention is averaged, SHAP summed up
    if variant == "shap":
        text_values = np.transpose(text_values)
        text_values = fmt.flatten_attribution(text_values)
    elif variant == "visualizer":
        text_values = fmt.flatten_attention(text_values)

    if text_values.size != len(input_text):
        raise ValueError(
            "Length of input text and attribution values do not match. "
            f"Text: {len(input_text)}, Attributions: {len(text_values)}"
        )

    # determine the minimum and maximum values
    min_val, max_val = np.min(text_values), np.max(text_values)

    # separate the threshold calculation for negative and positive values
    # visualization negative thresholds are all 0 since attention always positive
    if variant == "visualizer":
        neg_thresholds = np.linspace(
            0, 0, num=(len(bucket_tags) - 1) // 2 + 1, endpoint=False
        )[1:]
    # standard config for 5 negative buckets
    else:
        neg_thresholds = np.linspace(
            min_val, 0, num=(len(bucket_tags) - 1) // 2 + 1, endpoint=False
        )[1:]
    # creating positive thresholds between 0 and max values
    pos_thresholds = np.linspace(0, max_val, num=(len(bucket_tags) - 1) // 2 + 1)[1:]
    # combining thresholds
    thresholds = np.concatenate([neg_thresholds, [0], pos_thresholds])

    # init empty marked text list
    marked_text = []

    # looping over each text snippet and attribution value
    for text, value in zip(input_text, text_values):

        # validating text and skipping empty text/special tokens
        # if text not in fmt.SPECIAL_TOKENS:
        # setting initial bucket at lowest
        bucket = "-5"

        # looping over all bucket and their threshold
        for i, threshold in zip(bucket_tags, thresholds):
            # updating assigned bucket if value is above threshold
            if value >= threshold:
                bucket = i
        # finally adding text and bucket assignment to list of tuples
        marked_text.append((text, str(bucket)))

    # returning list of marked text snippets as list of tuples
    return marked_text


# function that defines color codes
# coloring along SHAP style coloring for consistency
def color_codes():
    return {
        # -5 to -1: Strong Light Sky Blue to Lighter Sky Blue
        # 0: white (assuming default light mode)
        # +1 to +5 light pink to strong magenta
        "-5": "#008bfb",
        "-4": "#68a1fd",
        "-3": "#96b7fe",
        "-2": "#bcceff",
        "-1": "#dee6ff",
        "0": "#ffffff",
        "+1": "#ffd9d9",
        "+2": "#ffb3b5",
        "+3": "#ff8b92",
        "+4": "#ff5c71",
        "+5": "#ff0051",
    }
