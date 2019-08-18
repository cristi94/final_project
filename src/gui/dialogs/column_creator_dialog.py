import wx


class ColumnCreatorDialog(wx.Dialog):
    def __init__(self, parent, title, caption=None):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super().__init__(parent, -1, title, style=style)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.tc = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        self.tc.SetValue("df['new_col'] = ")
        button_sizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(self.tc, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)

    def get_value(self):
        return self.tc.GetValue()
