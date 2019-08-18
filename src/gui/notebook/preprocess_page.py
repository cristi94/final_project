import wx
from gui.df_list_ctrl import DataFrameListCtrl
from gui.attributes_list_ctrl import AttributesListCtrl
from wx.lib.intctrl import IntCtrl


class PreprocessPage(wx.Panel):
    def __init__(self, parent, workset_controller):
        super().__init__(parent, id=wx.ID_ANY)
        self.workset_controller = workset_controller
        self.df_list_ctrl = None
        self.attributes_list_ctrl = None
        self.attribute_choice = None

        box1 = self.create_preview_df_box()
        box2 = self.create_attr_viewer_box()

        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(box1, 1, wx.EXPAND)
        border.Add(box2, 1, wx.EXPAND)
        self.SetSizer(border)

        self.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.on_combo_dropdown)
        self.Bind(wx.EVT_COMBOBOX, self.on_choice)

    def create_attr_viewer_box(self):
        st_box = wx.StaticBox(self, -1, "Attribute Viewer")
        top_border, other_border = st_box.GetBordersForSizer()
        box_sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_sizer = self.create_left_sizer(parent=st_box, border=other_border)

        self.attributes_list_ctrl = AttributesListCtrl(st_box, self.workset_controller)
        list_ctrl_sizer = wx.BoxSizer(wx.VERTICAL)
        list_ctrl_sizer.Add(self.attributes_list_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, other_border)

        box_sizer.Add(left_sizer, 0, wx.TOP, top_border)
        box_sizer.Add(list_ctrl_sizer, 1, wx.EXPAND | wx.TOP, top_border)
        st_box.SetSizer(box_sizer)
        return st_box

    def create_preview_df_box(self):
        st_box = wx.StaticBox(self, -1, "Preview Dataframe")
        top_border, other_border = st_box.GetBordersForSizer()
        box_sizer = wx.BoxSizer(wx.VERTICAL)
        box_sizer.AddSpacer(top_border)

        df_head = self.create_df_head(parent=st_box)
        self.df_list_ctrl = DataFrameListCtrl(st_box, self.workset_controller)

        box_sizer.Add(df_head, 0, wx.BOTTOM | wx.LEFT | wx.RIGHT, other_border)
        box_sizer.Add(self.df_list_ctrl, 1, wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, other_border)
        st_box.SetSizer(box_sizer)
        return st_box

    def create_left_sizer(self, parent, border):
        st1 = wx.StaticText(parent, -1, "Choose column ")

        self.attribute_choice = wx.ComboBox(parent, -1, choices=["All"], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.attribute_choice.SetSelection(0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st1, 0, wx.LEFT | wx.RIGHT | wx.DOWN, border)
        sizer.Add(self.attribute_choice, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN, border)

        return sizer

    def on_combo_dropdown(self, evt):
        old_val = self.attribute_choice.GetValue()
        df = self.workset_controller.get_df()
        choices = list(["All"])
        choices = choices + list(df.columns)
        self.attribute_choice.SetItems(choices)
        self.attribute_choice.SetValue(old_val)

    def on_choice(self, e):
        column = e.GetString()
        self.workset_controller.refresh_attr_view(column)

    def create_df_head(self, parent):
        rb1 = wx.RadioButton(parent, 11, label="Head", style=wx.RB_GROUP)
        rb2 = wx.RadioButton(parent, 22, label="Tail")
        l1 = wx.StaticText(parent, -1, "No. of records: ")
        tc1 = IntCtrl(parent, -1, value=5, size=(40, -1), style=wx.TE_PROCESS_ENTER, min=1, max=50)
        tc1.Bind(wx.EVT_TEXT_ENTER, self.on_records_no)

        df_filter_sizer = wx.BoxSizer(wx.HORIZONTAL)
        df_filter_sizer.Add(rb1)
        df_filter_sizer.Add(rb2)
        df_filter_sizer.Add(l1)
        df_filter_sizer.Add(tc1)
        return df_filter_sizer

    def get_df_view(self):
        return self.df_list_ctrl

    def get_attr_view(self):
        return self.attributes_list_ctrl

    def on_records_no(self, e):
        rows_no = e.GetEventObject()
        df_controller = self.workset_controller
        df_controller.set_df_view_no_of_rows(int(rows_no.GetValue()))
        df_controller.refresh_df_view()
