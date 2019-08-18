import wx
import seaborn as sns
sns.set()
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar


class PlotFrame(wx.Frame):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        super().__init__(parent, ID, title, pos, size, style)

        self.figure = Figure(facecolor="white", figsize=(1, 1))
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)

        self.SetSizer(sizer)

    def plot_boxplot(self, df, col):
        sns.boxplot(data=df[col], ax=self.axes)
        self.canvas.draw()

    def plot_boxplot_with(self, df, col1, col2):
        sns.boxplot(x=col1, y=col2, data=df, ax=self.axes)
        self.canvas.draw()

    def plot_barplot(self, df, col):
        sns.countplot(x=col, data=df, ax=self.axes)
        self.canvas.draw()

    def plot_barplot_with(self, df, col1, col2):
        sns.countplot(x=col2, hue=col1, data=df, ax=self.axes)
        self.canvas.draw()

    def plot_hist(self, df, col):
        sns.distplot(df[col], ax=self.axes)
        self.canvas.draw()

    def plot_violin(self, df, col):
        df.plot.bar(x=col, ax=self.axes)
        sns.violinplot(data=df[col], ax=self.axes)
        self.canvas.draw()

    def plot_corr_mat(self, df):
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        new_df = df.select_dtypes(include=numerics)
        corr_matrix = new_df.corr()
        sns.heatmap(corr_matrix, ax=self.axes, xticklabels=True, yticklabels=True)
