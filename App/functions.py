import os
# import dill  # pip install dill --user
import sys
import numpy as np
import pandas as pd

# Save session (all python variables)
# https://stackoverflow.com/questions/2960864/how-can-i-save-all-the-variables-in-the-current-python-session
def save_workspace(file="global_env"):
    dill.dump_session(file + ".pkl")

# Load the session
def load_workspace(file):
    dill.load_session(file + ".pkl")

# Check files in current working directory
def list_files(folder):
    return os.listdir(folder)

# clear all variables
def clear_env():
    import sys
    sys.modules[__name__].__dict__.clear()

# returns a logical (T/F) array where the key matches the index of arr
def grepl(arr, key):
    return [key in i for i in arr]

# gets elements that contain a keyword in an array
def get_matches(arr, key):
    match = grepl(arr, key)
    arr = np.array(arr)
    return arr[match]

# returns a logical list
# if elements of arr1 intersects with array2, the result will be T at array1's index
def get_matches2(arr1, arr2):
    return [True if x in arr2 else False for x in arr1]

# returns the elements that are present in 2 arrays
def intersect(arr1, arr2):
    t = get_matches2(arr1, arr2)
    return arr1[t]

# key = "matrix"
# sep = "\t"; header = 0; index_col = 0

# Read data frame into pandas
def read_tbl(filepath, sep="\t", header=0, index_col=0):

    try:
        if grepl([filepath], ".csv"):
            # Read into pandas data frame
            return pd.read_csv(filepath, header=header, index_col=index_col)

        if grepl([filepath], ".txt"):
            # Read into pandas data frame
            return pd.read_table(filepath, sep=sep, header=header, index_col=index_col)

    except Exception as e:
        # If file isn't found throw error, and specify number of files matching the key
        print("Oops!", e.__class__, "occurred.")
        print(len(filepath), "not found.")
        return None

# Sort by a value in ascending/descending order
# axis 0 is by column and 1 is by row
def sort_tbl(name, tbl, axis):
    return tbl.sort_values(by=name, axis=axis)


# Reindex pandas data frame (tbl) by row
# ord = new row order
# https://www.geeksforgeeks.org/python-pandas-dataframe-reindex/
def reord_rows(ord, tbl):
    return tbl.reindex(ord)


# Reindex pandas data frame (tbl) by column
# ord = new column order
def reord_cols(ord, tbl):
    return tbl.reindex(columns=ord)
