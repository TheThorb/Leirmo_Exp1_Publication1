"""
Create figure 05 "Initial slice distribution"

Compare the slice distribution of perfect spheres versus
the main specimens of build 1.

"""

## Import packages
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import transforms


## Prepare data
# The slice distribution considering only the main specimens of build 1
df_main = pd.read_csv(os.path.join('..', 'data', 'Slice_distribution_build1_main.csv'), sep=';')

# The slice distribution considering perfect spheres in the defined positions
df_sphere = pd.read_csv(os.path.join('..', 'data', 'Slice_distribution_spheres.csv'), sep=';')

# Put dataframes in list for simple processing
dfs = [df_main, df_sphere]

# For both dataframes:
for df in dfs:   
    # Convert to cm²
    df['Total slice surface (mm²)'] = df['Total slice surface (mm²)'] / 100
        
    # Set the height as index
    df.set_index('Height (mm)', inplace=True)


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

# Define colors
colors = sns.color_palette('colorblind')

# Define the figure
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15, 8))

# Configure layout spacing
fig.tight_layout(pad=6.0)


for i in range(len(axs)):   
    # Plot the slice distributions in spearate panels of the figure
    axs[i].plot(dfs[i], linewidth=2)

    # Set label for y-axis
    axs[i].set_ylabel('Slice area [cm²]', fontsize=medium)
    
    # Set label for x-axis
    axs[i].set_xlabel('Height [mm]', fontsize=medium)
    
    # Set the label size for both axes
    axs[i].tick_params(labelsize=small, bottom=True)
    
    # Define the bounds of the axes
    axs[i].set_ybound(lower=0)
    axs[i].set_xbound(lower=0, upper=500)

    # Set ticks for every 50 mm height
    axs[i].set_xticks(list(range(0, 501, 50)))

    # Set grid lines for the y-axis
    axs[i].grid(b=True, axis='both')
    
    
# Save figure
plt.savefig('05.2_Initial_slice_distribution.jpeg', dpi=600, bbox_inches='tight')
plt.savefig('05.2_Initial_slice_distribution.pdf', bbox_inches='tight')