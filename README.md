# Leirmo_Exp1
This repository contains data, code and figures for the experiment "Leirmo_Exp1".
The experiment is part of the PhD-project og Torbjørn Langedahl Leirmo and was conducted in the spring/summer of 2020.


## Contents
The repository contain folders of data, figures and plots, as  well as files of source code and notebooks for data analysis.
The notebooks are numbered according to the logical progression of analyzing the data, namely:

1. Analyze repeated measurements
2. Comparison of builds
3. Analysis of variation along the z-axis of the build chamber
4. Analysis of variation in the xy-plane

The remaining notebooks are either work in progress or unrelated analyses.

There are two Python-files of source code. These files contain utility functions used in one or more of the notebooks.

"my_functions.py": Primarily functions for reading and saving data, as well as functions for handlig lists of dataframes.
"my_plot.py": Functions for plotting data


### Folders
"data": This folder contain data related to the experiment.
 - "data_description.txt": Textual description of the data
 - "leirmo_exp1_layout.csv": Information about the experiment layout (placement of specimens)
 - "layput_data.pkl": Pickled version of the layout information for quick read
 - "Leirmo_Exp1_ALL.csv": Table with all data directly exported from the coordinate measuring machine (i.e. no layout information)
 - "prep_data.pkl": Pickled version of all data from coordinate measuring machine
 - "T-test_Angle_Cylindricity.csv": Results from T-test of angle versus cylindricity
 - "T-test_Z-dir_Cylinders.csv": Results from T-test of Z-direction versus cylindricity
 
"figs": Figures used as illustrations in notebooks.
 - "layout_positions.png": A visualization of the different positions in the build chamber (x, y and z- direction)
 - "specimen_with_labels.png": Figure displaying the test artifact where the features are labelled
 
"plots": Plots created from various notebooks. Separate contents file is found in the folder.


## Dependencies
The code is developed in a Windows 10 operating system using Python 3.
The following list contain all dependencies and the appropriate versions.

 - Matplotlib v3.2.0
 - Pandas v1.1.2
 - Numpy v1.19.1
 - Scipy v1.5.2
 - Seaborn v0.11.1
