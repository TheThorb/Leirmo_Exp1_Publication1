
"""
Module of functions for standardized plotting of data

Created by Torbjørn L. Leirmo


Contents:
    p_val_heat_map(ax, df)                      # Create heatmap for p-values

"""

# Import libraries

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

##############################################################################

def p_val_heat_map(ax, df):
    """
    Create a heatmap from a dataframe of p-values.

    Arguments:
        ax = an axis-object (empty)
        df = dataframe of p-values (see my_functions.py)

    Return:
        ax = the axis-object now with the plot

    """

    # Replace NA-values with ones and multiply show percent
    df.fillna(1, inplace=True)
    df = df.applymap(lambda x: x*100)

    # Set labels for all ticks
    x_labels = df.columns
    y_labels = df.index

    # Set colormap-palette
    cmap = "RdYlGn"

    # Initialize figure
    im = ax.imshow(df, cmap=cmap, vmin=0, vmax=100)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("P-value", rotation=-90, va="bottom", fontsize=15)

    # Show all ticks
    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_yticks(np.arange(len(y_labels)))

    # Label ticks according to table
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)

    # Loop over data dimensions and create text annotations
    for i in range(len(x_labels)):
        for j in range(len(y_labels)):
            ax.text(j, i, "{:.2f} %".format(df.iloc[i,j]),
                   ha="center", va="center", color="black")

    # Remove a potential grid
    ax.grid(False)

    # Return the axis-object containing the plot
    return ax