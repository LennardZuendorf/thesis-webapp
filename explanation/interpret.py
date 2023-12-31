# interpret module that implements the interpretability method
# external imports
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from shap import plots, PartitionExplainer

# internal imports
from utils import formatting as fmt


# main explain function that returns a chat with explanations
def chat_explained(model, prompt):
    model.set_config()

    # create the shap explainer
    shap_explainer = PartitionExplainer(model.MODEL, model.TOKENIZER)
    # get the shap values for the prompt
    shap_values = shap_explainer([prompt])

    # create the explanation graphic and plot
    graphic = create_graphic(shap_values)
    plot = create_plot(shap_values)

    # create the response text
    response_text = fmt.format_output_text(shap_values.output_names)
    return response_text, graphic, plot


# graphic plotting function that creates a html graphic (as string) for the explanation
def create_graphic(shap_values):
    # create the html graphic using shap text plot function
    graphic_html = plots.text(shap_values, display=False)

    # return the html graphic as string
    return str(graphic_html)


# plotting function that creates a heatmap style explanation plot
def create_plot(shap_values):
    values = shap_values.values[0]
    output_names = shap_values.output_names
    input_names = shap_values.data[0]

    # Set seaborn style to dark
    sns.set(style="white")
    fig, ax = plt.subplots()

    # Setting figure size
    fig.set_size_inches(
        max(values.shape[1] * 2, 10),
        max(values.shape[0] * 1, 5),
    )

    # Plotting the heatmap with Seaborn's color palette
    im = ax.imshow(
        values,
        vmax=values.max(),
        vmin=values.min(),
        cmap=sns.color_palette("vlag_r", as_cmap=True),
        aspect="auto",
    )

    # Creating colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Token Attribution", rotation=-90, va="bottom")
    cbar.ax.yaxis.set_tick_params(color="black")
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="black")

    # Setting ticks and labels with white color for visibility
    ax.set_yticks(np.arange(len(input_names)), labels=input_names)
    ax.set_xticks(np.arange(len(output_names)), labels=output_names)
    plt.setp(ax.get_xticklabels(), color="black", rotation=45, ha="right")
    plt.setp(ax.get_yticklabels(), color="black")

    # Adjusting tick labels
    ax.tick_params(
        top=True, bottom=False, labeltop=False, labelbottom=True, color="white"
    )

    # Adding text annotations with appropriate contrast
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            val = values[i, j]
            color = "white" if im.norm(values.max()) / 2 > im.norm(val) else "black"
            ax.text(j, i, f"{val:.4f}", ha="center", va="center", color=color)

    return plt
