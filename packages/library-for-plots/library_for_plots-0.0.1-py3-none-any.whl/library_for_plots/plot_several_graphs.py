from .myimports import *


# Function for drawing several plots in one figure from graph list
def plot_several_graphs(graph_list):
    plt.figure(figsize=(8, 6))
    lines = []
    labels = []
    for graph in graph_list:
        if len(graph) >= 6:
            legend = graph[5]
        else:
            legend = None
        line, = plt.plot(graph[0], graph[1], lw=2, label=legend)
        lines.append(line)
        labels.append(legend)
    if len(graph_list) > 1 and any(legend is not None for legend in labels):
        plt.legend(loc='upper right', fontsize=LABEL_FONT['fontsize'])
    plt.title("Несколько графиков", **TITLE_FONT)
    plt.xlabel(graph_list[0][3], **LABEL_FONT)
    plt.ylabel(graph_list[0][4], **LABEL_FONT)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
