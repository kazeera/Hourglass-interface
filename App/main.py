from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.recycleview import RecycleView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty, ListProperty, DictProperty, partial
from kivy.uix.colorpicker import ColorPicker
from kivy.core.window import Window

import rpy2
from rpy2.robjects.packages import importr
import xlsxwriter
import pandas as pd # reading and importing dataframes for Dataset objects
import random # customize colors - random chooser
import dill # need to import pkl data (existing python environment variables)
from functions import * # in house functions

## Properties class = User specifications - update when widget values are updated
class hourglassParameters():
    # Data file paths
    filepath_Matrix = None  # numeric matrix
    filepath_rowAnn = None  # describes rows of matrix
    filepath_colAnn = None  # describes columns of matrix
    outfilename = None # Path to output excel file with dataset

    # Name
    dataset_name = "Dataset1"

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
    do_survival_analysis = False # perform survival analysis?
    surv_time_column = "" # OS/DFS time column in rowAnn
    surv_status_column = ""# vital status/event column in rowAnn
    do_impute = False # run imputed version in parallel?
    impute_with_mean = 5 # percent +/- around mean to impute missing values
    do_remove_outliers = True
    discrete_params = "" # numeric parameters that will be plotted as discrete values e.g. scores 1-4

    # Run hourglass tab
    qc_feature_boxplots = False # make quality control (qc) boxplots
    qc_param_boxplots = False # make quality control (qc) boxplots
    param_column = "" # parameter column in colAnn (e.g. Parameter, Readout)
    feature_column = "" # feature column in colAnn (e.g. Gene.Sym, Stain)
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

class Dataset:
    mat = None  # numeric matrix
    rowAnn = None  # describes rows of matrix
    colAnn = None  # describes columns of matrix

    def __init__(self):
        pass

# Instantiate parameters object (save variables here to input into R)
p = hourglassParameters()
ds = Dataset()

# Import saved variables
dill.load_session("dataset2.pkl")
# dill.load_session("hourglassParameters_p2.pkl")

# Create Welcome tab
class Welcome(Widget):
    pass

# Upload Files tab ---
class UploadTable(Widget):
    def update_name(self):
        p.dataset_name = self.ids.dataset_name.text

class FileChoosePopup(Popup):
    load = ObjectProperty()

class UploadFilePopup(BoxLayout):
    button_text = StringProperty('Choose File')
    file_path = StringProperty("No file chosen")
    label_text = StringProperty("File: ")
    the_popup = ObjectProperty(None)
    id_parameter = StringProperty()

    def open_popup(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        self.file_path = str(selection[0])
        self.the_popup.dismiss()

        # check for non-empty list i.e. file selected and change button text
        if self.file_path:
            self.ids.upload_button.text = self.file_path

        # Update parameter class and read in data to get info from (for mainly spinners)
        if self.id_parameter == "filepath_matrix":
            p.filepath_Matrix = self.file_path
            ds.mat = read_tbl(self.file_path)
        if self.id_parameter == "filepath_rowann":
            p.filepath_rowAnn = self.file_path
            ds.rowAnn = read_tbl(self.file_path)
        if self.id_parameter == "filepath_colann":
            p.filepath_colAnn = self.file_path
            ds.colAnn = read_tbl(self.file_path)

# Comparisons Table tab ---
class ComparisonTable(BoxLayout):
    comp_table2 = ObjectProperty()
    id_number = -1
    # Initialize list
    row_list = []
    row_info_list = []

    def add_a_row(self):
        # Update ID number
        self.id_number += 1
        # Make current row
        curr_row = ComparisonTableRow(id_number2=str(self.id_number))
        # Add to list of ComparisonTableRow objects
        self.row_list.append(curr_row)
        # Add row widget
        self.ids.container.add_widget(curr_row)
        # # Make a list of dict objects (dict object = row info)
        self.row_info_list.append({'MainComparison': "", 'CustomComparison': "", 'Subgroup': "", 'WithinGroup': "", 'Filter': "", 'BySample': "", 'ByPatient': ""})

    def remove_a_row2(self):
        if len(self.row_list) > 0:
            self.ids.container.remove_widget(self.row_list[0])
            del self.row_list[0]

class ComparisonTableRow(BoxLayout):
    id_number2 = StringProperty()

    # Initialize
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_clock, 5)

    # Update checkbox status
    def update_clock(self, *args):
        self.update_row_info()

    # Update hourglass parameters object according to user selection
    def update_row_info(self):
        key_vals = {'MainComparison': "" if self.ids.main_comparison.text == "Main Comparison" else self.ids.main_comparison.text,
                    'CustomComparison': self.ids.custom_comparison.text,
                    'Subgroup': "" if self.ids.subgroup.text == "Subgroup" else self.ids.subgroup.text,
                    'WithinGroup': self.ids.within_group.text,
                    'Filter': self.ids.filter.text,
                    'BySample': str(self.ids.by_sample.active).upper(),
                    'ByPatient': str(self.ids.by_patient.active).upper()
                    }
        ComparisonTable.row_info_list[int(self.id_number2)] = key_vals
        p.comparisons_table = ComparisonTable.row_info_list

