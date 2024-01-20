# markup module that provides marked up text and a plot for the explanations

# external imports
import numpy as np
from numpy import ndarray

# internal imports
from utils import formatting as fmt


def markup_text(input_text: list, text_values: ndarray, variant: str):
    buckets = 10

    # Flatten the explanations values
    if variant == "shap":
        text_values = np.transpose(text_values)
    text_values = fmt.flatten_values(text_values)

    # Determine the minimum and maximum values
    min_val, max_val = np.min(text_values), np.max(text_values)

    # Separate the threshold calculation for negative and positive values
    if variant == "visualizer":
        thresholds = np.linspace(min_val, max_val, num=buckets, endpoint=False)[1:]
    else:
        neg_thresholds = np.linspace(min_val, 0, num=buckets // 2 + 1, endpoint=False)[
            1:
        ]
        pos_thresholds = np.linspace(0, max_val, num=buckets // 2 + 1)[1:]
        thresholds = np.concatenate([neg_thresholds, pos_thresholds])

    marked_text = []

    # Function to determine the bucket for a given value
    for text, value in zip(input_text, text_values):
        bucket = 0
        for i, threshold in enumerate(thresholds, start=1):
            if value > threshold:
                bucket = i
        marked_text.append((text, str(bucket)))

    return marked_text


def color_codes():
    return {
        # 1-5: Strong Light Red to Lighter Red
        "1": "#FF6666",  # Strong Light Red
        "2": "#FF8080",  # Slightly Lighter Red
        "3": "#FF9999",  # Intermediate Light Red
        "4": "#FFB3B3",  # Light Red
        "5": "#FFCCCC",  # Very Light Red
        # 6-10: Light Green to Strong Light Green
        "6": "#B3FFB3",  # Light Green
        "7": "#99FF99",  # Slightly Stronger Green
        "8": "#80FF80",  # Intermediate Green
        "9": "#66FF66",  # Strong Green
        "10": "#4DFF4D",  # Very Strong Green
    }
