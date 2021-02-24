"""
Create figure 31 "Difference between repeated measurements"

Compare the distributions of difference between repeated measurements and fit the distribtions to
probability density function (log-normal distribution)

"""

## Import packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats
from matplotlib.lines import Line2D


## Define function for retrieving the frozen distribution of the fitted probability density function
#  Valid distributions include lognorm, invgamma and powerlognorm
def calc_pdf(x, data):
    return stats.lognorm.pdf(x, *stats.lognorm.fit(data))


## Prepare data
# Create path
path = os.path.join('..', 'data', 'prep_data.pkl')

# Load data from pickle to dataframe
df = pd.read_pickle(path)

# Drop irrelevant columns
df = df[['part_name', 'rep', 'char_name', 'error', 'time', 'char_number']]

# Specify characteristics
chars = ['Cylindricity_Cyl_4mm_Pos',
            'Cylindricity_Cyl_8mm_Neg',
            'Cylindricity_Cyl_8mm_Pos',
            'Cylindricity_Cyl_16mm-Neg',
            'Cylindricity_Cyl_16mm_Pos',
            'Cylindricity_Cyl_24mm_Neg',
            'Cylindricity_Cyl_24mm_Pos',
            'Diameter_Cyl_4mm_Pos',
            'Diameter_Cyl_8mm_Neg',
            'Diameter_Cyl_8mm_Pos',
            'Diameter_Cyl_16mm_Neg',
            'Diameter_Cyl_16mm_Pos',
            'Diameter_Cyl_24mm_Neg',
            'Diameter_Cyl_24mm_Pos',
            'Flatness_HX1_Plane1',
            'Flatness_HX1_Plane2',
            'Flatness_HX1_Plane3',
            'Flatness_HX1_Plane4',
            'Flatness_HX1_Plane5',
            'Flatness_HX1_Plane6',
            'Flatness_HX2_Plane1',
            'Flatness_HX2_Plane2',
            'Flatness_HX2_Plane3',
            'Flatness_HX2_Plane4',
            'Flatness_HX2_Plane5',
            'Flatness_HX2_Plane6']

# Define list of strings to simplify column selection
reps = ['rep1', 'rep2', 'rep3']

# Extract specified characteristics
df_s = df[df['char_name'].isin(chars)]


## Restructuring to have repeated measurements as columns
# Split repeated measurements into separate dataframes
df_r1 = df_s[df_s['rep'] == 1]
df_r2 = df_s[df_s['rep'] == 2]
df_r3 = df_s[df_s['rep'] == 3]

# Sort rows and rename columns to ensure aligned data after merge
df_r1 = df_r1.set_index('part_name').sort_values(by='time').rename(columns={'error': 'rep1', 'char_name': 'char_type'})
df_r2 = df_r2.set_index('part_name').sort_values(by='time').rename(columns={'error': 'rep2', 'char_name': 'char_type'})
df_r3 = df_r3.set_index('part_name').sort_values(by='time').rename(columns={'error': 'rep3', 'char_name': 'char_type'})

# Merge the dataframes (with the different repetitions)
df_tot = pd.concat([df_r1, df_r2['rep2'], df_r3['rep3']], axis=1)

# Drop redundant columns and reset index
df_tot = df_tot[['char_type', 'rep1', 'rep2', 'rep3']].reset_index()

# Replace exact characteristic name with simply characteristic type
df_tot.loc[df_tot['char_type'].str.startswith('Cylindricity'), 'char_type'] = 'Cylindricity'
df_tot.loc[df_tot['char_type'].str.startswith('Flatness'), 'char_type'] = 'Flatness'
df_tot.loc[df_tot['char_type'].str.startswith('Diameter'), 'char_type'] = 'Diameter'

# Calculate difference between minimum and maximum
df_tot['diff'] = df_tot[reps].max(axis=1) - df_tot[reps].min(axis=1)


## Define parameters for figure
# Range for x-axis
xr = 0.05

# Array for x-axis
x = np.linspace(0, xr, 1000)

# Number of bins for histograms
b = 150

# Transperency for histograms
a = 0.5

# Define colors
colors = sns.color_palette('colorblind')

# Define the characteristics
chars = ["Cylindricity", "Diameter", "Flatness"]

# Definition for font size
large = 24
medium = 18
small = 14
x_small = 12


## Create figure
# Seaborn theme
sns.set_theme(context='paper', style='whitegrid')

# Initialize a figure with subplots
fig, axs = plt.subplots(nrows=5, ncols=1, figsize=(15, 20), sharex=True)

# Initialize legend
legend_elements = []


## Single characteristics
# Iterate all characteristics and plot them seperately
for char, i in zip(chars, range(3)):
    # Create histogram for the characteristic
    sns.histplot(df_tot.loc[df_tot['char_type'] == char, 'diff'], stat='density', bins=b, binrange=(0, xr), ax=axs[i], color=colors[i], alpha=a)

    # Find the probability density function for fitted lognormal distribution
    pdf = calc_pdf(x, df_tot.loc[df_tot['char_type'] == char, 'diff'])
    
    # Plot the fitted probability density function over the histogram
    sns.lineplot(x=x, y=pdf, ax=axs[i], linewidth=4, color=colors[i])
    
    # Plot fitted probability density function in the final panel
    sns.lineplot(x=x, y=pdf, ax=axs[4], linewidth=2, color=colors[i])
    
    
    ## Entry in legend
    # Define line with label for legend
    line = Line2D([0], [0], color=colors[i], lw=4, label=char)
    
    # Add legend for current panel
    axs[i].legend(handles=[line], loc='upper right', fontsize=small)
    
    # Add legend entry to the list of legend elements for the last panel
    legend_elements.append(line)
    

## Combined data
# Define line with label for legend
line = Line2D([0], [0], color=colors[3], lw=4, label='Combined data')

# Add legend for current panel
axs[3].legend(handles=[line], loc='upper right', fontsize=small)

# Add legend entry to the list of legend elements for the last panel
legend_elements.append(line)

# Plot the aggregated data as histogram
sns.histplot(df_tot['diff'], stat='density', bins=b, binrange=(0, xr), ax=axs[3], alpha=a, color=colors[3])

# Find the probability density function for fitted lognormal distribution
pdf = calc_pdf(x, df_tot['diff'])

# Plot the fitted probability density function over the histogram
sns.lineplot(x=x, y=pdf, ax=axs[3], linewidth=4, color=colors[3])

# Plot fitted probability density function in the final panel
sns.lineplot(x=x, y=pdf, ax=axs[4], linewidth=2, color=colors[3])

# Add legend to the last panel
axs[4].legend(handles=legend_elements, loc='upper right', fontsize=small)


# Define parameters common to all panels
for ax in axs:
    # Set label for the y-axis
    ax.set_ylabel("Density", fontsize=small)
    
    # Set label for the x-axis
    ax.set_xlabel("Difference (mm)", fontsize=small)
    
    # Set labelsizes
    ax.tick_params(labelsize=x_small)

# Save figure
plt.savefig("31.2_Difference_between_repeated_measurements.jpeg", dpi=600, bbox_inches='tight')
plt.savefig("31.2_Difference_between_repeated_measurements.pdf", bbox_inches='tight')