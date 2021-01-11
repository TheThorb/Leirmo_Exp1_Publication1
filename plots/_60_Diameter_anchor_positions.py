"""
Create figure 60 "Diameter anchor positions"

Boxplots showing the variation in diameter of all cylinders with respect to z-height.

Only consider the 'reference specimen' rotated -90 degrees.

"""

## Import packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.patches import Patch


## Prepare data
# Load pickled data
df = pd.read_pickle(os.path.join('..', 'data', 'prep_data.pkl'))
layout = pd.read_pickle(os.path.join('..', 'data', 'layout_data.pkl'))

# Specify characteristics
chars = ['Diameter_Cyl_4mm_Pos',\
        'Diameter_Cyl_8mm_Neg',\
        'Diameter_Cyl_8mm_Pos',\
        'Diameter_Cyl_16mm_Neg',\
        'Diameter_Cyl_16mm_Pos',\
        'Diameter_Cyl_24mm_Neg',\
        'Diameter_Cyl_24mm_Pos']

# Initialize empty list for characteristics
char_list = []

# Populate char_list with the dataframes:
for i in range(len(chars)):
    # Calculate the mean value of repeated measurements and remove redundant columns
    temp = df[df['char_name'] == chars[i]].groupby('part_name').mean()\
    .drop(['rep', 'actual', 'nominal', 'char_number'], axis = 1).join(layout)

    # Isolate the specimen rotated -90 degrees
    temp = temp[temp['angle'] == -90]

    # Add the temporary dataframe to the characteristics list
    char_list.append(temp)

# Merge the dataframes into a single one
df = pd.concat(char_list)

# Extract columns of interest and converting to absolute values
df = df[['error', 'z_pos', 'y_pos']]
df['error'] = df['error'].abs()


## Define parameters for figure
# Definition for font size
large = 24
medium = 18
small = 14
x_small = 12

# Define font
pfont = {'fontname':'Palatino Linotype'}


## Plot data using seaborn module
# Seaborn theme
sns.set_theme(context='paper', style='whitegrid', font_scale=1.2)

# Define colors
colors = sns.color_palette('colorblind')

# Define the figure
fig = plt.figure(figsize=(10,7))

# Create box-plot
ax = sns.boxplot(data=df, x="z_pos", y="error", hue="y_pos", palette=colors)

# Configure axes
ax.set(xlabel='Position in z-direction', ylabel='Measured error [mm]')


## Configure legend
# Define legend elements
legend_elements = [Patch(facecolor=colors[0], label='Front-right', edgecolor='black'),
                   Patch(facecolor=colors[1], label='Rear-center', edgecolor='black')]

# Define legend with title and elements
ax.legend(title='Position in the xy-plane', loc='upper right', title_fontsize=medium, fontsize=small, fancybox=True, markerscale=8, handles=legend_elements)

# Set labels for axes
ax.set_ylabel("Measured error [mm]", fontsize=medium)
ax.set_xlabel("Z-level", fontsize=medium)

# Set label size
ax.tick_params(labelsize=small)


# Save figure
plt.savefig('60.2_Diameter_anchor_positions.jpg', dpi=300, bbox_inches='tight')