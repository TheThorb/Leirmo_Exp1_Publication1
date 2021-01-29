# Leirmo_Exp1_Publication1
This repository contains data, code, and figures for the first publication of results from the first experiment of Torbjørn Langedahl Leirmo.
The repository is established in connection with a scientific publication where the results are disseminated.
Links will be provided shortly after publication.
Any inquiries may be directed to torbjorn.leirmo@ntnu.no.


## Dependencies
The code is developed in a Windows 10 operating system using Python 3.
The following list contains all dependencies and the appropriate versions.

 - Matplotlib v3.3.3
 - Numpy v1.19.5
 - Pandas v1.2.0
 - Scipy v1.6.0
 - Seaborn v0.11.1


## Contents
The repository contains folders of data, figures, and plots, as well as files of source code and notebooks for data analysis.

### Jupyter Notebooks
The notebooks are numbered according to the logical progression of analyzing the data, namely:

0. Slice distribution visualization (pre-process)
1. Analyze repeated measurements
2. Comparison of builds
3. Analysis of variation along the z-axis of the build chamber
4. Analysis of variation in the xy-plane

### Python files
There are two Python-files of source code. These files contain utility functions used in one or more of the notebooks.

* "my_functions.py": Primarily functions for reading and saving data, as well as functions for handling lists of Pandas dataframes.
* "my_plot.py": Functions for plotting data


### Folders
"artifacts": STL-files used in the experiment.
 - "Leirmo_Exp1_Corner_Specimens.stl": The corner specimen constructed by constructive solid geometry in MS 3D-builder
 - "Leirmo_Exp1_ISO-ASTM_52902_CA_F.stl": Small cylindrical specimen retrieved from ISO/ASTM 52902:2019
 - "Leirmo_Exp1_Main_Artifact.stl": Artifact constructed in SolidWorks inspired by the design of Minetola et al. (2016)

"data": This folder contains data related to the experiment.
 - "data_description.txt": Textual description of the data
 - "leirmo_exp1_layout.csv": Information about the experiment layout (placement of specimens)
 - "layput_data.pkl": Pickled version of the layout information for fast loading
 - "Leirmo_Exp1_ALL.csv": Table with all data directly exported from the coordinate measuring machine (i.e. no layout information)
 - "prep_data.pkl": Pickled version of all data from the coordinate measuring machine
 - "T-test_Angle_Cylindricity.csv": Results from T-test of angle versus cylindricity
 - "T-test_Z-dir_Cylinders.csv": Results from T-test of Z-direction versus cylindricity
 
"figs": Figures used as illustrations in notebooks.
 - "layout_positions.png": A visualization of the different positions in the build chamber (x-, y-, and z-direction)
 - "specimen_with_labels.png": Figure displaying the test artifact where the features are labeled
 
"plots": Plots and the code for their creation. Separate contents file is found in the folder.


## References
ISO/ASTM 52902:2019(E). Additive manufacturing – Test artifacts – Geometric capability assessment of additive manufacturing systems. ISO/ASTM: 2019.

Minetola, P.; Iuliano, L.; Marchiandi, G. Benchmarking of FDM Machines through Part Quality Using IT Grades. Procedia CIRP 2016, 41, 1027–1032, DOI: https://doi.org/10.1016/j.procir.2015.12.075.
