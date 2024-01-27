# markup module that provides marked up text and a plot for the explanations

# external imports
import numpy as np
from numpy import ndarray

# internal imports
from utils import formatting as fmt


def markup_text(input_text: list, text_values: ndarray, variant: str):
    bucket_tags = ["-5", "-4", "-3", "-2", "-1", "0", "+1", "+2", "+3", "+4", "+5"]

    # Flatten the values depending on the source
    # attention is averaged, SHAP summed up
    if variant == "shap":
        text_values = np.transpose(text_values)
        text_values = fmt.flatten_attribution(text_values)
    else:
        text_values = fmt.flatten_attention(text_values)

    # Determine the minimum and maximum values
    min_val, max_val = np.min(text_values), np.max(text_values)

    # Separate the threshold calculation for negative and positive values
    if variant == "visualizer":
        neg_thresholds = np.linspace(
            0, 0, num=(len(bucket_tags) - 1) // 2 + 1, endpoint=False
        )[1:]
    else:
        neg_thresholds = np.linspace(
            min_val, 0, num=(len(bucket_tags) - 1) // 2 + 1, endpoint=False
        )[1:]
    pos_thresholds = np.linspace(0, max_val, num=(len(bucket_tags) - 1) // 2 + 1)[1:]
    thresholds = np.concatenate([neg_thresholds, [0], pos_thresholds])

    marked_text = []

    # Function to determine the bucket for a given value
    for text, value in zip(input_text, text_values):
        bucket = "-5"
        for i, threshold in zip(bucket_tags, thresholds):
            if value >= threshold:
                bucket = i
        marked_text.append((text, str(bucket)))

    return marked_text


def color_codes():
    return {
        # 1-5: Strong Light Sky Blue to Lighter Sky Blue
        "-5": "#3251a8",  # Strong Light Sky Blue
        "-4": "#5A7FB2",  # Slightly Lighter Sky Blue
        "-3": "#8198BC",  # Intermediate Sky Blue
        "-2": "#A8B1C6",  # Light Sky Blue
        "-1": "#E6F0FF",  # Very Light Sky Blue
        "0": "#FFFFFF",  # White
        "+1": "#FFE6F0",  # Lighter Pink
        "+2": "#DF8CA3",  # Slightly Stronger Pink
        "+3": "#D7708E",  # Intermediate Pink
        "+4": "#CF5480",  # Deep Pink
        "+5": "#A83273",  # Strong Magenta
    }
