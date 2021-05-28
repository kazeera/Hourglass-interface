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
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, ListProperty, NumericProperty
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

    # NumericMatrix = ""
    # RowAnn = ""
    # ColAnn = ""

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
dill.load_session('dataset.pkl')
list(set(ds.rowAnn["Smoker"]))


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
            print(currentButton)

        # Update global variable containing
        # if currentButton == 'filepath_matrix':
        #     global NumericMatrix
        #     NumericMatrix = self.file_path
        # if currentButton == 'filepath_rowann':
        #     global RowAnn
        #     RowAnn = self.file_path
        # if currentButton == 'filepath_colann':
        #     global ColAnn
        #     ColAnn = self.file_path

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

    global currentButton
    currentButton = 'String'

    def whats_the_button(self, button):
        global currentButton
        currentButton = button

# Comparisons Table ---
class ComparisonTable(BoxLayout):
    id_number = -1
    # container = GridLayout()
    # Initialize list
    row_list = []

    def add_a_row(self):
        # Update ID number
        self.id_number += 1
        # Make current row
        curr_row = ComparisonTableRow(id_number2=str(self.id_number))
        # Add to list of ComparisonTableRow objects
        self.row_list.append(curr_row)
        # Add row widget
        for i in range(len(self.row_list)):
            self.ids.container.remove_widget(self.row_list[i])
        for i in range(len(self.row_list)):
            self.ids.container.add_widget(self.row_list[i])

    def remove_a_row2(self):
        self.ids.container.remove_widget(self.row_list[1])
        # for i in range(len(self.row_list)):
        #     self.ids.container.remove_widget(self.row_list[i])
        del self.row_list[1]
        # for i in range(len(self.row_list)):
        #     self.ids.container.add_widget(self.row_list[i])
        print(ComparisonTable.row_list)
        print(self.row_list)

    # def redraw_list(self):
    #     for i in range(len(self.row_list)):
    #         self.ids.container.remove_widget(self.row_list[i])
    #     for i in range(len(self.row_list)):
    #         self.ids.container.add_widget(self.row_list[i])
    #     print(ComparisonTable.row_list)

class ComparisonTableRow(BoxLayout):
    id_number2 = StringProperty()

    def current_row(self):
        print(self.id_number2)
        print(self.ids.main_comparison.text)
        print(self.ids.subgroup.text)
        print(self.ids.filter.text)

    def remove_a_row(self):
        # ComparisonTable.ids.container.remove_widget(ComparisonTable.row_list[int(self.id_number2)])
        # del ComparisonTable.row_list[self.id_number2]
        ComparisonTable.remove_a_row2(root.ComparisonTable.id_number)
        # ComparisonTable.remove_a_row2(ComparisonTable(), int(self.id_number2))





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
        self.correlation = f'{value}' # TODO We could make a new class called Options() and upload all the options to pass to R and make log file
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
    pass


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
