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
	from_char_dict(keys, a_dict)				# Retrieve specified characteristics from the dictionary
	get_column(col, some_list)					# Get specific columns from a list of dataframes
	
"""

# Import libraries

import pandas as pd


def load_results():
    """
    Create dataframe with selected columns from the resutlts-file.
    
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