# Feature Sets tab ---
class FeatureSets(Widget):
    pass

class FeatureTab1(GridLayout):
    pass

class FeatureTab2(RecycleView):
    features = [""]
    def __init__(self, **kwargs):
        super(FeatureTab2, self).__init__(**kwargs)
        # Set clock to refresh tab every 3 seconds
        Clock.schedule_interval(self.update_clock, 3)

    def update_clock(self, *args):
        # If the user has selected a column from colAnn for features, continue
        if p.feature_column != "" and ds.colAnn is not None:
            # Get new features
            new_features = list(ds.colAnn[str(p.feature_column)].unique())

            if new_features != self.features:
                self.features = new_features
                self.data = [{'label_text': str(x)} for x in self.features]

class FeatureTab2Label(BoxLayout):
    label_text = StringProperty()

    def update_row_info(self):
        # Create new key values pairs
        key_vals = {
            'Feature': self.label_text,
            'Standard_Parameter': "" if self.ids.std_parameter.text == "Standard Parameter (required)" else self.ids.std_parameter.text,
            'Alternative_Parameter': "" if self.ids.alt_parameter.text == "Alternative Parameter" else self.ids.alt_parameter.text,
        }
        # Check whether feature already exists
        if self.label_text not in [i['Feature'] for i in p.feature_parameters]:
            # Add new feature
            p.feature_parameters.append(key_vals)
        else:
            # Update existing feature
            p.feature_parameters['Feature' == self.label_text] = key_vals
        # # Print
        # print(p.feature_parameters['Feature' == self.label_text]) #todo why doesn;t this print properly? shows only first
        # print(p.feature_parameters)

class FeatureTab3(BoxLayout):
    id_number = -1
    # Initialize list
    row_list = []

    def add_a_row(self):
        # Update ID number
        self.id_number += 1
        # Make current row
        curr_row = FeatureTab3Row(id_FeatureTab3=str(self.id_number))
        # Add to list of ComparisonTableRow objects
        self.row_list.append(curr_row)
        # Add row widget
        self.ids.container.add_widget(curr_row)
        # Make a list of dict objects (dict object = row info)
        p.feature_sets.append({'GroupName': "", 'GroupList': "", 'Alternative': False})

    def remove_a_row2(self): #todo remove
        if len(self.row_list) > 0:
            self.ids.container.remove_widget(self.row_list[0])
            # p.feature_sets.remove(p.feature_sets[0]) #p.feature_sets['GroupName' == 'A'])
            del self.row_list[0]

