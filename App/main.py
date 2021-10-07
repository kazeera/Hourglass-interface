# https://www.reddit.com/r/kivy/comments/ejgfaq/accessing_functions_from_other_classes_in_kv_file/
# http://inclem.net/2019/06/20/kivy/widget_interactions_between_python_and_kv/
# https://kivy.org/doc/stable/api-kivy.clock.html

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
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, NoTransition
from kivy.uix.colorpicker import ColorPicker
import pandas as pd
from kivy.utils import get_color_from_hex, rgba
import numpy as np

from kivy.core.window import Window

# to choose the colors randomly
# every time you run it shows different color
import random
import dill
from functions import *

class hourglassParameters():
    datasetName = None
    filepath_matrix = None  # numeric matrix
    filepath_rowAnn = None  # describes rows of matrix
    filepath_colAnn = None  # describes columns of matrix
    comparisons_table = None
    correlation_method = None

    def __init__(self):
        pass

class Dataset:
    datasetName = None
    mat = None  # numeric matrix
    rowAnn = None  # describes rows of matrix
    colAnn = None  # describes columns of matrix

    def __init__(self):
        pass

p = hourglassParameters()
ds = Dataset()
# dill.load_session("dataset.pkl")
# list(set(ds.rowAnn["Smoker"]))

class Welcome(Widget):
    pass

# Upload Files ---
class UploadTable(Widget):
    def update_name(self):
        ds.datasetName = self.ids.datasetName.text
        ## Update dataset object
        print_hourglass_parameter("datasetName", self.ids.datasetName)
    pass

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

        # Update parameter class
        if self.id_parameter == "filepath_matrix":
            p.filepath_matrix = self.file_path
            ds.mat = read_tbl(self.file_path)
        if self.id_parameter == "filepath_rowann":
            p.filepath_rowann = self.file_path
            ds.rowAnn = read_tbl(self.file_path)
        if self.id_parameter == "filepath_colann":
            p.filepath_matrix = self.file_path
            ds.colAnn = read_tbl(self.file_path)

        # Update dataset object
        print_hourglass_parameter(self.id_parameter, self.file_path) # TODO we can update our dataset object here

# Comparisons Table ---
class ComparisonTable(BoxLayout):
    comp_table2 = ObjectProperty()
    id_number = -1
    # Initialize list
    row_list = []
    row_info_list = []
    #
    # # Simulate list
    row_info_list = [{'MainComparison': "Smoker", 'Subgroup': "", 'CustomComparison': "Gene1", 'Filter': ""}, {'MainComparison': "Sex", 'Subgroup': "", 'CustomComparison': "", 'Filter': ""}, {'MainComparison': "Cancer.Type", 'Subgroup': "", 'CustomComparison': "", 'Filter': ""}]

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
        self.row_info_list.append({'MainComparison': "", 'Subgroup': "", 'CustomComparison': "", 'Filter': ""})

    def remove_a_row2(self):
        if len(self.row_list) > 0:
            self.ids.container.remove_widget(self.row_list[0])
            del self.row_list[0]

class ComparisonTableRow(BoxLayout):
    id_number2 = StringProperty()
    # TODO use to update kivy
    def update_row_info(self):
        key_vals = {'MainComparison': "" if self.ids.subgroup.text == "MainComparison" else self.ids.main_comparison.text,
                    'Subgroup': "" if self.ids.subgroup.text == "Subgroup" else self.ids.subgroup.text,
                    'CustomComparison': self.ids.custom_comparison.text,
                    'Filter': self.ids.filter.text}
        ComparisonTable.row_info_list[int(self.id_number2)] = key_vals
        print(ComparisonTable.row_info_list[int(self.id_number2)])

