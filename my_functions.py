"""
Module of functions taylored for the PhD-experiments of Torbjørn L. Leirmo.

Created by Torbjørn L. Leirmo


Contents:
	load_results()								# Load the 'results'-file
	load_layout()								# Laod the 'layout'-file
	make_dict(df, df_layout)					# Make a dictionary of characteristics
	save_dict(char_dict)						# Save the dictionary in separate files
	get_single_values(col, val, some_list)		# Get rows containing a certain value from a list of dataframes
	exclude_values(col, val, some_list)			# Exclude rows containing a certain value from a list of dataframes
	df_from_dict(keys, a_dict)					# Retrieve specified characteristics from the dictionary
	get_column(col, some_list)					# Get specific columns from a list of dataframes
	get_planes(some_dict)						# Get a dataframe with all planes and angle_z
	t_test_z(dft)								# Perform a t-test for z-layers and return a DataFrame
	
"""

# Import libraries

import math
import pandas as pd
from scipy.stats import ttest_ind


def load_results():
    """
    Create dataframe with selected columns from the resutlts-file.
	
	Return:
		a single dataframe
    
    """
    
    path = "Data/Leirmo_Exp1_ALL.csv"
    
    
    # Define by header name which columns to import 
    cols = ["Uuid", \
            "Characteristic", \
            "K1 Measured value", \
            "K2001 Characteristic number", \
            "K2101 Nominal value", \
            "K4 Time/Date", \
            "K14 Part ident", \
            "K53 Order number"]
    
    
    # Read .csv file using only the defined columns and re-arranging them
    df = pd.read_csv(path, usecols=cols)[["Uuid", \
                                          "K53 Order number", \
                                          "K14 Part ident", \
                                          "Characteristic", \
                                          "K1 Measured value", \
                                          "K2101 Nominal value", \
                                          "K4 Time/Date", \
                                          "K2001 Characteristic number"]]
    
    
    # Re-name columns to shorter more descriptive names
    df.columns = ['uuid', 'part_name', 'rep', 'char_name', 'actual', 'nominal', 'time', 'char_number']


    # Calculating the difference between the nominal and actual values and store them in column 'error'
    df.insert(6, 'error', df['actual'] - df['nominal'], True)


    # Correcting the datatype of the timestamp
    df['time'] = pd.to_datetime(df['time'])


    # uuid        = Unique ID for each measurement (36 characters for measurement run, and 36 for characteristic)
    # part_name   = Name of the specimen           (e.g. "Leirmo_Exp1_Build3_#11")
    # rep         = Measurement repetition number  (1-3)
    # char_name   = Name of the characteristic     (e.g. "Cylindricity_Cyl_4mm_Pos")
    # actual      = Measured value                 (The measured value for the characteristic [mm])
    # nominal     = Nominal value                  (The nominal value, i.e. ideal value [mm])
    # error       = Measured error                 (Difference between measured and nominal values [mm])
    # time        = Timestamp                      (Time of measurement. NB! Eight minutes late!)
    # char_number = Number of the characteristic   (1-106)
    
    
    return df

def load_layout():
    """
	Load the layout data and return a DataFrame using part_name as index.

	"""

    path = "Data/leirmo_exp1_layout.csv"
    
    return pd.read_csv(path, sep = ';', index_col = 'part_name')

def make_dict(df, df_layout):
    """
    Establish a dictionary of characteristics with layout data
    Dictionary keys = characteristic name
    Dictionary values = dataframe with parts, errors and layout data
    
    """
    
    char_dict = {}
    
    
    # Identify all the unique parts and characteristics
    chars = df['char_name'].unique()
    
    
    # Construct separate csv-files of mean error values for each characteristic
    for char in chars:
        char_dict[char] = df[df['char_name'] == char].groupby('part_name').mean()\
        .drop(['rep', 'actual', 'nominal', 'char_number'], axis = 1).join(df_layout)
    
    return char_dict
    
def save_dict(char_dict):
    """
    Save all characteristics form the dictionary to separate .csv-files.
    
    Required: A dictionary of characteristics
    
    """
    
    for name, df in char_dict.items():
        df.to_csv('Data/Chars/{}_mean_excel.csv'.format(name), sep = ';')

def get_single_values(col, val, some_list):
    """
    Function for retrieving rows with a certain value from a list of dataframes.
    
    Arguments:
        col = name of the column in which the value should be
        val = the value used to identify the desired rows
        some_list = a list of dataframes
    
    Return:
        a list of dataframes
    
    """
    
    result = []
    for char in some_list:
        result.append(char[char[col] == val])
    return result

def exclude_values(col, val, some_list):
    """
	Function for removing rows with a certain value from a list of dataframes.
    
    Arguments:
        col = name of the column in which to search for the value
        val = the value used to identify the desired rows
        some_list = a list of dataframes
    
    Return:
        a list of dataframes
	
	"""
    
    result = []
    for char in some_list:
        result.append(char[char[col] != val])
    return result

def df_from_dict(keys, a_dict):
    """
    Function for retrieving a list of specified dataframes from a dictionary.
    
    Arguments:
        keys = a list of dataframes to extract from the dictionary
        a_dict = the dictionary to extract the dataframes from
    
    Return:
        A list of dataframes
    
    """
    
    result = []
    for key in keys:
        result.append(a_dict[key])
    return result

