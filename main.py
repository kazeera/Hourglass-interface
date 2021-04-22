from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.uix.widget import Widget



class CustomDropDown(DropDown):
    pass

class UploadTable(Widget):
    pass

class ComparisonTable(Widget):
    pass

class CustomizeStats(Widget):
    def correlation_clicked(self, value):
        self.ids.correlation_label.text = f'{value}'

    def test_clicked(self, value):
        self.ids.test_label.text = f'{value}'

class KVTabLay(Widget):
    pass



class HourglassApp(App):
    def build(self):

        # dropdown = CustomDropDown()
        # mainbutton = Button(text='Select',size_hint = (0.5,0.1))
        #                     #pos_hint = (0.5, 0.5)?
        # mainbutton.bind(on_release=dropdown.open)
        # dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        return KVTabLay()

if __name__ == '__main__':
    HourglassApp().run()

#Test Change - Bowen