# Colors
# todo Henry
"""
Colors 
Issues:
- color tab doesn't display all values when CCButton inherits BoxLayout but does when it inherits Button
- however, when it inherits Button, it doesn't change color (current) - try swtich to BoxLayout
- displaying all row_Ann_vals with RecycleView
"""
# https://stackoverflow.com/questions/58862489/how-can-i-call-an-on-pre-enter-function-in-kivy-for-my-root-screen
# randomize colors https://www.youtube.com/watch?v=OkW-1uzP5Og
# import random
# color = [random.random() for i in xrange(3)] + [1]
# Customize colors
class CustomizeColors(RecycleView):
    # Make a list of unique main and subgroup comparisons (ie. rowAnn column names) that are not ""
    rowAnn_cols = list(
        set([x["MainComparison"] for x in ComparisonTable.row_info_list if x["MainComparison"] != ""] +
            [x["Subgroup"] for x in ComparisonTable.row_info_list if x["Subgroup"] != ""]))

    if ds.rowAnn is not None:
        # Make a list of unique values in each rowAnn column
        rowAnn_vals = [set(ds.rowAnn[x]) for x in rowAnn_cols if x in ds.rowAnn.columns]

        # If a custom_column is specified, make a set
        custom_cols = set(item["CustomComparison"] for item in ComparisonTable.row_info_list if item["CustomComparison"] != "")

        # If this set has a length greater than 0, append the levels (low/int/high) values to values list
        if len(custom_cols) > 0:
            rowAnn_cols.append("CustomComparison")
            rowAnn_vals.append({"low", "int", "high"})
        print(rowAnn_cols)
        print(rowAnn_vals)

        def __init__(self, **kwargs):
            super(CustomizeColors, self).__init__(**kwargs)
            self.data = [{'rowAnn_col': str(x)} for x in self.rowAnn_cols]
            # self.data = [{'row_id': i for i in range(len(self.rowAnn_cols))}]
            #
            # for i in range(0, 10):
            #     layout.add_widget(CCButton(rowAnn_val=str(i)))

class ColorPopup(Popup):
    load = ObjectProperty()

class CCBoxlayout(BoxLayout):
    row_id = ""
    # rowAnn_col = CustomizeColors.rowAnn_cols[int(row_id)]
    # rowAnn_vals = [CustomizeColors.rowAnn_vals[int(row_id)]]
    rowAnn_col = StringProperty()

class CCButton(BoxLayout): # If this inherits Button, no overlap but it crashes when we pick color; If we make this BoxLayout, the color picker works but Value1 and Value2 overlap
    the_popup = ObjectProperty(None)
    rowAnn_val = StringProperty()
    rowAnn_val_color = StringProperty()

    # declaring the colours you can use directly also
    red = [1, 0, 0, 1]
    green = [0, 1, 0, 1]
    blue = [0, 0, 1, 1]
    purple = [1, 0, 1, 1]
    # creating the list of defined colors
    colors = [red, green, blue, purple]

    button_color = random.choice(colors) #rgba("#ffffff")

    def open_popup(self):
        self.the_popup = ColorPopup(load=self.load)
        self.the_popup.open()

    def load(self, colorpicker, *args):
        self.rowAnn_val_color = str(colorpicker.hex_color)[1:]
        self.the_popup.dismiss()

        # check for non-empty list i.e. file selected and change button text
        if self.rowAnn_val_color:
            self.ids.color_button.background_color = str(self.rowAnn_val_color)
        print(self.rowAnn_val_color)

# Make Groups ---
class MakeGroups(Widget):
    pass

class MakeGroupsTab1(BoxLayout):
    id_number = -1
    # Initialize list
    row_list = []
    row_info_list = []

    # # # Simulate list
    row_info_list = [{'GroupName': "T Cell Markers", 'GroupList': "Gene1, Gene2, Gene3"},
                     {'GroupName': "B Cell Markers", 'GroupList': "Gene4,Gene5, Gene6, Gene7"},
                     {'GroupName': "Immune Cell Markers", 'GroupList': "B Cell Markers, T Cell Markers"},
                     {'GroupName': "ECM Markers", 'GroupList': "Gene24, Gene27, Gene35"}]

    def add_a_row(self):
        # Update ID number
        self.id_number += 1
        # Make current row
        curr_row = MakeGroupsTab1Row(id_number2=str(self.id_number))
        # Add to list of ComparisonTableRow objects
        self.row_list.append(curr_row)
        # Add row widget
        self.ids.container.add_widget(curr_row)
        # # Make a list of dict objects (dict object = row info)
        self.row_info_list.append({'GroupName': "", 'GroupList': ""})

