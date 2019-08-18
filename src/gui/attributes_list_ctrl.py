import wx
import numpy as np
from gui.dialogs.replace_dialog import ReplaceDialog
from gui.dialogs.df_filter_dialog import DfFilterDialog
from gui.frames.plot_frame import PlotFrame


class AttributesListCtrl(wx.ListCtrl):
    def __init__(self, parent, workset_controller):
        super().__init__(parent, wx.ID_ANY, style=wx.LC_REPORT)
        workset_controller.set_attr_view(self)
        self.workset_controller = workset_controller
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_context_menu)
        self.state = None
        self.popupID1 = None
        self.popupID2 = None
        self.popupID3 = None
        self.popupID4 = None
        self.popupID5 = None
        self.popupID6 = None
        self.popupID7 = None
        self.popupID8 = None
        self.popupID9 = None
        self.popupID10 = None
        self.popupID11 = None
        self.popupID12 = None
        self.old_value = None
        self.series_name = None

    def clear(self):
        self.DeleteAllItems()
        self.DeleteAllColumns()

    def populate_df(self, df):
        self.state = 'df'
        self.create_columns(df)
        self.create_rows(df)

    def populate_series(self, series):
        self.state = 'series'
        self.series_name = series.name
        self.InsertColumn(0, 'Value')
        self.InsertColumn(1, 'Count')
        self.SetColumnWidth(0, 200)
        self.create_rows(series.to_frame())

    def create_columns(self, column_list):
        self.InsertColumn(0, 'Statistics')
        for i, col in enumerate(column_list):
            self.InsertColumn(i+1, col)

    def create_rows(self, df):
        def remove_decimals(number):
            if type(number) == np.float64:
                number = '{0:.2f}'.format(number)
            return str(number)
        for i in range(len(df)):
            self.InsertItem(i, str(df.index[i]))
            for col_index, col in enumerate(df.columns):
                value = remove_decimals((df.loc[df.index[i], col]))
                self.SetItem(i, col_index+1, value)

    def on_context_menu(self, e):
        if self.state == 'series':
            if self.popupID1 is None:
                self.popupID1 = wx.NewIdRef()
                self.Bind(wx.EVT_MENU, self.on_replace, id=self.popupID1)
                self.popupID2 = wx.NewIdRef()
                self.Bind(wx.EVT_MENU, self.on_create_new_df, id=self.popupID2)
                self.popupID3 = wx.NewIdRef()
                self.Bind(wx.EVT_MENU, self.on_remove_missing_vals, id=self.popupID3)
                self.popupID4 = wx.NewIdRef()
                self.Bind(wx.EVT_MENU, self.on_bar_plot, id=self.popupID4)
                self.popupID5 = wx.NewIdRef()
                self.Bind(wx.EVT_MENU, self.on_create_dummies, id=self.popupID5)
                self.popupID6 = wx.NewIdRef()
                self.Bind(wx.EVT_MENU, self.on_replace_all_others, id=self.popupID6)
                self.popupID7 = wx.NewIdRef()
                self.Bind(wx.EVT_MENU, self.on_box_plot, id=self.popupID7)
                self.popupID8 = wx.NewIdRef()
                self.Bind(wx.EVT_MENU, self.on_plot_hist, id=self.popupID8)
                self.popupID9 = wx.NewIdRef()
                self.Bind(wx.EVT_MENU, self.on_plot_violin, id=self.popupID9)
                self.popupID10 = wx.NewIdRef()
                self.Bind(wx.EVT_MENU, self.on_plot_corr_mat, id=self.popupID10)
                self.popupID11 = wx.NewIdRef()
                self.Bind(wx.EVT_MENU, self.on_encode, id=self.popupID11)
                self.popupID12 = wx.NewIdRef()

            self.old_value = e.GetItem().GetText()

            menu = wx.Menu()
            menu.Append(self.popupID1, "Replace value")
            menu.Append(self.popupID6, "Replace all but value")
            menu.Append(self.popupID11, "Encode labels")
            menu.Append(self.popupID2, "Select for a new dataframe")
            menu.Append(self.popupID5, "Convert to dummy variables")

            df = self.workset_controller.get_df()

            if df[self.series_name].isnull().values.any():
                submenu = wx.Menu()
                submenu.Append(self.popupID3, "Remove")
                submenu.Append(self.popupID4, "Replace")
                menu.AppendSubMenu(submenu, "Missing Values")

            submenu = wx.Menu()
            submenu.Append(self.popupID8, "Histogram")
            submenu.Append(self.popupID7, "Box Plot")
            # submenu.Append(self.popupID9, "Violin Plot")
            submenu.Append(self.popupID4, "Bar Plot")
            submenu.Append(self.popupID10, "Correlation Matrix")

            boxplot_with_sm = wx.Menu()
            barplot_with_sm = wx.Menu()
            df = self.workset_controller.get_df()
            features = list(df.columns)
            for feature in features:
                item = wx.MenuItem(boxplot_with_sm, wx.ID_ANY, feature)
                boxplot_with_sm.Append(item)
                self.Bind(wx.EVT_MENU, self.on_box_plot_with, item)
                item = wx.MenuItem(barplot_with_sm, wx.ID_ANY, feature)
                barplot_with_sm.Append(item)
                self.Bind(wx.EVT_MENU, self.on_bar_plot_with, item)

            submenu.AppendSubMenu(boxplot_with_sm, "Box Plot with")
            submenu.AppendSubMenu(barplot_with_sm, "Bar Plot with")

            menu.AppendSubMenu(submenu, "Plot")

            self.PopupMenu(menu)
            menu.Destroy()
            self.old_value = None

    def on_encode(self, evt):
        self.workset_controller.encode_labels(column=self.series_name)

    def on_replace(self, evt):
        replace_dialog = ReplaceDialog(self, "Enter new value:", "Replace Value", def_val="")
        if replace_dialog.ShowModal() == wx.ID_OK:
            self.workset_controller.replace(new_val=replace_dialog.GetValue(), old_val=self.old_value,
                                            col=self.series_name)
        replace_dialog.Destroy()

    def on_create_new_df(self, evt):
        df_filter_dlg = DfFilterDialog(self, def_name=self.series_name, def_val=self.old_value)

        if df_filter_dlg.ShowModal() == wx.ID_OK:
            name, op, val = df_filter_dlg.get_ans()
            self.workset_controller.update_df(name, op, val)
        df_filter_dlg.Destroy()

    def on_remove_missing_vals(self, evt):
        self.workset_controller.remove_nans(self.series_name)

    def on_create_dummies(self, evt):
        self.workset_controller.create_dummies(self.series_name)

    def on_replace_all_others(self, evt):
        replace_dialog = ReplaceDialog(self, "Enter new value:", "Replace Values", def_val="")
        if replace_dialog.ShowModal() == wx.ID_OK:
            old_vals = list()
            for item_idx in range(self.GetItemCount()):
                old_value = self.GetItem(item_idx, col=0).GetText()
                if old_value != self.old_value:
                    old_vals.append(old_value)
            self.workset_controller.replace_all_others(new_val=replace_dialog.GetValue(), old_vals=old_vals,
                                                       col=self.series_name, kept_val=self.old_value)
        replace_dialog.Destroy()

    def on_box_plot(self, evt):
        df = self.__get_dataframe()

        win = PlotFrame(self, -1, self.series_name, size=(400, 400), style=wx.DEFAULT_FRAME_STYLE)
        win.plot_boxplot(df, self.series_name)
        win.Show()

    def on_box_plot_with(self, evt):
        menu_id = evt.GetId()
        obj = evt.GetEventObject()
        feature = obj.GetLabelText(menu_id)
        df = self.__get_dataframe()
        win = PlotFrame(self, -1, "Box plot", size=(400, 400), style=wx.DEFAULT_FRAME_STYLE)
        win.plot_boxplot_with(df, self.series_name, feature)
        win.Show()

    def on_bar_plot(self, evt):
        df = self.__get_dataframe()

        win = PlotFrame(self, -1, "Bar Plot", size=(400, 400), style=wx.DEFAULT_FRAME_STYLE)
        win.plot_barplot(df, self.series_name)
        win.Show()

    def on_bar_plot_with(self, evt):
        menu_id = evt.GetId()
        obj = evt.GetEventObject()
        feature = obj.GetLabelText(menu_id)
        df = self.__get_dataframe()
        win = PlotFrame(self, -1, "Bar plot", size=(400, 400), style=wx.DEFAULT_FRAME_STYLE)
        win.plot_barplot_with(df, self.series_name, feature)
        win.Show()

    def on_plot_hist(self, evt):
        df = self.__get_dataframe()

        win = PlotFrame(self, -1, "Histogram", size=(500, 400), style=wx.DEFAULT_FRAME_STYLE)
        win.plot_hist(df, self.series_name)
        win.Show()

    def on_plot_violin(self, evt):
        df = self.__get_dataframe()

        win = PlotFrame(self, -1, "Violin Plot", size=(500, 400), style=wx.DEFAULT_FRAME_STYLE)
        win.plot_violin(df, self.series_name)
        win.Show()

    def on_plot_corr_mat(self, evt):
        df = self.__get_dataframe()
        win = PlotFrame(self, -1, "Correlation Matrix", size=(500, 400), style=wx.DEFAULT_FRAME_STYLE)
        win.plot_corr_mat(df)
        win.Show()

    def __get_dataframe(self):
        df = self.workset_controller.get_df()
        return df
