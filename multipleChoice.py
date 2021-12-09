import wx
from datetime import datetime


class MultipleChoicePanel(wx.Panel):
    frame = False

    def __init__(self, parent, question):
        super().__init__(parent)
        self.xframe = parent

        self.SetSize((1000, 800))

        button1 = wx.Button(self, label='Never')
        button1.Bind(wx.EVT_BUTTON, self.never_button)

        button2 = wx.Button(self, label='Rarely')
        button2.Bind(wx.EVT_BUTTON, self.rarely_button)

        button3 = wx.Button(self, label='Sometimes')
        button3.Bind(wx.EVT_BUTTON, self.sometimes_button)

        button4 = wx.Button(self, label='Often')
        button4.Bind(wx.EVT_BUTTON, self.often_button)

        button5 = wx.Button(self, label='Always')
        button5.Bind(wx.EVT_BUTTON, self.always_button)

        self.next = wx.Button(self, -1, "Next panel", (345, 50))
        self.prev = wx.Button(self, -1, "Prev panel", (545, 50))

        q1 = wx.StaticText(self, label=question)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(q1, proportion=1,
                       flag=wx.ALL | wx.BOTTOM,
                       border=5)
        main_sizer.Add(button1, proportion=1,
                       flag=wx.EXPAND | wx.ALL,
                       border=5)
        main_sizer.Add(button2, proportion=1,
                       flag=wx.EXPAND | wx.ALL,
                       border=5)
        main_sizer.Add(button3, proportion=1,
                       flag=wx.EXPAND | wx.ALL,
                       border=5)
        main_sizer.Add(button4, proportion=1,
                       flag=wx.EXPAND | wx.ALL,
                       border=5)
        main_sizer.Add(button5, proportion=1,
                       flag=wx.EXPAND | wx.ALL,
                       border=5)

        self.SetSizer(main_sizer)

    def never_button(self, event):
        answer = "Never"
        with open('answers.txt', 'a') as f:
            now = datetime.now()
            f.write(now.strftime("%d-%m-%Y %H:%M:%S") + ': ')
            f.write(answer)
            f.write('\n')

    def rarely_button(self, event):
        answer = "Rarely"
        with open('answers.txt', 'a') as f:
            now = datetime.now()
            f.write(now.strftime("%d-%m-%Y %H:%M:%S") + ': ')
            f.write(answer)
            f.write('\n')

    def sometimes_button(self, event):
        answer = "Sometimes"
        with open('answers.txt', 'a') as f:
            now = datetime.now()
            f.write(now.strftime("%d-%m-%Y %H:%M:%S") + ': ')
            f.write(answer)
            f.write('\n')

    def often_button(self, event):
        answer = "Often"
        with open('answers.txt', 'a') as f:
            now = datetime.now()
            f.write(now.strftime("%d-%m-%Y %H:%M:%S") + ': ')
            f.write(answer)
            f.write('\n')

    def always_button(self, event):
        answer = "Always"
        with open('answers.txt', 'a') as f:
            now = datetime.now()
            f.write(now.strftime("%d-%m-%Y %H:%M:%S") + ': ')
            f.write(answer)
            f.write('\n')
