# plotting functions

# external imports
import numpy as np
import matplotlib.pyplot as plt


def plot_seq(seq_values: list, method: str = ""):

    # Separate the tokens and their corresponding importance values
    tokens, importance = zip(*seq_values)

    # Convert importance values to numpy array for conditional coloring
    importance = np.array(importance)

    # Determine the colors based on the sign of the importance values
    colors = ["#ff0051" if val > 0 else "#008bfb" for val in importance]

    # Create a bar plot
    plt.figure(figsize=(len(tokens) * 0.9, np.max(importance)))
    x_positions = range(len(tokens))  # Positions for the bars

    # Creating vertical bar plot
    bar_width = 0.8
    plt.bar(x_positions, importance, color=colors, align="center", width=bar_width)

    # Annotating each bar with its value
    padding = 0.1  # Padding for text annotation
    for x, (y, color) in enumerate(zip(importance, colors)):
        sign = "+" if y > 0 else ""
        plt.annotate(
            f"{sign}{y:.2f}",  # Format the value with sign
            xy=(x, y + padding if y > 0 else y - padding),
            ha="center",
            color=color,
            va="bottom" if y > 0 else "top",  # Vertical alignment
            fontweight="bold",  # Bold text
            bbox={
                "facecolor": "white",
                "edgecolor": "none",
                "boxstyle": "round,pad=0.1",
            },  # White background
        )

    plt.axhline(0, color="black", linewidth=1)
    plt.title(f"Input Token Attribution with {method}")
    plt.xlabel("Input Tokens", labelpad=0.5)
    plt.ylabel("Attribution")
    plt.xticks(x_positions, tokens, rotation=45)

    # Adjust y-axis limits to ensure there's enough space for labels
    y_min, y_max = plt.ylim()
    y_range = y_max - y_min
    plt.ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)

    return plt
