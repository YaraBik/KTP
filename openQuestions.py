import wx
from datetime import datetime
from main import Program


class OpenQPanel(wx.Panel):
    def __init__(self, parent, question):
        super().__init__(parent)
        self.xframe = parent

        self.SetSize((800, 600))

        # q1 = wx.StaticText(self, label=question)
        # self.text1 = wx.TextCtrl(self, -1, size=(175, 50))
        #
        # button1 = wx.Button(self, label='Submit answer')
        # button1.Bind(wx.EVT_BUTTON, self.on_button1)
        #
        # button2 = wx.Button(self, label='Quit application')
        # button2.Bind(wx.EVT_BUTTON, self.on_button2)

        next = wx.Button(self, label='>')
        next.Bind(wx.EVT_BUTTON, self.nextPanel)

        prev = wx.Button(self, label='<')
        prev.Bind(wx.EVT_BUTTON, self.previousPanel)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        # main_sizer.Add(q1, proportion=1,
        #                flag=wx.ALL | wx.BOTTOM,
        #                border=10)
        # main_sizer.Add(self.text1, proportion=1,
        #                flag=wx.EXPAND,
        #                border=10)
        # main_sizer.Add(button1, proportion=1,
        #                flag=wx.EXPAND | wx.ALL,
        #                border=5)
        # main_sizer.Add(button2, proportion=1,
        #                flag=wx.EXPAND | wx.ALL,
        #                border=5)
        main_sizer.Add(next, proportion=1,
                       flag=wx.EXPAND | wx.ALL,
                       border=5)
        main_sizer.Add(prev, proportion=1,
                       flag=wx.EXPAND | wx.ALL,
                       border=5)
        self.SetSizer(main_sizer)

    def nextPanel(self, event):
        parent = self.xframe
        parent.panels[parent.question_number].Hide()
        parent.question_number += 1
        parent.panels[parent.question_number].Show()
        print("Next question!")

    def previousPanel(self, event):
        parent = self.xframe
        parent.panels[parent.question_number].Hide()
        parent.question_number -= 1
        parent.panels[parent.question_number].Show()

    def on_button1(self, event):
        answer = self.text1.GetValue()
        with open('answers.txt', 'a') as f:
            now = datetime.now()
            f.write(now.strftime("%d-%m-%Y %H:%M:%S") + ': ')
            f.write(answer)
            f.write('\n')

    def on_button2(self, event):
        self.xframe.Close()
