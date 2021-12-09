import wx
from datetime import datetime


class RangeQPanel(wx.Panel):
    def __init__(self, parent, question):
        super().__init__(parent)
        self.xframe = parent

        self.SetSize((1000, 800))

        q1 = wx.StaticText(self, label=question)

        self.next = wx.Button(self, -1, "Next panel", (345, 50))
        self.prev = wx.Button(self, -1, "Prev panel", (545, 50))

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)

        main_sizer.Add(q1, proportion=1,
                       flag=wx.ALL | wx.BOTTOM,
                       border=10)
