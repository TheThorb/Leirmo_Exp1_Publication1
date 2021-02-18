"""
Create figure 30 "Difference between repeated measurements"

Plot the difference between repeated measurements based on the characteristic type

The figure is designed for publication in Applied Sciences

"""

## Import packages
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import os


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

# Create new dataframe sorted by characteristic type
data = df_tot.sort_values(by='char_type')

# Compute the standard deviation of differences
std = df_tot['diff'].std()

# Reset index
data.reset_index(drop=True, inplace=True)


## Define parameters for figure
# Definition for font sizes
large = 24
medium = 18
small = 14
x_small = 12

# Define font
pfont = {'fontname':'Palatino Linotype'}

# Seaborn theme
sns.set_theme(context='paper', style='whitegrid')

# Initialize figure
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15, 7))

# Configure layout spacing
fig.tight_layout(pad=8.0)

# Set context with Seaborn
sns.set_context("paper", font_scale=1.2)


## PLOT 1
# Scatterplot in first frame
sns.scatterplot(ax=axs[0], data=data, y='diff', x=data.index, hue='char_type', legend=True, palette='colorblind')

# Insert horizontal line at five standard deviations
axs[0].axhline(y=std*5, color='black', linestyle='--', alpha=0.7)

# Get number of datapoints for each characteristic
n_cyl = len(data[data['char_type'] == 'Cylindricity'])
n_dia = len(data[data['char_type'] == 'Diameter'])
n_flt = len(data[data['char_type'] == 'Flatness'])

# Set ticks on x-axis in intersections between characteristics
axs[0].set_xticks([n_cyl/2, n_cyl + (n_dia/2), len(data) - (n_flt/2)])

# Set tick labels for x-axis
axs[0].set_xticklabels(["Cylindricity\nn = {}".format(n_cyl),\
                        "Diameter\nn = {}".format(n_dia),\
                        "Flatness\nn = {}".format(n_flt)], fontsize=medium)

# Set ticks on y-axis
axs[0].set_yticks([0, std*3, 0.05, std*5, 0.1, 0.15, 0.2, 0.25])

# Set tick labels for y-axis
axs[0].set_yticklabels(["0.00", "3\u03C3", "0.05", "5\u03C3\n", "0.10", "0.15", "0.20", "0.25"], fontsize=medium)

# Place legend in upper left corner without title
axs[0].legend(loc='upper left', title=None, fontsize=medium, fancybox=True, markerscale=2)


## Filter outliers above five standard deviations
data = data[data['diff'] < std * 5]


## PLOT 2
# Scatterplot in second frame
sns.scatterplot(ax=axs[1], data=data, y='diff', x=data.index, hue='char_type', legend=False, palette='colorblind')


# Get number of datapoints for each characteristic
n_cyl = len(data[data['char_type'] == 'Cylindricity'])
n_dia = len(data[data['char_type'] == 'Diameter'])
n_flt = len(data[data['char_type'] == 'Flatness'])

# Set ticks on x-axis in intersections between characteristics
axs[1].set_xticks([n_cyl/2, n_cyl + (n_dia/2), len(data) - (n_flt/2)])

# Set tick labels for x-axis
axs[1].set_xticklabels(["Cylindricity\nn = {}".format(n_cyl),\
                        "Diameter\nn = {}".format(n_dia),\
                        "Flatness\nn = {}".format(n_flt)], fontsize=medium)

# Set ticks on y-axis
axs[1].set_yticks([0, 0.01, 0.02, 0.03, std*3, 0.04, 0.05, 0.06])

# Set tick labels for y-axis
axs[1].set_yticklabels(["0.00", "0.01", "0.02", "0.03", "3\u03C3", "0.04", "0.05", "0.06"], fontsize=medium)


for ax in axs:
    # Set label for y-axis
    ax.set_ylabel("Difference [mm]", fontsize=large)
    
    # Hide ticks on x-axis
    ax.tick_params(axis='x', length=0)
    
    # Insert horizontal line at three standard deviations
    ax.axhline(y=std*3, color='black', linestyle='-', alpha=0.7)
    
    # Set grid for y-axis only
    ax.xaxis.grid(False)

# Save figure
plt.savefig("30.5_Difference_between_repeated_measurements.jpeg", dpi=600, bbox_inches='tight')
plt.savefig("30.5_Difference_between_repeated_measurements.pdf", bbox_inches='tight')