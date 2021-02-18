"""
Create figure 04 "Slice distribution all builds"

Line plot showing the slice distribution of all builds in a single figure

"""

## Import packages
import os
import pandas as pd
import seaborn as sns
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

# Convert to cm²
for i in [1, 2, 3]: df['Build {}'.format(i)] = df['Build {}'.format(i)] / 100

# Set the height as index
df.set_index('Height (mm)', inplace=True)


## Define parameters for figure
# Definition for font size
large = 24
medium = 18
small = 14
x_small = 12


## Plot data using matplotlib
# Seaborn theme
sns.set_theme(context='paper', style='whitegrid', font_scale=1.2)

# Define colors
colors = sns.color_palette('colorblind')

# Define the figure
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 8))

# Create the lineplot
for i in range(len(df.columns)):
    plt.plot(df.iloc[:,i], color=colors[i])


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
ax.set_xlabel("Height\n[mm]", fontsize=medium, labelpad=10, rotation='horizontal')
ax.set_ylabel("Slice area\n[cm²]", fontsize=medium, labelpad=10)

# Set label size
ax.tick_params(labelsize=small, bottom=True)

# Define the bounds of the axes
ax.set_xbound(lower=0, upper=500)
ax.set_ybound(lower=0)

# Set ticks for every 50 mm height
ax.set_xticks(list(range(0, 501, 50)))

# Set grid lines for the y-axis
ax.grid(b=True, axis='both')


# Save figure
plt.savefig('04.2_Slice_distribution_all_builds.jpeg', dpi=600, bbox_inches='tight')
plt.savefig('04.2_Slice_distribution_all_builds.pdf', bbox_inches='tight')