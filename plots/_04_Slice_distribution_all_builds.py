"""
Create figure 04 "Slice distribution all builds"

Line plot showing the slice distribution of all builds in a single figure

"""

## Import packages
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import transforms
from matplotlib.lines import Line2D


## Prepare data
# Load the slice distribution of each build from CSV-files
df_b1 = pd.read_csv(os.path.join('..', 'data', 'Slice_distribution_build1.csv'), sep=';')
df_b2 = pd.read_csv(os.path.join('..', 'data', 'Slice_distribution_build2.csv'), sep=';')
df_b3 = pd.read_csv(os.path.join('..', 'data', 'Slice_distribution_build3.csv'), sep=';')

# Use the first build as a foundation for common dataframe
df = df_b1.rename(columns={"Total slice surface (mmý)": "Build 1"})

# Add the other two build to the common dataframe
df.insert(2, "Build 2", df_b2['Total slice surface (mmý)'])
df.insert(3, "Build 3", df_b3['Total slice surface (mmý)'])

# Convert height to negative numbers
# (this will be reverted later during transform)
df['Height (mm)'] = -df['Height (mm)']

# Set the height as index
df.set_index('Height (mm)', inplace=True)


## Define parameters for figure
# Definition for font size
large = 24
medium = 18
small = 14
x_small = 12

# Define colors
colors = ['tab:blue', 'tab:orange', 'tab:green']


## Plot data using matplotlib
# Define the figure
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))

# Define transformation parameters for plotting data
base = plt.gca().transData
rot = transforms.Affine2D().rotate_deg(-90)

# Create the lineplot
for i in range(len(df.columns)):
    plt.plot(df.iloc[:,i], color=colors[i], transform=rot + base)


## Configure legend
# Initiate list of legend elements
legend_elements = []

# Define legend elements and add to list
for i in range(len(df.columns)):
    legend_elements.append(Line2D([0], [0], color=colors[i], lw=4, label=i+1))

# Create legend with title and elements
ax.legend(title="Build", loc='upper right', title_fontsize=medium, fontsize=small, fancybox=True, handles=legend_elements)


## Configure axes
# Set labels for axes
ax.set_xlabel("Slice area\n[mm²]", fontsize=medium, labelpad=10)
ax.set_ylabel("Height\n[mm]", fontsize=medium, labelpad=40, rotation='horizontal')

# Set label size
ax.tick_params(labelsize=small)

# Define the bounds of the axes
ax.set_xbound(lower=0)
ax.set_ybound(lower=0, upper=500)

# Set ticks for every 50 mm height
ax.set_yticks(list(range(0, 501, 50)))

# Set grid lines for the y-axis
ax.grid(axis='y')


# Save figure
plt.savefig('04.0_Slice_distribution_all_builds.jpg', dpi=300, bbox_inches='tight')