class FeatureTab3Row(BoxLayout):
    id_FeatureTab3 = StringProperty()

    def update_row_info(self):
        # Create dictionary variable to store feature subset name/list
        key_vals = {
            'GroupName': self.ids.group_name.text,
            'GroupList': self.ids.group_list.text,
            'Alternative': self.ids.alternative.active
        }
        # Update hourglass parameters object
        p.feature_sets[int(self.id_FeatureTab3)] = key_vals
        # print(p.feature_sets[int(self.id_FeatureTab3)])

    def remove_row(self): #todo add functionality
        pass
        if len(FeatureTab3.row_list) > 0:
            # # Make current row
            # curr_row = FeatureTab2Row(id_FeatureTab3=str(45))
            # # Add row widget
            # self.app.root.ids.container.add_widget(curr_row)
            # FeatureTab2.ids.container.add_widget(curr_row)
            # FeatureTab2.ids.container.remove_widget(FeatureTab2.row_list[self.id_FeatureTab3])
            pass
            # App.get_running_app().app.root.ids.container.remove_widget(FeatureTab2.row_list[self.id_FeatureTab3])

            # p.feature_sets.remove(p.feature_sets[0]) #p.feature_sets['GroupName' == 'A'])
            # del FeatureTab2.row_list[self.id_FeatureTab3]
#  Customize colors tab ---
class CustomizeColors(RecycleView):
    rowAnn_cols = []
    rowAnn_vals = []
    current_vals = 1

    # Initialize RecycleView layout
    def __init__(self, **kwargs):
        super(CustomizeColors, self).__init__(**kwargs)
        self.data = [{'rowAnn_val': str(i)} for i in self.rowAnn_vals]  # rowAnn_col = rowAnn_color label
        # Set clock to refresh tab every 2 seconds
        Clock.schedule_interval(self.update_clock, 2)

    def update_clock(self, *args):
        self.update_rowAnnvals()

    def update_rowAnnvals(self):
        # Make a list of unique main and subgroup comparisons (ie. rowAnn column names) that are not ""
        self.rowAnn_cols = list(
            set([x["MainComparison"] for x in p.comparisons_table if x["MainComparison"] != ""] +
                [x["Subgroup"] for x in p.comparisons_table if x["Subgroup"] != ""]))

        # Filter out Main Comparison and Subgroup keywords from spinners
        self.rowAnn_cols = [x for x in self.rowAnn_cols if x not in ["Main Comparison", "Subgroup"]]
        # Get all unique variables in rowAnn columns
        self.rowAnn_vals = [[x + "-" + str(y) for y in ds.rowAnn[x].unique()] for x in self.rowAnn_cols
                            if ds.rowAnn[x].dtype == object]
        # Remove nan??
        self.rowAnn_vals = [x for x in self.rowAnn_vals if not str(x).endswith("-nan")]

        # Check whether any main comparisons are continuous (cont) variables (vars) ie. numeric)
        cont_vars = [x for x in self.rowAnn_cols if ds.rowAnn[x].dtype != object]

        # If a custom_column is specified, make a set
        custom_cols = set(item["CustomComparison"] for item in p.comparisons_table if item["CustomComparison"] != "")

        # If this set has a length greater than 0, append the levels (low/int/high) values to values list
        if (len(custom_cols) > 0) | (len(cont_vars) > 0):
            self.rowAnn_vals.append(["Custom-" + x for x in ["low", "intermediate", "high"]])

        # Unlist list of lists
        self.rowAnn_vals = [item for sublist in self.rowAnn_vals for item in sublist]

        # Update current buttons list
        if self.current_vals != self.rowAnn_vals:
            self.current_vals = self.rowAnn_vals

            # Regenerate RecycleView tab
            self.data = [{'rowAnn_val': str(i)} for i in self.rowAnn_vals]

            # Make color palette for rowAnn_vals (unique color for each value) - #todo color changes when there are two many variables e.g. Sample ID
            colors = []
            # Make a list of unique colors
            for i in range(len(self.rowAnn_vals)):
                colors = colors + ["%06x" % random.randint(0, 0xffffff) + 'ff']
            # Make a dictionary of name:hex objects
            p.color_palette = {self.rowAnn_vals[i]: colors[i] for i in range(len(self.rowAnn_vals))}
            # res is {'Cancer.Type-nan': '49c7a9ff', 'Cancer.Type-Mouth': '371fd3ff', 'Cancer.Type-Stomach': '13925dff', 'Cancer.Type-Lung': '529891ff', 'Cancer.Type-Brain': 'fc97a4ff', 'Sex-X': '3734e9ff', 'Sex-F': '7a9527ff', 'Sex-M': '78207aff', 'Smoker-nan': 'b51ffbff', 'Smoker-No': 'e2554dff', 'Smoker-Yes': 'fb7c2cff', 'Custom-low': 'eeb315ff', 'Custom-intermediate': '5efabaff', 'Custom-high': '1f2516ff'}
            # >>> res['A'] is '7a5de0ff'
            # print(p.color_palette)

