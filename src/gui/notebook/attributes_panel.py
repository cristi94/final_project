import wx


class AttributesPanel(wx.Window):
    def __init__(self, parent):
        super().__init__(parent, size=(50,50))
        self.SetBackgroundColour("red")

