## Properties class = User specifications - update when widget values are updated
# Jan 18, 2022
## Properties class = User specifications - update when widget values are updated
class hourglassParameters():
    # Data file paths
    filepath_matrix = None  # numeric matrix
    filepath_rowAnn = None  # describes rows of matrix
    filepath_colAnn = None  # describes columns of matrix

    # Name
    dataset_name = "BySample"

    # Make Comparisons tab
    comparisons_table = [] # list of dict objects: {'MainComparison': "", 'CustomComparison': "", 'Subgroup': "", 'WithinGroup': "", 'Filter': ""}

    # Feature Sets tab = Custom analysis in R (key/values)
    feature_sets = [] # list of dict objects for feature set name and comma-delimited list: {'GroupName': "", 'GroupList':""}
    feature_parameters = [] # list of dict objects for parameters for each feature and comma-delimited list: {'Feature': "", 'StdParam':"", 'AltParam':""}

    # Customize Colors tab
    color_palette = []

    # Advanced Options tab
    corr_method = "pearson" # default correlation method for correlation plot
    pval_test = "t.test" # default 2 sample statistical test
    pval_label = "stars" # default labels for p-values on box and correlation plots
    color_gradient = "RdBu"
    paired_id_column = "" # patient ID column name in rowAnn - only when there are multiple samples per patient in dataset
    do_survival_analysis = True # perform survival analysis?
    surv_time_column = "OS time" # OS/DFS time column in rowAnn
    surv_status_column = "Status"# vital status/event column in rowAnn
    do_impute = True # run imputed version in parallel?
    impute_with_mean = 5 # percent +/- around mean to impute missing values
    do_remove_outliers = True
    discrete_params = "Het.Score" # numeric parameters that will be plotted as discrete values e.g. scores 1-4
    # Run hourglass tab
    qc_feature_boxplots = False # make quality control (qc) boxplots
    qc_param_boxplots = True # make quality control (qc) boxplots
    param_column = "Parameter" # parameter column in colAnn (e.g. Parameter, Readout)
    feature_column = "Stain" # feature column in colAnn (e.g. Gene.Sym, Stain)
    # if feature_sets is not empty --
    boxplot_indiv = True # make individual boxplots
    boxplot_overview = True # overview - combines individual boxplots into 1
    heatmap = True # make heatmaps showing all features in all samples/patients?
    corrplot = True # make correlation plots comparing all features?
    corrscatt_overview = False # make correlation scatter plots comparing all features?
    pval_FC_heatmap = True # make heatmaps showing fold-change and p-values for each comparison?
    barplot_profile = True # make discrete bar plots showing feature amounts in each patient/sample?
    barplot_het = True # make barplots to collapse samples by patient to see heterogeneity (het) across patients

    def __init__(self):
        pass

# Instantiate parameters object (save variables here to input into R)
p = hourglassParameters()

# Simulate user input
p.feature_sets = [{'GroupName': 'TCell', 'GroupList': "CD3,CD8"},
    {'GroupName': 'BCell', 'GroupList': "CD20, CD27, CD5, PDL1"},
    {'GroupName': 'immune','GroupList': "TCell, BCell"},
    {'GroupName': 'all', 'GroupList': "immune, IL6, SMA"}]

p.feature_parameters  = [{'Feature': "CD3", 'StdParam': "Num.Pos.per.mm.2", 'AltParam': "Pos.Pixel.Percent"}, {'Feature': "CD8", 'StdParam': "Num.Pos.per.mm.2", 'AltParam': "Pos.Pixel.Percent"},
    {'Feature': "CD20", 'StdParam': "Num.Pos.per.mm.2", 'AltParam': "Pos.Pixel.Percent"}, {'Feature': "CD27", 'StdParam': "Num.Pos.per.mm.2", 'AltParam': "Pos.Pixel.Percent"},
    {'Feature': "CD5", 'StdParam': "Num.Pos.per.mm.2", 'AltParam': "Pos.Pixel.Percent"}, {'Feature': "PDL1", 'StdParam': "Num.Pos.per.mm.2", 'AltParam': "Pos.Pixel.Percent"},
    {'Feature': "IL6", 'StdParam': "Num.Pos.per.mm.2", 'AltParam': "Pos.Pixel.Percent"}, {'Feature': "SMA", 'StdParam': "Num.Pos.per.mm.2", 'AltParam': "Pos.Pixel.Percent"}]

