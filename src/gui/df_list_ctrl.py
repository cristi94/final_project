import wx
from gui.dialogs.column_creator_dialog import ColumnCreatorDialog


class DataFrameListCtrl(wx.ListCtrl):
    def __init__(self, parent, workset_controller):
        super().__init__(parent, wx.ID_ANY, style=wx.LC_REPORT)
        workset_controller.set_df_view(self)
        self.workset_controller = workset_controller
        self.Bind(wx.EVT_LIST_COL_CLICK, self.on_activated)

    def populate(self, df):
        self.create_columns(df.columns)
        self.create_records(df)

    def create_columns(self, columns):
        for i, col in enumerate(columns):
            self.InsertColumn(i, col)
        self.AppendColumn('Add New Col')

    def create_records(self, df):
        for row_index, (index, row) in enumerate(df.iterrows()):
            for col_index, value in enumerate(row):
                if col_index == 0:
                    self.InsertItem(row_index, str(row[0]))
                else:
                    if type(value) == int:
                        value = str(value)
                    elif self.is_val_float(value):
                        value = float(value)
                        value = "{0:.2f}".format(round(value, 2))
                    self.SetItem(row_index, col_index, value)
        # self.SetItem(0, column=self.GetColumnCount()-1, label='Add')

    def clear(self):
        self.DeleteAllItems()
        self.DeleteAllColumns()

    def on_activated(self, e):
        if e.GetColumn() == self.GetColumnCount() - 1:
            dlg = ColumnCreatorDialog(self, "Create new columns below:", "New column editor")
            if dlg.ShowModal() == wx.ID_OK:
                self.workset_controller.add_feature(dlg.get_value())
                # df_controller = self.workset_controller
                # df = df_controller.get_df()
                # for line in dlg.get_value().splitlines():
                #     exec(line)
                # df_controller.set_df(df)
                # df_controller.refresh_df_view()

    @staticmethod
    def is_val_float(element):
        try:
            float(element)
            return True
        except ValueError:
            return False
