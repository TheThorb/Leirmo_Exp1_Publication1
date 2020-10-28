"""
Module of functions taylored for the PhD-experiments of Torbjørn L. Leirmo.

Created by Torbjørn L. Leirmo


Contents:
	load_results()								# Load the 'results'-file
	load_layout()								# Load the 'layout'-file
    pickle_data()                               # Load results and layout and pickle to separate files
	make_dict(df, df_layout)					# NB! No pickles! Make a dictionary of characteristics
	make_char_dict()                            # Create dictionary of characteristics from pickled data
    save_dict(char_dict)						# Save the dictionary in separate files
	get_single_values(col, val, some_list)		# Get rows containing a certain value from a list of dataframes
	exclude_values(col, val, some_list)			# Exclude rows containing a certain value from a list of dataframes
	df_from_dict(keys, a_dict)					# Retrieve specified characteristics from the dictionary
	get_column(col, some_list)					# Get specific columns from a list of dataframes
	get_planes(some_dict)						# Get a dataframe with all planes and angle_z
	my_t_test(dft, par='z_pos')					# Perform a t-test for all combinations of a DF and return a MIDF
	get_p_vals(dft, par='z_pos')                # Perform a t-test for all combinations of a DF and return p-vals only
    calc_laser_angle(x, y, feature_vector=...)  # Calculate laser angle
    rotate_vector(vector, a=0, b=0, c=0)        # Rotate a vector
    add_laser_angle(df, feature_vector=...)     # Add column 'laser_angle' to dataframe

"""

# Import libraries

import math
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

##############################################################################

