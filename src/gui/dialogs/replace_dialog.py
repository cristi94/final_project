import wx


class ReplaceDialog(wx.TextEntryDialog):
    def __init__(self, parent, message, caption, def_val):
        super().__init__(parent, message, caption)
        self.SetValue(def_val)
