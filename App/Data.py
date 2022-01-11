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
ds.name = "hello"
print(ds.name)