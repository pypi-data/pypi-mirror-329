from .myimports import *


# Function for drawing plots from file
def plot_from_file(filename, col_x, col_y, title, xlabel, ylabel, delimiter=None):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File{filename} is not found!")
    data = np.loadtxt(filename, delimiter=delimiter)
    # Приведение номеров колонок к индексам Python.
    x = data[:, col_x - 1]
    y = data[:, col_y - 1]
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, lw=2)
    plt.title(title, **TITLE_FONT)
    plt.xlabel(xlabel, **LABEL_FONT)
    plt.ylabel(ylabel, **LABEL_FONT)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
