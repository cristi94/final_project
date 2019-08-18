import wx
import os


class FileDialog(wx.FileDialog):
    def __init__(self, parent, message, style):
        wildcard = "CSV files (*.csv)|*.csv"
        # style = wx.FD_OPEN
        super().__init__(parent=parent, message=message, defaultDir=os.getcwd(), wildcard=wildcard, style=style)
