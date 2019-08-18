import wx
import wx.aui as aui
from gui.notebook.notebook import Notebook
from gui.logger import Logger
from gui.menu_bar import MenuBar
from gui.file_dialog import FileDialog
from controller.workset_controller import WorksetController


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, wx.ID_ANY, "Final Project", wx.DefaultPosition, (850, 700), wx.DEFAULT_FRAME_STYLE)

        icon = wx.Icon(r"C:\Users\Cristian\PycharmProjects\final_project\bitmaps\horse.png")
        self.SetIcon(icon)

        self._aui_manager = aui.AuiManager()
        self._aui_manager.SetManagedWindow(self)

        self.logger = None
        self.create_log_bar()
        self.workset_controller = WorksetController(view=self, logger=self.logger)
        self.create_menu_bar()
        self.notebook = self.create_notebook()

        self._aui_manager.Update()

        self.bind_events()

    def bind_events(self):
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_MENU, self.menu_handler)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_group)

    def on_radio_group(self, e):
        rb = e.GetEventObject()
        self.workset_controller.set_df_view_method(rb.GetLabel())
        self.workset_controller.refresh_df_view()

    def create_menu_bar(self):
        menu_bar = MenuBar()
        self.SetMenuBar(menu_bar)

    def menu_handler(self, evt):
        id = evt.GetId()
        if id == wx.ID_OPEN:
            file_dialog = FileDialog(self, "Open CSV File", style=wx.FD_OPEN)
            if file_dialog.ShowModal() == wx.ID_OK:
                path = file_dialog.GetPath()
                self.workset_controller.load_csv(path)
            file_dialog.Destroy()
        elif id == wx.ID_SAVEAS:
            file_dialog = FileDialog(self, "Save File As", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if file_dialog.ShowModal() == wx.ID_OK:
                path = file_dialog.GetPath()
                self.workset_controller.to_csv(path)
            file_dialog.Destroy()

    def create_log_bar(self):
        self.logger = Logger(self)
        log_pane_info = aui.AuiPaneInfo().Caption('Log').Bottom().Floatable(False)
        self._aui_manager.AddPane(self.logger, log_pane_info)

    def create_notebook(self):
        notebook = Notebook(self, self.workset_controller)
        notebook_pane_info = aui.AuiPaneInfo().Centre().CloseButton(False).CaptionVisible(False).Floatable(False)
        self._aui_manager.AddPane(notebook, notebook_pane_info)
        return notebook

    def on_close(self, event):
        _ = event
        self._aui_manager.UnInit()
        del self._aui_manager
        self.Destroy()

    def get_workset_controller(self):
        return self.workset_controller

    def enable(self):
        self.GetMenuBar().enable_menu_items()
        self.notebook.enable_pages()