def get_column(col, some_list):
    """
    Function for retrieving specific column(s) from a list of dataframes.
    
    Arguments:
        col = the name of the column(s) to extract
        some_list = a list of dataframes from which the columns will be extracted
    
    Return:
        a list of dataframes (or series if only one column)
    
    """
    
    result = []
    for element in some_list:
        result.append(element[col])
    return result

def get_planes(some_dict):
    """
    Get a list of dataframes containing HX1 and HX2 with angle_z included

    Arguments:
        some_dict = a dictionary containing the required characteristics

    Return:
        a list of dataframes

    """
    
	# Initiate list of DataFrames to return
    df_planes = []
    
	# Iterate through planes 1-6 (j) of HX1 and HX2 (i)
    for i in range(1,3):
        for j in range(1,7):
            temp = some_dict['Flatness_HX{}_Plane{}'.format(i, j)]
            
			# Identify initial orientation based on i and j
            if i == 1:
                flat_rot = (210 + (j*60)) % 360
            else:
                flat_rot = (240 + (j*60)) % 360
            
            # Find the x and y components of the vector (unoriented)
            x = math.cos(math.radians(flat_rot))
            y = math.sin(math.radians(flat_rot))
            
			# Initiate list of z-angles for easy insertion into DataFrame
            z_angles = []
            
			# Calculate the offset from z-direction after part orientation
            for angle in temp['angle']:
                z_angles.append(math.degrees(math.acos(y * math.sin(math.radians(angle)))))
            
			# Insert the z_angles as a new column in the DataFrame
            temp.insert(7, 'angle_z', z_angles, True)
            
			# Insert a column with the characteristic name
            temp.insert(0, 'char', 'Flatness_HX{}_Plane{}'.format(i, j), True)
            
			# Remove any duplicated columns
            temp = temp.loc[:,~temp.columns.duplicated()]
            
			# Add the dataframe to the list
            df_planes.append(temp)
    
	# Return the list of DataFrames
    return df_planes

def t_test_z(dft):
    """
    Perform a T-test for pairwise comparison of the distributions of layers in z-direction
    
    Argument:
        A single DataFrame with an 'error' column
    
    Return:
        A multi-index dataframe containing the T-statistics and P-values of all combinations
    
    """
    
    # Initiate DataFrame object with multi-index
    df_t_test = pd.DataFrame(
							{1: [None] * 10,
							2: [None] * 10,
							3: [None] * 10,
							4: [None] * 10,
							5: [None] * 10},
    index = pd.MultiIndex.from_tuples(
        [(1, 'T-stat'), (1, 'P-val'),\
        (2, 'T-stat'), (2, 'P-val'),\
        (3, 'T-stat'), (3, 'P-val'),\
        (4, 'T-stat'), (4, 'P-val'),\
        (5, 'T-stat'), (5, 'P-val')]))

    # Iterate through all combinations and populate the dataframe
    #   PS: Due to symmetry, only half the dataframe is traversed  
    for i in range(1,6):
        df1 = dft[dft['z_pos'] == i]
        for j in range(i+1, 6):
            df2 = dft[dft['z_pos'] == j]

            # Perform the t-test and populate the dataframe
            df_t_test[i][j]['T-stat'], df_t_test[i][j]['P-val'] = ttest_ind(df1['error'], df2['error'])
            df_t_test[j][i]['T-stat'] = df_t_test[i][j]['T-stat']
            df_t_test[j][i]['P-val'] = df_t_test[i][j]['P-val']


    # Return a multi-index dataframe with results
    return df_t_test

def my_t_test(dft, par='z_pos'):
    """
    Perform a T-test for pairwise comparison of distributions
    
    Arguments:
        A single DataFrame with an 'error' column
        A string indicating which parameters to compare (default = 'z_pos')

    Return:
        A multi-index dataframe containing the T-statistics and P-values of all combinations
    
    """
    
    # Find the number of unique values of 'par'
    n = len(dft[par].unique())

    # Extract and sort a list of unique lables
    labels = sorted(dft[par].unique())

    # Create the lables for 2nd level indexes
    lvl2 = ['T-statistic', 'P-value'] * n

    # Zip lables of 1st and 2nd level to a list of tuples
    tuples = list(zip(*[sorted(labels * 2), lvl2]))

    # Initiate DataFrame object with multi-index
    df_t_test = pd.DataFrame(index = pd.MultiIndex.from_tuples(tuples, names=['z-layer','type']), columns = labels)

    # Iterate through all combinations and populate the dataframe
    #   PS: Due to symmetry, only half the dataframe is traversed
    for i in range(n):
        # Get the rows of the dataframe corresponding to label i
        df1 = dft[dft[par] == labels[i]]
        for j in range(i+1, n):
            # Get the rows of the dataframe corresponding to label j
            df2 = dft[dft[par] == labels[j]]

            # Perform the t-test
            t_stat, p_val = ttest_ind(df1['error'], df2['error'])

            # Populate the output dataframe with the newly discovered results
            df_t_test[labels[i]][labels[j]]['T-statistic'] = t_stat
            df_t_test[labels[i]][labels[j]]['P-value'] = p_val
            df_t_test[labels[j]][labels[i]]['T-statistic'] = -t_stat
            df_t_test[labels[j]][labels[i]]['P-value'] = p_val

    # Return a multi-index dataframe with results
    return df_t_test