p.comparisons_table = [{'MainComparison': 'Sample_Cancer_Subtype', 'CustomComparison': '', 'Subgroup': 'Smoker', 'WithinGroup': '', 'Filter': 'Sex!=X', 'BySample': 'True', 'ByPatient': 'True'},
{'MainComparison': 'Patient_Cancer_Subtype', 'CustomComparison': '', 'Subgroup': 'Smoker', 'WithinGroup': 'Sex', 'Filter': 'Sex!=X', 'BySample': 'False', 'ByPatient': 'True'},
{'MainComparison': '', 'CustomComparison': 'IL6_Pos.Pixel.Percent', 'Subgroup': '', 'WithinGroup': '', 'Filter': 'NeoAdjuvant!=neo', 'BySample': 'True', 'ByPatient': 'True'}]

p.color_palette = {'Smoker-Yes': '#5FC576ff', 'Smoker-No': '#5899E8ff',
                   'Patient_Cancer_Subtype-A': '#2EE162ff', 'Patient_Cancer_Subtype-B': '#670CB9ff', 'Patient_Cancer_Subtype-C': '#B6C163ff',
                   'Sample_Cancer_Subtype-A': '#2F9E97ff', 'Sample_Cancer_Subtype-B': '#FFFC4Dff', 'Sample_Cancer_Subtype-C': '#C0632Fff',
                   'Custom-high': '#73F5F2ff', 'Custom-intermediate': '#9B13C7ff', 'Custom-low': '#761342ff'}

# Save python environment variable to file
import dill
dill.dump_session("hourglassParameters_p2.pkl")

# Updated Mar13, 2022
import dill
dill.load_session("hourglassParameters_p2.pkl")

# Reduce to 1 comparison
p.comparisons_table = [{'MainComparison': 'Sample_Cancer_Subtype', 'CustomComparison': '', 'Subgroup': 'Smoker', 'WithinGroup': '', 'Filter': 'Sex!=X', 'BySample': 'True', 'ByPatient': 'True'}]
# New names of elements, e.g. StdParam (old) Standard_Parameter (new)
p.feature_parameters = [{'Feature': 'CD3', 'Standard_Parameter': 'Num.Pos.per.mm.2', 'Alternative_Parameter': 'Pos.Pixel.Percent'},
 {'Feature': 'CD8', 'Standard_Parameter': 'Num.Pos.per.mm.2', 'Alternative_Parameter': 'Pos.Pixel.Percent'},
 {'Feature': 'CD20', 'Standard_Parameter': 'Num.Pos.per.mm.2', 'Alternative_Parameter': 'Pos.Pixel.Percent'},
 {'Feature': 'CD27', 'Standard_Parameter': 'Num.Pos.per.mm.2', 'Alternative_Parameter': 'Pos.Pixel.Percent'},
 {'Feature': 'CD5', 'Standard_Parameter': 'Num.Pos.per.mm.2', 'Alternative_Parameter': 'Pos.Pixel.Percent'},
 {'Feature': 'PDL1', 'Standard_Parameter': 'Num.Pos.per.mm.2', 'Alternative_Parameter': 'Pos.Pixel.Percent'},
 {'Feature': 'IL6', 'Standard_Parameter': 'Num.Pos.per.mm.2', 'Alternative_Parameter': 'Pos.Pixel.Percent'},
 {'Feature': 'SMA', 'Standard_Parameter': 'Num.Pos.per.mm.2', 'Alternative_Parameter': 'Pos.Pixel.Percent'}]

# Add 'Alternative': "TRUE"
p.feature_sets = [{'GroupName': 'TCell', 'GroupList': 'CD3,CD8', 'Alternative': "TRUE"},
                  {'GroupName': 'BCell', 'GroupList': 'CD20, CD27, CD5, PDL1', 'Alternative': "TRUE"},
                  {'GroupName': 'immune', 'GroupList': 'TCell, BCell', 'Alternative': "TRUE"},
                  {'GroupName': 'all', 'GroupList': 'immune, IL6, SMA', 'Alternative': "TRUE"}]
# New patient ID
p.paired_id_column = "Patient_ID"

# Save p object to file
dill.dump_session("hourglassParameters_p2.pkl")