def load_results():
    """
    Create dataframe with selected columns from the results-file.
	
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

    # part_name   = Name of the specimen           (e.g. "Leirmo_Exp1_Build3_#11")
    # build       = Build number                   (1-3)
    # part_index  = Specimen number in the build   (1-45)
    # x_pos       = x-position (simple)            (1-3)
    # y_pos       = y-position (simple)            (1-3)
    # z_pos       = z-position (simple)            (1-3)
    # angle       = Part rotation about x-axis     (0-180, -90 for anchor specimen [degrees])
    # center_x    = x-position (actual)            (Center position along x-axis* as given in Magics [mm])
    # center_y    = y-position (actual)            (Center position along y-axis* as given in Magics [mm])
    # center_z    = z-position (actual)            (Center position along z-axis** as given in Magics [mm])
    
    # *  x- and y-positions are evenly distributed at 70, 170 and 270 [mm]
    # ** z-positions are adjusted for layer height at 50.88, 150.6, 250.32, 350.04 and 449.76 [mm]
    
    return pd.read_csv(path, sep = ';', index_col = 'part_name')


def pickle_data():
    """
    Pickle the dataframe with all results for faster loading.

    """
    # Load the results and the layout data into separate dataframes
    df_res = load_results()
    df_layout = load_layout()

    # Pickle the dataframes to specified locations
    df_res.to_pickle("Data/prep_data.pkl")
    df_layout.to_pickle("Data/layout_data.pkl")


### NB! No pickles involved!
def make_dict(df, df_layout):
    """
    Establish a dictionary of characteristics with layout data
    Dictionary keys = characteristic name
    Dictionary values = dataframe with parts, errors and layout data
    
    """
    char_dict = {}
    
    # Identify all the unique parts and characteristics
    chars = df['char_name'].unique()
    
    ## Create an entry for every characteristic.
    # Stores only mean measured error of repeated measurements
    # Removes redundant columns
    for char in chars:
        char_dict[char] = df[df['char_name'] == char].groupby('part_name').mean()\
        .drop(['rep', 'actual', 'nominal', 'char_number'], axis = 1).join(df_layout)
    
    return char_dict


def make_char_dict():
    """
    Create a dictionary of characteristics from pickled data.
    The function loads data instead of taking arguments

    """
    # Initialize empty dictionary for characteristics
    char_dict = {}

    # Load pickled data
    df = pd.read_pickle("Data/prep_data.pkl")
    layout = pd.read_pickle("Data/layout_data.pkl")
    
    # Identify all the unique parts and characteristics
    chars = df['char_name'].unique()
    
    ## Create an entry for every characteristic.
    # Stores only mean measured error of repeated measurements
    # Removes redundant columns
    for char in chars:
        char_dict[char] = df[df['char_name'] == char].groupby('part_name').mean()\
        .drop(['rep', 'actual', 'nominal', 'char_number'], axis = 1).join(layout)
    
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
    df_t_test = pd.DataFrame(index = pd.MultiIndex.from_tuples(tuples, names=[par,'type']), columns = labels)

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


def get_p_vals(dft, par='z_pos'):
    """
    Perform a T-test for pairwise comparison of distributions and only get p-values
    
    Arguments:
        A single DataFrame with an 'error' column
        A string indicating which parameters to compare (default = 'z_pos')

    Return:
        A dataframe containing the P-values of all combinations
    
    """
    # Find the number of unique values of 'par'
    n = len(dft[par].unique())

    # Extract and sort a list of unique lables
    labels = sorted(dft[par].unique())

    # Initiate DataFrame object
    df = pd.DataFrame(index=labels, columns=labels)

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
            df[labels[i]][labels[j]] = p_val
            df[labels[j]][labels[i]] = p_val

    # Return a dataframe with the p-values
    return df


def calc_angle(vector_a, vector_b):
    """
    Calculate the angle between two vectors

    Arguments:
        vector_a = the first vector as a nympy array
        vector_2 = the second vector as a nympy array
    Return:
        The angle in degrees

    """
    # Cast to numpy arrays
    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    # Calculate dot-products
    over = np.dot(vector_a, vector_b)
    under = np.sqrt(vector_a.dot(vector_a)) * np.sqrt(vector_b.dot(vector_b))

    # Return angle in degrees
    return math.degrees(np.arccos(over/under))


def calc_laser_angle(x, y, feature_vector=np.array([0, 0, 1])):
    """
    Calculate laser angle.

    Arguments:
        x = x-position of the feature/part
        y = y-position of the feature/part
        feature_vector = normal vector of the feature (default = [0, 0, 1])

    Return:
        The laser angle in degrees

    """
    # Initialize positions
    part_pos = np.array([x, y, 0])
    laser_pos = np.array([170, 170, 600])

    # Calculate the vector from part position to the laser
    laser_vector = np.subtract(laser_pos, part_pos)

    # Return angle in degrees
    return calc_angle(feature_vector, laser_vector)


def rotate_vector(vector, a=0, b=0, c=0):
    """
    Rotate a vector about x, y and z axis.

    Arguments:
        vector = the vector to rotate
        a = rotation about x-axis in degrees
        b = rotation about y-axis in degrees
        c = rotation about z-axis in degrees

    Return:
        a rotated vector
    """

    if a:
        a = math.radians(a)
        vector = np.dot(np.array([[1,0,0],[0,np.cos(a),-np.sin(a)],[0, np.sin(a), np.cos(a)]]), vector)
    if b:
        b = math.radians(b)
        vector = np.dot(np.array([[np.cos(b),0,np.sin(b)],[0,1,0],[-np.sin(b), 0, np.cos(b)]]), vector)
    if c:
        c = math.radians(c)
        vector = np.dot(np.array([[np.cos(c), -np.sin(c),0],[np.sin(c), np.cos(c),0],[0,0,1]]), vector)

    return vector


def add_laser_angle(df, feature_vector=np.array([0, 0, 1])):
    """
    Calculate the laser angle and insert as a new column in the dataframe.

    Arguments:
        A single dataframe containing x- and y-positions

    Return:
        A copy of the original dataframe with a column for laser angle

    """
    # Get a list of column names
    headers = list(df.columns)

    # Initiate a list (to be the new column)
    new_col = []

    # Iterate over the rows of the dataframe
    for i in range(len(df)):
        # Update feature vector with part orientation
        new_feature_vector = rotate_vector(vector=np.array(feature_vector), a=df.iloc[i]['angle'])

        # Find x-coordinate depending on availability
        if 'center_x' in headers:
            x_coor = df.iloc[i]['center_x']
        elif 'x_pos' in headers:
            x_coor = (df.iloc[i]['x_pos'] * 100) -30

        # Find y-coordinate depending on availability
        if 'center_y' in headers:
            y_coor = df.iloc[i]['center_y']
        elif 'y_pos' in headers:
            y_coor = (df.iloc[i]['y_pos'] * 100) -30

        # Calculate the laser angle and append to list
        new_col.append(calc_laser_angle(x_coor, y_coor, new_feature_vector))

    # Add the new column to the dataframe
    df['laser_angle'] = new_col

    # Return the dataframe
    return df