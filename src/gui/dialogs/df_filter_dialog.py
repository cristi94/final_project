import wx


class DfFilterDialog(wx.Dialog):
    def __init__(self, parent, def_name, def_val):
        super().__init__(parent, title="Choose data for new dataframe",
                         style=wx.DEFAULT_DIALOG_STYLE)

        box_sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "Select attributes / values for new dataframe:")

        hbox_sizer = wx.BoxSizer(wx.HORIZONTAL)

        main_frame = self.GetParent().GetParent().GetParent().GetParent().GetParent()
        df_controller = main_frame.get_workset_controller()
        choices = df_controller.get_columns_list()

        self.name_ch = wx.Choice(self, -1, choices=choices)
        self.name_ch.SetSelection(choices.index(def_name))
        hbox_sizer.Add(self.name_ch, wx.ALL | wx.ALIGN_LEFT, 5)

        self.op_ch = wx.Choice(self, -1, choices=['=', '<=', '<', '>=', '>', '!='])
        self.op_ch.SetSelection(0)
        hbox_sizer.Add(self.op_ch, wx.ALL | wx.ALIGN_CENTER, 5)

        self.val_box = wx.TextCtrl(self, -1)
        self.val_box.SetValue(def_val)
        hbox_sizer.Add(self.val_box, wx.ALL | wx.ALIGN_RIGHT, 5)

        button_sizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        box_sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        box_sizer.Add(hbox_sizer, 0, wx.ALL, 10)
        box_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALIGN_BOTTOM)

        self.SetSizer(box_sizer)

    def get_ans(self):
        return self.get_name_ch(), self.get_op_ch(), self.get_val()

    def get_op_ch(self):
        return self.op_ch.GetString(self.op_ch.GetSelection())

    def get_name_ch(self):
        return self.name_ch.GetString(self.name_ch.GetSelection())

    def get_val(self):
        return self.val_box.GetValue()
