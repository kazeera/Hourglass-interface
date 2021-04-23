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


class GridLay(GridLayout):
    def __init__(self, **kwargs):
        super(). __init__(**kwargs)

        self.cols = 2
        self.add_widget(Label(text='Numeric Matrix'))
        self.button = Button(text='Upload File')
        self.add_widget(self.button)
        self.add_widget(Label(text='Row Annotations'))
        self.button = Button(text='Upload File')
        self.add_widget(self.button)
        self.add_widget(Label(text='Column Annotations'))
        self.button = Button(text='Upload File')
        self.add_widget(self.button)

class TabbedLay(TabbedPanel):
    def __init__(self, **kwargs):
        super(). __init__(**kwargs)

        self.table = GridLay()

        self.do_default_tab = False
        self.default_tab_text = "Welcome to Hourglass"
        self.default_tab_content = (Label(text='Welcome to Hourglass'))
        self.tab_width = 300
        self.tab_height = 75

        self.tab1 = TabbedPanelItem()
        self.tab1.text = 'Upload Data'
        self.tab1.content = self.table
        self.add_widget(self.tab1)

        self.tab2 = TabbedPanelItem()
        self.tab2.text = 'Pick Comparisons'
        self.tab2Button = Button(text='Button', font_size=24)
        self.tab2.content = self.tab2Button
        self.tab2Header = Label(text='Tab 2')
        self.add_widget(self.tab2)

        self.tab3 = TabbedPanelItem()
        self.tab3.text = 'Make Groups'
        self.add_widget(self.tab3)

        self.tab4 = TabbedPanelItem()
        self.tab4.text = 'Customize Colours'
        self.add_widget(self.tab4)

        self.tab5 = TabbedPanelItem()
        self.tab5.text = 'Customize Stats'
        self.add_widget(self.tab5)

        self.tab6 = TabbedPanelItem()
        self.tab6.text = 'Data Explorer'
        self.add_widget(self.tab6)




class CustomDropDown(DropDown):
    pass

class UploadTable(Widget):
    pass

class ComparisonTable(Widget):
    pass

class CustomizeStats(Widget):
    def spinner_clicked(self, value):
        self.ids.correlation_label.text = f'{value}'

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
