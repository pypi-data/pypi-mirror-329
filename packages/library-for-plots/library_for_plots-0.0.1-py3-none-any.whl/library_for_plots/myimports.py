import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os

# Enabling LaTeX notation and setting font to Arial
mpl.rcParams['text.usetex'] = False # False because LaTex is not installed on MEPHI's Jupyter
mpl.rcParams['font.family'] = 'Arial'

# You can set preamble for loading LaTex packages
# Example: mpl.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

TITLE_FONT = {'fontsize': 16, 'fontweight': 'bold'}  # Self-explanatory 
LABEL_FONT = {'fontsize': 14}
