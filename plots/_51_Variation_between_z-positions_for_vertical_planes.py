"""
Create figure 51 "Variation between z-positions for vertical planes"

Compare the distributions measured error at different z-levels.

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
sns.boxplot(ax=axs[0], data=df, y='error', x='z_pos', palette='colorblind')

# Set label for the x-axis
axs[0].set_xlabel("Z-position", fontsize=medium)


## PLOT 2
# Kernel density estimation for second frame
sns.kdeplot(ax=axs[1], data=df, y='error', hue='z_pos', fill=True, alpha=.3, palette='colorblind', legend=True)

# Set the label for the x-axis
axs[1].set_xlabel("Density", fontsize=medium)

# Set legend title
leg = axs[1].get_legend()
leg.set_title("Z-position")


# Define parameters common to both panels
for ax in axs:
    # Set label for y-axis
    ax.set_ylabel("Error [mm]", fontsize=medium)
    
    # Set the label size for both axes
    ax.tick_params(labelsize=small)
    
    # Set the limits of the y-axis
    ax.set_ylim(ymin=0, ymax=0.45)


# Save figure
plt.savefig("51.1_Variation_between_z-positions_for_vertical_planes.jpeg", dpi=600, bbox_inches='tight')
plt.savefig("51.1_Variation_between_z-positions_for_vertical_planes.pdf",  bbox_inches='tight')