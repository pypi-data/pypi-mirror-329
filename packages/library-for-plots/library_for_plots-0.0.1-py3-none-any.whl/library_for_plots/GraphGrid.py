from .myimports import *
from .get_subplot_label import get_subplot_label


# Class for drawing graph grid
class GraphGrid:
    def __init__(self, nrows, ncols, output_file=None):
        self.nrows = nrows
        self.ncols = ncols
        self.output_file = output_file
        self.fig, self.axes = plt.subplots(nrows, ncols, figsize=(ncols * 5, nrows * 4))
        self.current_index = 0
        # Приведение набора осей к плоскому массиву
        if nrows * ncols == 1:
            self.axes = [self.axes]
        else:
            self.axes = np.array(self.axes).flatten()
        # Обеспечиваем корректные отступы между графиками, чтобы текст не пересекался
        plt.subplots_adjust(wspace=0.3, hspace=0.4)
        
    def add_graph(self, x, y, title, xlabel, ylabel, legend_label=None):
        if self.current_index >= self.nrows * self.ncols:
            raise IndexError("Все ячейки сетки уже заняты!")
        ax = self.axes[self.current_index]
        ax.plot(x, y, lw=2, label=legend_label)
        # Если есть легенда, размещаем её так, чтобы она не перекрывала данные
        if legend_label is not None:
            ax.legend(loc='upper right', fontsize=LABEL_FONT['fontsize'])
        # Добавляем подпись (номер подплота) в углу графика
        subplot_label = get_subplot_label(self.current_index)
        ax.text(0.03, 0.97, f"{subplot_label}" , transform=ax.transAxes,
                fontsize=LABEL_FONT['fontsize'], verticalalignment='top')
        ax.set_title(title, **TITLE_FONT)
        ax.set_xlabel(xlabel, **LABEL_FONT)
        ax.set_ylabel(ylabel, **LABEL_FONT)
        ax.grid(True)
        self.current_index += 1

    def show(self):
        plt.tight_layout()
        if self.output_file:
            plt.savefig(self.output_file)
            print(f"Результат сохранён в файл: {self.output_file}")
        else:
            plt.show()
