import wx


class MenuBar(wx.MenuBar):
    def __init__(self):
        super().__init__()
        self.mn_itms_to_enable = list()

        file_menu = wx.Menu()

        open_file_menu_item = wx.MenuItem(file_menu, wx.ID_OPEN, text="Open")
        file_menu.Append(open_file_menu_item)

        save_as_menu_item = wx.MenuItem(file_menu, wx.ID_SAVEAS, text="Save as")
        save_as_menu_item.Enable(False)
        self.mn_itms_to_enable.append(save_as_menu_item)
        file_menu.Append(save_as_menu_item)

        self.Append(file_menu, "File")

    def enable_menu_items(self, enable=True):
        for mn_itm in self.mn_itms_to_enable:
            mn_itm.Enable(enable)
