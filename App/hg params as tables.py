# Run in python console
import dill
import pandas as pd
import xlsxwriter
dill.load_session("hourglassParameters_p2.pkl")

# Convert to tables to write to Excel
# 1  - Comparisons
# Make initial dataframe
df1 = pd.DataFrame(p.comparisons_table)
# Get attributes of p object that are not hidden or already present
atts = [i for i in p.__dir__() if"__" not in i and i not in ['feature_sets', 'feature_parameters', 'comparisons_table', 'color_palette']]
# Create a new column and add values to dataframe
for att in atts:
    df1[att] = p.__getattribute__(att)
df1_t = df1.transpose()
# 2 - Color Palette
x = p.color_palette
df2 = pd.DataFrame({'Variable': [i for i in x], 'HexCode': [x[i] for i in x]})

# 3 - Feature Sets
df3 = pd.DataFrame(p.feature_sets)

# 4 - Feature Parameters
df4 = pd.DataFrame(p.feature_parameters)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pandas_multiple.xlsx', engine='xlsxwriter')

# Write each dataframe to a different worksheet.
df1_t.to_excel(writer, sheet_name='Comparisons', header=False)
df2.to_excel(writer, sheet_name='Colors', index=False)
df3.to_excel(writer, sheet_name='FeatureSets', index=False)
df4.to_excel(writer, sheet_name='FeatureParameters', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()