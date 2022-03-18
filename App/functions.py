import pandas as pd

# returns a logical (T/F) array where the key matches the index of arr
def grepl(arr, key):
    return [key in i for i in arr]

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

