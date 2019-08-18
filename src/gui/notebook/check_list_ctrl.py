from wx.lib.mixins.listctrl import CheckListCtrlMixin
import wx


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin):
    def __init__(self, parent, workset_controller):
        super().__init__(parent, -1, style=wx.LC_REPORT)
        CheckListCtrlMixin.__init__(self)
        workset_controller.set_training_attr_view(self)
        self.workset_controller = workset_controller

        self.InsertColumn(0, "Name")
        self.InsertColumn(1, "Data Type")

    def populate(self):
        self.DeleteAllItems()
        df = self.workset_controller.get_df()
        dtypes = df.dtypes
        for index, items in enumerate(dtypes.iteritems()):
            self.InsertItem(index, items[0])
            self.SetItem(index, 1, str(items[1]))

    def get_selected(self):
        selected = list()
        for index in range(self.GetItemCount()):
            if self.IsChecked(index):
                selected.append(self.GetItem(index).GetText())
        return selected
