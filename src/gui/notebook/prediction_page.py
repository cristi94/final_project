from gui.notebook.check_list_ctrl import CheckListCtrl
import wx

MODELS = {
    0: "Conditional Logistic Regression - Binary Target",
    1: "Random Forest Regressor"
    # 2: "Multilayer Perceptron Network"
}


class PredictionPage(wx.Panel):
    def __init__(self, parent, workset_controller):
        super().__init__(parent, id=wx.ID_ANY)
        self.workset_controller = workset_controller
        self.target_choice = None
        self.classifier_output = None
        self.classifier_ch = None
        self.attr_check_list = None
        self.rad_btns = list()
        self.percentage_split_box = None

        box = self.create_classifier_box()
        h_sizer = self.create_horiz_sizer()

        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(box, 0, wx.EXPAND | wx.ALL, 5)
        border.Add(h_sizer, 1, wx.EXPAND)
        self.SetSizer(border)

        self.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.on_combo_dropdown)

    def create_horiz_sizer(self):
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_bsizer = self.create_left_sizer()
        box = self.create_output_box()
        h_sizer.Add(left_bsizer, 0, wx.EXPAND | wx.ALL, 5)
        h_sizer.Add(box, 1, wx.EXPAND | wx.ALL, 5)
        return h_sizer

    def create_output_box(self):
        box = wx.StaticBox(self, -1, "Classifier Output")
        top_border, other_border = box.GetBordersForSizer()
        bsizer = wx.BoxSizer(wx.VERTICAL)
        bsizer.AddSpacer(top_border)

        self.classifier_output = wx.TextCtrl(box, style=wx.TE_READONLY | wx.TE_MULTILINE)
        bsizer.Add(self.classifier_output, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN, other_border)

        box.SetSizer(bsizer)
        return box

    def create_left_sizer(self):
        box2 = self.create_attr_box()
        box3 = self.create_test_options_box()
        box4 = self.create_target_box()

        left_bsizer = wx.BoxSizer(wx.VERTICAL)
        left_bsizer.Add(box2, 1, wx.EXPAND)
        left_bsizer.Add(box3, 0, wx.EXPAND)
        left_bsizer.Add(box4, 0, wx.EXPAND | wx.ALIGN_BOTTOM)
        return left_bsizer

    def create_test_options_box(self):
        box3 = wx.StaticBox(self, -1, "Test options")
        top_border, other_border = box3.GetBordersForSizer()
        gsizer = wx.GridSizer(3, 2, 2, 2)

        rb1 = wx.RadioButton(box3, 111, label="Percentage split", style=wx.RB_GROUP)
        self.rad_btns.append(rb1)
        self.percentage_split_box = wx.TextCtrl(box3)
        self.percentage_split_box.SetValue("0.7")
        rb2 = wx.RadioButton(box3, 222, label="Cross-Validation")
        self.rad_btns.append(rb2)
        tc2 = wx.TextCtrl(box3)
        tc2.SetValue("10")
        rb3 = wx.RadioButton(box3, 333, label="Custom test set")
        self.rad_btns.append(rb3)
        b1 = wx.Button(box3, label="Add..")

        gsizer.Add(rb1, 0, wx.EXPAND | wx.TOP, top_border)
        gsizer.Add(self.percentage_split_box, 0, wx.EXPAND | wx.TOP, top_border)
        gsizer.Add(rb2, 0, wx.EXPAND)
        gsizer.Add(tc2, 0, wx.ALIGN_CENTER)
        gsizer.Add(rb3, 0, wx.EXPAND)
        gsizer.Add(b1, 0, wx.ALIGN_CENTER)

        bsizer = wx.BoxSizer(wx.VERTICAL)
        bsizer.Add(gsizer, 1, wx.LEFT | wx.RIGHT | wx.DOWN, other_border)
        box3.SetSizer(bsizer)
        return box3

    def create_attr_box(self):
        box = wx.StaticBox(self, -1, "Attributes")
        top_border, other_border = box.GetBordersForSizer()
        bsizer = wx.BoxSizer(wx.VERTICAL)
        bsizer.AddSpacer(top_border)

        self.attr_check_list = CheckListCtrl(box, self.workset_controller)

        bsizer.Add(self.attr_check_list, 1, wx.EXPAND | wx.ALL, 5)

        box.SetSizer(bsizer)
        return box

    def create_target_box(self):
        box = wx.StaticBox(self, -1, "Target")
        top_border, other_border = box.GetBordersForSizer()
        bsizer = wx.BoxSizer(wx.HORIZONTAL)

        choices = ['None']
        self.target_choice = wx.ComboBox(box, -1, choices=choices, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.target_choice.SetSelection(0)
        target_sizer = wx.BoxSizer(wx.VERTICAL)
        target_sizer.Add(self.target_choice, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, other_border)

        predict_btn = wx.Button(box, -1, "Predict")
        predict_btn.Bind(wx.EVT_BUTTON, self.on_predict)
        btn_sizer = wx.BoxSizer(wx.VERTICAL)
        btn_sizer.Add(predict_btn, 1, wx.LEFT | wx.BOTTOM, other_border)

        bsizer.Add(target_sizer, 1, wx.EXPAND | wx.TOP, top_border)
        bsizer.Add(btn_sizer, 1, wx.EXPAND | wx.ALIGN_RIGHT | wx.TOP, top_border)
        box.SetSizer(bsizer)
        return box

    def create_classifier_box(self):
        box = wx.StaticBox(self, -1, "Classifier")
        top_border, other_border = box.GetBordersForSizer()
        bsizer = wx.BoxSizer(wx.VERTICAL)
        bsizer.AddSpacer(top_border)

        choices = list(MODELS.values())
        self.classifier_ch = wx.Choice(box, -1, choices=choices)
        self.classifier_ch.SetSelection(0)

        bsizer.Add(self.classifier_ch, 1, wx.EXPAND | wx.ALL, 5)
        box.SetSizer(bsizer)
        return box

    def on_combo_dropdown(self, evt):
        old_val = self.target_choice.GetValue()
        df = self.workset_controller.get_df()
        choices = list(["None"])
        choices = choices + list(df.columns)
        self.target_choice.SetItems(choices)
        self.target_choice.SetValue(old_val)

    def on_predict(self, evt):
        if False:
            self.classifier_output.AppendText("Chosen model:")
            self.classifier_output.AppendText("\n")
            self.classifier_output.AppendText(self.classifier_ch.GetString(self.classifier_ch.GetSelection()))
            self.classifier_output.AppendText("\n")
            self.classifier_output.AppendText("\n")
            self.classifier_output.AppendText("Chosen features:")
            self.classifier_output.AppendText("\n")
            for feature in self.attr_check_list.get_selected():
                self.classifier_output.AppendText(feature)
                self.classifier_output.AppendText(" ")
            self.classifier_output.AppendText("\n")
            self.classifier_output.AppendText("\n")
            self.classifier_output.AppendText("Chosen test method")
            self.classifier_output.AppendText("\n")
            for rb in self.rad_btns:
                if rb.GetValue():
                    self.classifier_output.AppendText(rb.GetLabel())
            self.classifier_output.AppendText("\n")
            self.classifier_output.AppendText("\n")
            self.classifier_output.AppendText("Chosen target:")
            self.classifier_output.AppendText("\n")
            self.classifier_output.AppendText(self.target_choice.GetValue())
            self.classifier_output.AppendText("\n")
            self.classifier_output.AppendText("\n")

        if self.target_choice.GetValue() == "None":
            dlg = wx.MessageDialog(self, 'Target not selected', "Evaluate Target", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

        elif self.classifier_ch.GetSelection() == 1:
            self.classifier_output.AppendText("Starting algorithm ...\n")

            busy = wx.BusyCursor()

            features_list = self.attr_check_list.get_selected()
            target = self.target_choice.GetValue()
            output = self.workset_controller.random_forest(features_list, target,
                                                           self.percentage_split_box.GetValue())

            del busy

            self.classifier_output.AppendText(str(output))
            self.classifier_output.AppendText("\n")

        elif self.classifier_ch.GetSelection() == 0:
            self.classifier_output.AppendText("Starting algorithm ...\n")
            features_list = self.attr_check_list.get_selected()
            target = self.target_choice.GetValue()
            output = self.workset_controller.mlogit(features_list, target,
                                                    self.percentage_split_box.GetValue())
            self.classifier_output.AppendText(str(output))
            self.classifier_output.AppendText("\n")