class MakeGroupsTab1Row(BoxLayout):
    id_number2 = StringProperty()

    # TODO use to update kivy
    def update_row_info(self):
        key_vals = {
            'GroupName': self.ids.group_name.text,
            'GroupList': self.ids.group_list.text}

        MakeGroupsTab1.row_info_list[int(self.id_number2)] = key_vals
        print(MakeGroupsTab1.row_info_list[int(self.id_number2)])

class MakeGroupsTab2(RecycleView):
    colAnn_feature_col = StringProperty() # 'Gene.Sym'  # replace with correct drop down menu selection

    # all_features = []
    #
    # for x in MakeGroupsTab1.row_info_list:
    #     # String split by comma
    #     x = x["GroupList"].split(',')
    #     # Trim white space
    #     x = [x_sub.strip() for x_sub in x]
    #     # Genes present in colAnn
    #     # x = [y for y in x if y in ds.colAnn[self.ids.colAnn_feature_col].values]
    #     # Append to list
    #     all_features = all_features + x
    #
    # # Unique feature list
    # all_features = list(set(all_features))

    all_features = ["Gene A", "Gene B", "Gene C", "Gene ", "Gene C", "Gene B", "Gene C", "Gene B"]

    # Add a boxlayout with label for Gene and 2 textInputs
    def __init__(self, **kwargs):
        super(MakeGroupsTab2, self).__init__(**kwargs)
        self.data = [{'label_text': str(x)} for x in self.all_features]

class MakeGroupsTab2Label(BoxLayout):
    label_text = StringProperty()

# Custom widgets ---
class CustomCheckbox(BoxLayout):
    label_text = StringProperty()
    check_box = BooleanProperty()

    def on_checkbox_active(checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active')
        else:
            print('The checkbox', checkbox, 'is inactive')
class CustomSpinner(BoxLayout):
    label_text = StringProperty()
    spinner_list = ListProperty()
    initial_option = StringProperty()
    id_parameter = StringProperty()
    ann = StringProperty('')# todo

    # Print selection to console
    def clicked(self, key, value):
        # p.update(self, "mat", value)
        print_hourglass_parameter(key, value)

    # Update column annotations
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_clock, 5)

    def update_clock(self, *args):
        if self.ann == 'rowAnn':
            self.spinner_list = HourglassApp.getRowAnnCols(self)
        elif self.ann == 'colAnn':
            self.spinner_list = HourglassApp.getColAnnCols(self)
        else:
            pass

class SpinnerLabel(Label):
    pass

# Adv options ---
class AdvancedOptions(Widget):
    def correlation_clicked(self, value):
        self.correlation = f'{value}'
        # self.ids.correlation_label.text = f'{value}'

    def pvaltest_clicked(self, value):
        self.pvaltest = f'{value}'
        # self.ids.pvaltest_label.text = f'{value}'

    def pvallabel_clicked(self, value):
        self.pvallabel = f'{value}'
        # self.ids.pvallabel_label.text = f'{value}'

class RunHourglass(Widget):
    def runHourglass(self):
        pass # button to  interface with R, pass hourglass parameters, table and data filepaths

def print_hourglass_parameter(key, value):
    print(key, ":", value)

class KVTabLay(Widget):
    comp_table1 = ObjectProperty()
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

    def build(self):
        Window.clearcolor = (1,1,1,1)
        return KVTabLay()

if __name__ == '__main__':
    HourglassApp().run()
