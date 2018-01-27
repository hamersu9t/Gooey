from gooey.gui.components.widgets.bases import TextContainer
import wx

from gooey.gui import formatters


class Dropdown(TextContainer):

    def getWidget(self, parent, *args, **options):
        default = 'Select Option'
        return wx.ComboBox(
            parent=parent,
            id=-1,
            value=default,
            choices=[default] + self._meta['choices'],
            style=wx.CB_DROPDOWN)

    def setOptions(self, options):
        prevSelection = self.widget.GetSelection()
        self.widget.Clear()
        for option in ['Select Option'] + options:
            self.widget.Append(option)
        self.widget.SetSelection(0)


    def setValue(self, value):
        ## +1 to offset the default placeholder value
        index = self._meta['choices'].index(value) + 1
        self.widget.SetSelection(index)

    def getWidgetValue(self):
        return self.widget.GetValue()

    def formatOutput(self, metadata, value):
        return formatters.dropdown(metadata, value)
