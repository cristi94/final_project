import wx


class Logger(wx.TextCtrl):
    def __init__(self, parent):
        super().__init__(parent, -1, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL, size=(-1, 200))
        wx.Log.SetActiveTarget(wx.LogTextCtrl(self))

    def write(self, text):
        self.WriteText(text)
        self.WriteText("\n")
