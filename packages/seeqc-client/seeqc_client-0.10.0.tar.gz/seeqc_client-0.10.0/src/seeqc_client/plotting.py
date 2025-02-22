import os

import matplotlib as mpl
import matplotlib.image as image
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def _get_logo_path() -> str:
    """return path of Seeqc logo"""
    import seeqc_client
    path = os.path.dirname(seeqc_client.__file__)
    return path + r'\black_logo.png'


def plot(data: dict):
    """plot results histogram"""
    mpl.rcParams["font.family"] = "Consolas"
    file = _get_logo_path()
    seeqc = image.imread(file)
    names = list(data.keys())
    values = list(data.values())
    fig = plt.bar(range(len(data)), values, tick_label=names, color='black')
    ax = plt.gca()
    ax.set_facecolor("#e4e4e3")
    ax.set_ylim([0, 1])
    ax.grid(axis='y', linestyle=(0, (3, 5)))
    ax.set_axisbelow(True)
    ax.set_ylabel('Populations')
    plt.yticks(np.arange(0, 1.1, 0.1))
    imagebox = OffsetImage(seeqc, zoom=0.1, alpha=0.8)
    position = ((len(data)-1)*0.5, 0.5)  # (x, y) position, with x in the center of bars and y at the middle of the y-axis range
    ab = AnnotationBbox(imagebox, position, frameon=False, xycoords='data')
    ax.add_artist(ab)
    plt.show()
