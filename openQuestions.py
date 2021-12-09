import wx
from datetime import datetime


class OpenQPanel(wx.Panel):
    def __init__(self, parent, question):
        super().__init__(parent)
        self.xframe = parent

        self.SetSize((1000, 800))

        q1 = wx.StaticText(self, label=question)
        self.text1 = wx.TextCtrl(self, -1, size=(175, 50))

        self.submit_button = wx.Button(self, label='Submit answer')
        self.submit_button.Bind(wx.EVT_BUTTON, self.submit)

        self.next = wx.Button(self, -1, "Next panel", (345, 50))
        self.prev = wx.Button(self, -1, "Prev panel", (545, 50))

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)

        main_sizer.Add(q1, proportion=1,
                       flag=wx.ALL | wx.BOTTOM,
                       border=10)
        main_sizer.Add(self.text1, proportion=1,
                       flag=wx.EXPAND,
                       border=10)
        main_sizer.Add(self.submit_button, proportion=1,
                       flag=wx.EXPAND | wx.ALL,
                       border=5)

    def submit(self, event):
        answer = self.text1.GetValue()
        with open('answers.txt', 'a') as f:
            now = datetime.now()
            f.write(now.strftime("%d-%m-%Y %H:%M:%S") + ': ')
            f.write(answer)
            f.write('\n')
