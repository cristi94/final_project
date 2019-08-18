import pandas as pd
import wx.lib.agw.customtreectrl as CT


class DfTreeCtrl(CT.CustomTreeCtrl):
    def __init__(self, parent):
        super().__init__(parent, agwStyle=CT.TR_DEFAULT_STYLE | CT.TR_AUTO_CHECK_CHILD)

    def populate(self, root_name, df):
        root = self.AddRoot(root_name, ct_type=1)
        root.Expand()
        for attr_name in df.columns:
            attr_item = self.AppendItem(root, attr_name, ct_type=1)
            series = df[attr_name]
            if series.dtype == 'object':
                for attr_val in series.unique().tolist():
                    self.AppendItem(attr_item, str(attr_val), ct_type=1)
        self.CheckItem(root, True)

    def get_columns(self):
        root = self.GetRootItem()
        columns_dict = dict()
        for col in root.GetChildren():
            if col.IsChecked():
                columns_dict[col.GetText()] = []
                for attr in col.GetChildren():
                    if attr.IsChecked():
                        columns_dict[col.GetText()].append(attr.GetText())
        return columns_dict
