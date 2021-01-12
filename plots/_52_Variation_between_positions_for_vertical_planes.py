"""
Create figure 52 "Variation between positions for vertical planes"

Create boxplots to compare x- and y-positions against z-levels.

Only consider the vertical planes (HX planes 2 and 5) for valid comparison.

"""

## Import packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


## Prepare data
# Load pickled data
df = pd.read_pickle(os.path.join('..', 'data', 'prep_data.pkl'))
layout = pd.read_pickle(os.path.join('..', 'data', 'layout_data.pkl'))

# Specify characteristics
chars = ['Flatness_HX2_Plane2',\
        'Flatness_HX2_Plane5']

# Initialize empty list for characteristics
char_list = []

# Populate char_list with the dataframes:
for i in range(len(chars)):
    # Calculate the mean value of repeated measurements and remove redundant columns
    temp = df[df['char_name'] == chars[i]].groupby('part_name').mean()\
    .drop(['rep', 'actual', 'nominal', 'char_number'], axis = 1).join(layout)

    # Add the temporary dataframe to the characteristics list
    char_list.append(temp)

# Merge the dataframes into a single one
df = pd.concat(char_list)


## Define parameters for figure
# Definition for font size
large = 24
medium = 18
small = 14
x_small = 12

# Define font
pfont = {'fontname':'Palatino Linotype'}


## Create figure
# Seaborn theme
sns.set_theme(context='paper', style='whitegrid', font_scale=1.2)

# Initialize figure
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15,7.5))

# Configure layout spacing
fig.tight_layout(pad=8.0)


## PLOT 1
# Boxplot for the first frame
sns.boxplot(ax=axs[0], data=df, y='error', x='x_pos', hue='z_pos', palette='colorblind')

# Set label for the x-axis
axs[0].set_xlabel("X-position", fontsize=medium)

# Add letter below plot
plt.text(x=0.5, y=-0.2, s="(a)", fontsize=large, weight='bold', **pfont,
         horizontalalignment='center',
         verticalalignment='center',
         transform=axs[0].transAxes)


## PLOT 2
# Boxplot for the second frame
sns.boxplot(ax=axs[1], data=df, y='error', x='y_pos', hue='z_pos', palette='colorblind')

# Set the label for the x-axis
axs[1].set_xlabel("Y-position", fontsize=medium)

# Add letter below plot
plt.text(x=0.5, y=-0.2, s="(b)", fontsize=large, weight='bold', **pfont,
         horizontalalignment='center',
         verticalalignment='center',
         transform=axs[1].transAxes)


# Define parameters common to both panels
for ax in axs:
    # Set label for y-axis
    ax.set_ylabel("Measured error [mm]", fontsize=medium)
    
    # Set the label size for both axes
    ax.tick_params(labelsize=small)
    
    # Set legend
    ax.legend(loc='upper right', title="Z-level", title_fontsize=medium, fontsize=small, fancybox=True, markerscale=2)


# Save figure
plt.savefig("52.0_Variation_between_positions_for_vertical_planes.jpg", dpi=300, bbox_inches='tight')