# Customize color boxlayout for each label
class CCBoxlayout(BoxLayout):
    rowAnn_val = StringProperty()

# Customize color button
class CCButton(BoxLayout):  # If this inherits Button, no overlap but it crashes when we pick color; If we make this BoxLayout, the color picker works but Value1 and Value2 overlap
    the_popup = ObjectProperty(None)
    button_text = StringProperty()
    rowAnn_val_color = "ffffff" # default color is white

    # Initialize RecycleView layout
    def __init__(self, **kwargs):
        super(CCButton, self).__init__(**kwargs)
        # self.rowAnn_val_color = self.get_rand_color() #uncomment for random color
        # Set clock to refresh tab
        Clock.schedule_interval(self.update_clock, 5)

    def update_clock(self, *args):
        self.ids.color_button.background_color = self.rowAnn_val_color = p.color_palette[self.button_text]

    def get_rand_color(self):
        return "%06x" % random.randint(0, 0xffffff) + 'ff'

    def open_popup(self):
        self.the_popup = ColorPopup(load=self.load)
        self.the_popup.open()

    def load(self, colorpicker, *args):
        self.rowAnn_val_color = str(colorpicker.hex_color)[1:]
        self.the_popup.dismiss()

        if self.rowAnn_val_color:
            # Set new button color if non-empty hex value
            self.ids.color_button.background_color = str(self.rowAnn_val_color)
            # Update existing feature in hg parameter class
            p.color_palette[self.button_text] = self.rowAnn_val_color
            # # Print
            # print(p.color_palette)

# Color wheel popup from Kivy, returns Hex code
class ColorPopup(Popup):
    load = ObjectProperty()

# Custom widgets ---
# Check box
class CustomCheckbox(BoxLayout):
    label_text = StringProperty()
    check_box = BooleanProperty()
    id_parameter = StringProperty()

    # Initialize
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_clock, 5)

    # Update checkbox status
    def update_clock(self, *args):
        setattr(p, self.id_parameter, self.ids.chckbx.active)

# Spinner (drop down menu)
class CustomSpinner(BoxLayout):
    label_text = StringProperty()
    spinner_list = ListProperty()
    initial_option = StringProperty()
    id_parameter = StringProperty()
    ann = StringProperty('')# todo

    # Initialize
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_clock, 3)

    # Update parameters object when spinner selection changes
    def selected(self, key, value):
        # print_hourglass_parameter(key, value)
        setattr(p, key, value)

    # When data is uploaded import column names from appropriate tables
    def update_clock(self, *args):
        if self.ann == 'rowAnn':
            self.spinner_list = HourglassApp.getRowAnnCols(self)
        elif self.ann == 'colAnn':
            self.spinner_list = HourglassApp.getColAnnCols(self)
        elif self.ann == 'paramsFeat':
            self.spinner_list = HourglassApp.getParamsFeature(self, *args)
        else:
            pass

# Adv options ---
class AdvancedOptions(Widget):
    # Also p.impute_with_mean, numeric value to impute columnwise around mean for imputed analysis
    impute_val = NumericProperty(5)

    # Update the parameters object with user text input
    def update_discrete_params(self):
        p.discrete_params = self.ids.discrete_params.text

    # Update the parameters object with impute percentage selected by user
    def update_impute_perc(self):
        p.impute_with_mean = self.ids.impute_with_mean.value
        
