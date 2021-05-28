# https://www.reddit.com/r/kivy/comments/ejgfaq/accessing_functions_from_other_classes_in_kv_file/
# http://inclem.net/2019/06/20/kivy/widget_interactions_between_python_and_kv/
# https://kivy.org/doc/stable/api-kivy.clock.html

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty, ListProperty, DictProperty
import pandas as pd
import numpy as np
import dill
from functions import *

class hourglassParameters():
    name = None
    filepath_matrix = None  # numeric matrix
    filepath_rowAnn = None  # describes rows of matrix
    filepath_colAnn = None  # describes columns of matrix
    comparisons_table = None
    correlation_method = None
    
    def __init__(self):
        pass

class Dataset:
    name = None
    mat = None  # numeric matrix
    rowAnn = None  # describes rows of matrix
    colAnn = None  # describes columns of matrix

    def __init__(self):
        pass

p = hourglassParameters()
ds = Dataset()
dill.load_session("dataset.pkl")
# list(set(ds.rowAnn["Smoker"]))


# Upload Files ---
class UploadTable(Widget):
    # ds.name = self.ids.datasetName
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
        if self.id_parameter == "filepath_matrix":
            p.filepath_matrix = self.file_path
            ds.colAnn = read_tbl(self.file_path)

        ## Update dataset object
        print_hourglass_parameter(self.id_parameter, self.file_path) # TODO we can update our dataset object here

    global currentButton # TODO has to be global?
    currentButton = 'String'

    def whats_the_button(self, button):
        global currentButton
        currentButton = button

# Comparisons Table ---
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
        self.row_info_list.append({'MainComparison': "NA", 'Subtype': "NA", 'CustomComparison': "NA", 'Filter': "NA"})

    def remove_a_row2(self):
        if len(self.row_list) > 0:
            self.ids.container.remove_widget(self.row_list[0])
            del self.row_list[0]

class ComparisonTableRow(BoxLayout):
    id_number2 = StringProperty()


    def update_row_info(self):
        key_vals = {'MainComparison': self.ids.main_comparison.text,
                    'Subtype': self.ids.subgroup.text,
                    'CustomComparison': self.ids.custom_comparison.text,
                    'Filter': self.ids.filter.text}
        ComparisonTable.row_info_list[int(self.id_number2)] = key_vals
        print(ComparisonTable.row_info_list[int(self.id_number2)])

# Make Groups ---
class MakeGroups(Widget):
    pass

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

    def clicked(self, key, value):
        # p.update(self, "mat", value)
        print_hourglass_parameter(key, value)

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

def getRowAnnCols(self):
    if ds.rowAnn is None:
        return ""
    else:
        return [""] + list(ds.rowAnn.columns.values) # ["", "Smoker", "Age", "Survival.Time", "OS.Status"]

def getColAnnCols(self):
    if ds.rowAnn is None:
        return ""
    else:
        return [""] + list(ds.colAnn.columns.values) # ["GeneSym", "GeneID", "Parameter"]

class HourglassApp(App):
    text_size = 19

    def getRowAnnCols(self):
        if ds.rowAnn is None:

            return ''
        else:
            return [""] + list(ds.rowAnn.columns.values)

    def getColAnnCols(self):
        if ds.colAnn is None:
            return ''
        else:
            return [""] + list(ds.colAnn.columns.values)


    def build(self):
        return KVTabLay()

if __name__ == '__main__':
    HourglassApp().run()
