# interpret module that implements the interpretability method
# external imports
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import shap


# main explain function that returns a chat with explanations
def chat_explained(model, prompt):
    # create the shap explainer
    shap_explainer = shap.PartitionExplainer(model.MODEL, model.TOKENIZER)
    # get the shap values for the prompt
    shap_values = shap_explainer(prompt)

    # create the explanation graphic and plot
    graphic = create_graphic(shap_values)
    plot = create_plot(shap_values)

    # create the response text
    response_text = format_output_text(shap_values.output_names)
    return response_text, graphic, plot


# output text formatting function that turns the list into a string
def format_output_text(output):
    # start string with first list item
    output_str = output[0]
    # add all other list items with a space in between
    for txt in output[1:]:
        output_str += " " + txt
    # return the output string
    return output_str


# graphic plotting function that creates a html graphic (as string) for the explanation
def create_graphic(shap_values):
    # create the html graphic using shap text plot function
    graphic_html = shap.plots.text(shap_values, display=False)

    # return the html graphic as string
    return str(graphic_html)


# plotting function that creates a heatmap style explanation plot
def create_plot(shap_values):
    # setup color palette for heatmap
    color_palette = sns.color_palette("coolwarm", as_cmap=True)

    # extract values, text from shap_values
    values = shap_values[0]
    input_text = shap_values.data[0]
    output_text = shap_values.output_names

    # Set the seaborn style for better aesthetics
    sns.set(style="darkgrid")
    plt.figure(figsize=(20, 10))

    # create the heatmap with horizontal shape
    sns.heatmap(
        values,
        cmap=color_palette,
        center=0,
        annot=False,
        cbar_kws={"fraction": 0.02},
    )

    # adjusting labels and ticks
    plt.xticks(
        ticks=np.arange(len(output_text)) + 0.5,
        labels=output_text,
        rotation=90,
    )
    plt.yticks(
        ticks=np.arange(len(input_text)) + 0.5,
        labels=input_text,
        rotation=0,
    )

    # set axis labels
    plt.xlabel("Output Tokens")
    plt.ylabel("Input Tokens")
    plt.title("Token-wise SHAP Values")

    return plt
