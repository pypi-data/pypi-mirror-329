from .myimports import *

# Function for drawing one plot
def plot_graph(x, y, title, xlabel, ylabel, legend_label=None):
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, lw=2, label=legend_label)
    if legend_label is not None:
        # Легенда размещается так, чтобы не перекрывать данные (верхний правый угол)
        plt.legend(loc='upper right', fontsize=LABEL_FONT['fontsize'])
    plt.title(title, **TITLE_FONT)
    plt.xlabel(xlabel, **LABEL_FONT)
    plt.ylabel(ylabel, **LABEL_FONT)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
