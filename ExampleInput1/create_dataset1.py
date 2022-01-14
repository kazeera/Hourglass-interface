import pandas as pd
import dill

# Make dataset class
class Dataset:
    name = None
    mat = None  # numeric matrix
    rowAnn = None  # describes rows of matrix
    colAnn = None  # describes columns of matrix

    def __init__(self):
        pass

# can modify object attributes
ds = Dataset()
print(ds.mat)

print(ds.name)
ds.name = "name"
print(ds.name)

ds.mat = "mat"
print(ds.mat)

ds.rowAnn = "rowAnn"

# # Save python object to file
# import pandas as pd
# import numpy as np
# from functions import *
# list_files("ExampleInput1/csv files/")
in_dir = "ExampleInput1/csv files/"
ds = Dataset()
ds.name = "name"
ds.mat = pd.read_csv(in_dir + "numeric_matrix.csv", header=0, index_col=0)
ds.rowAnn = pd.read_csv(in_dir + "row_annotations.csv", header=0, index_col=0)
ds.colAnn = pd.read_csv(in_dir + "column_annotations.csv", header=0, index_col=0)

dill.dump_session("dataset1.pkl")
# Load
dill.load_session("dataset1.pkl")