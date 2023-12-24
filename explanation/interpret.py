import seaborn as sns
import matplotlib.pyplot as plt

def interpret_plot(shap_values):
    values=shap_values[0]
    input_text = shap_values.data[0]
    output_text = shap_values.output_names

    # Set the seaborn style for better aesthetics
    sns.set(style="whitegrid")
    plt.figure(figsize=(20, 10))

    # Create the heatmap with horizontal shape
    sns.heatmap(shap_values_large, cmap=color_palette, center=0, annot=False, cbar_kws={'fraction': 0.02})

    # Adjust the labels for the larger set
    plt.xticks(ticks=np.arange(len(output_text_large)) + 0.5, labels=output_text_large, rotation=90)
    plt.yticks(ticks=np.arange(len(input_text_large)) + 0.5, labels=input_text_large, rotation=0)

    plt.xlabel("Output Tokens")
    plt.ylabel("Input Tokens")

    return plt