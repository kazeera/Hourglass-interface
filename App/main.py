from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.base import runTouchApp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox

class UploadTable(Widget):
    pass

class ComparisonTableRow(BoxLayout):
    pass

class ComparisonTable(BoxLayout):
    def add_a_row(self):
        self.ids.container.add_widget(ComparisonTableRow())

class OptionsCheckBox(CheckBox):
    def on_checkbox_active(checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active')
        else:
            print('The checkbox', checkbox, 'is inactive')

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


class KVTabLay(Widget):
    pass


class HourglassApp(App):
    def build(self):
        return KVTabLay()

if __name__ == '__main__':
    HourglassApp().run()
