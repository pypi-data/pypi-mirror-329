from .myimports import *
from .GraphGrid import *

def example_metal_diffusion():
    # Дано: A = 10^-4, H = 10^3
    A = 1e-4
    H = 1e3

    # Пример: вариант 1 для металлов "Медь" и "Железо" при t = 0.001c; t = 0.1c; t = 1c
    metals = {
        "Медь": {"Cp": 3.45e6, "D": 1.11e-4},    # Cp в Дж/(м^3·°C), D в м^2/с
        "Железо": {"Cp": 3.0e6, "D": 2.3e-5}
    }
    times = [0.001, 0.1, 1]  # секунды
    x = np.linspace(-0.1, 0.1, 500)  # диапазон по x, м

    # Создаём сетку 2 (металла) x 3 (времени)
    grid = GraphGrid(nrows=2, ncols=3)
    for i, metal in enumerate(metals.keys()):
        CP = metals[metal]["Cp"]
        D = metals[metal]["D"]
        for j, t in enumerate(times):
            coeff = H / (CP * A) * (1 / np.sqrt(D * t)) / np.sqrt(4 * np.pi)
            y = coeff * np.exp(- x**2 / (4 * D * t))
            title = fr"{metal}: распределение $\theta/\theta_0$ при $t = {t}\,c$"
            xlabel = r"$x, \,м$"
            ylabel = r"$\theta/\theta_0$"
            grid.add_graph(x, y, title, xlabel, ylabel)
    grid.show()
