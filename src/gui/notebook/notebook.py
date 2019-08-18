import wx
from gui.notebook.preprocess_page import PreprocessPage
from gui.notebook.prediction_page import PredictionPage
from gui.notebook.results_page import ResultsPage


class Notebook(wx.Notebook):
    def __init__(self, parent, workset_controller):
        super().__init__(parent)
        self.preproccess_page = PreprocessPage(self, workset_controller)
        self.AddPage(self.preproccess_page, "Preprocess")

        self.prediction_page = PredictionPage(self, workset_controller)
        self.AddPage(self.prediction_page, "Prediction")

        self.model_testing_page = ResultsPage(self, workset_controller)
        self.AddPage(self.model_testing_page, "Explore Results")

        self.enable_pages(False)

    def enable_pages(self, enable=True):
        self.preproccess_page.Enable(enable)
        self.prediction_page.Enable(enable)
        self.model_testing_page.Enable(enable)