# Run hourglass tab --
class FolderChoosePopup(Popup):
    load = ObjectProperty()
    file_path = "."

    def print(self, file_path):
        print(file_path)

    # Convert all user input into dataframes and create excel file output
    def create_outfile(self, selection):
        self.file_path = str(selection[0])
        # Convert to tables to write to Excel
        # 1  - Comparisons
        # Make initial dataframe
        df1 = pd.DataFrame(p.comparisons_table)
        # Get attributes of p object that are not hidden or already present
        atts = [i for i in p.__dir__() if "__" not in i and i not in ['feature_sets', 'feature_parameters', 'comparisons_table', 'color_palette']]

        # Add user selections to dataframe as new columns
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

        # Make name of file
        p.outfilename = self.file_path + "/" + p.dataset_name + ".xlsx"
        print(p.outfilename)
        # Create a Pandas Excel writer using XlsxWriter as the engine
        writer = pd.ExcelWriter(p.outfilename, engine='xlsxwriter')

        # Write each dataframe to a different worksheet
        df1_t.to_excel(writer, sheet_name='Comparisons', header=False)
        df2.to_excel(writer, sheet_name='Colors', index=False)
        df3.to_excel(writer, sheet_name='FeatureSets', index=False)
        df4.to_excel(writer, sheet_name='FeatureParameters', index=False)

        # Close the Pandas Excel writer and output the Excel file
        writer.save()

class ParameterPopup(Popup):
    load = ObjectProperty(None)

    def change_path(self, selection):
        p.outfilename = str(selection[0])

class RunHourglass(Widget):
    the_popup = ObjectProperty(None)
    # file_path = StringProperty()

    def runHourglass(self):
        # Interface to R
        print(p.outfilename)
        hourglass = importr("Hourglass")
        # [1] "Out_dir: ."
        # [1] "Getwd: C:/Users/Khokha lab/Documents/GitHub/Kivy Test"
        #
        # hourglass.create_folder(self.file_path + "/" + p.dataset_name )
        # # <rpy2.robjects.vectors.StrVector object at 0x000002ADA4AC6880> [RTYPES.STRSXP]
        # # R classes: ('character',)
        # # ['R Output']
        #
        # Run hourglass in R from main function
        hourglass.run_from_excel(p.outfilename)

    def open_popup(self):
        self.the_popup = FolderChoosePopup(load=self.load)
        self.the_popup.open()  # write to excel file

    def open_parameterPopup(self):
        self.the_popup = ParameterPopup(load=self.load)
        self.the_popup.open()  # select an existing excel file

    def load(self, selection):
        self.file_path = str(selection[0])
        self.the_popup.dismiss() #todo

def print_hourglass_parameter(key, value):
    print(key, ":", value)

class KVTabLay(Widget):
    pass

class HourglassApp(App):
    text_size = 26
    textInput_row_height = 60

    def getRowAnnCols(self):
        if ds.rowAnn is None:
            return [""]
        else:
            return [""] + list(ds.rowAnn.columns.values) # list(ds.rowAnn.columns.values)  # ["", "Smoker", "Age", "Survival.Time", "OS.Status"]

    def getColAnnCols(self):
        if ds.colAnn is None:
            return ""
        else:
            return [""] + list(ds.colAnn.columns.values)  # ["GeneSym", "GeneID", "Parameter"]

    def getParamsFeature(self, feature):
        if ds.colAnn is None:
            return ""
        else:
            if p.param_column == "" or p.feature_column == "" or feature == "":
                return "oops1"
            if feature in list(ds.colAnn[p.feature_column]):
                return list(ds.colAnn[p.param_column][ds.colAnn[p.feature_column] == feature])
        return "oops2"

    def build(self):
        Window.clearcolor = (1,1,1,1)
        return KVTabLay()

if __name__ == '__main__':
    HourglassApp().run()

