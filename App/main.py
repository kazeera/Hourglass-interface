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

class UploadTable(Widget):
    pass

class ComparisonTableRow(BoxLayout):
    pass

class ComparisonTable(BoxLayout):
    def add_a_row(self):
        self.ids.container.add_widget(ComparisonTableRow())

class AdvancedOptions(Widget):
    def correlation_clicked(self, value):
        self.ids.correlation_label.text = f'{value}'

    def test_clicked(self, value):
        self.ids.test_label.text = f'{value}'


class KVTabLay(Widget):
    pass


class HourglassApp(App):
    def build(self):
        return KVTabLay()

if __name__ == '__main__':
    HourglassApp().run()
