import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import seaborn as sns
sns.set()


METRICS = {
    1: "Confusion Matrix"
    # 2: "F1 Score"
}


class ResultsPage(wx.Panel):
    def __init__(self, parent, workset_controller):
        super().__init__(parent, id=wx.ID_ANY)
        workset_controller.set_results_view(self)
        self.workset_controller = workset_controller
        self.metric_ch = None
        self.figure = None
        self.axes = None
        self.canvas = None
        self.toolbar = None

        metric_box = self.create_metric_box()
        figure_box = self.create_figure_box()

        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(metric_box, 0, wx.EXPAND | wx.ALL, 5)
        border.Add(figure_box, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(border)

    def create_metric_box(self):
        box = wx.StaticBox(self, -1, "Display")
        top_border, other_border = box.GetBordersForSizer()
        bsizer = wx.BoxSizer(wx.VERTICAL)
        bsizer.AddSpacer(top_border)

        choices = list(METRICS.values())
        self.metric_ch = wx.Choice(box, -1, choices=choices)
        self.metric_ch.SetSelection(0)

        bsizer.Add(self.metric_ch, 1, wx.EXPAND | wx.ALL, 5)
        box.SetSizer(bsizer)
        return box

    def create_figure_box(self):
        box = wx.StaticBox(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.figure = Figure(facecolor="white", figsize=(1, 1))
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(box, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)

        sizer.Add(self.canvas, 1, wx.EXPAND)
        sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)

        box.SetSizer(sizer)
        return box

    def draw_confusion_mat(self, cm):
        self.axes.clear()
        sns.heatmap(cm, ax=self.axes, xticklabels=True, yticklabels=True, annot=True, cbar=False)
        self.canvas.draw()
