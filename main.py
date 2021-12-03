# question: Is this a question? answers: yes/no
# variables yes,no = false; if answer is yes, set yes to true
# output depend on if yes/no is true

import wx
from datetime import datetime

class MyPanel(wx.Panel):
    frame = False

    def __init__(self, parent):
        super().__init__(parent)
        frame = parent

        button1 = wx.Button(self, label='Submit answer')
        button1.Bind(wx.EVT_BUTTON, self.on_button1)

        button2 = wx.Button(self, label='Quit application')
        button2.Bind(wx.EVT_BUTTON, self.on_button2)

        q1 = wx.StaticText(self, label="What is reason that you decided to go to the counsellor?")

        self.text1 = wx.TextCtrl(self, -1, size=(175, 50))

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(q1, proportion=1,
                       flag=wx.ALL | wx.BOTTOM,
                       border=5)
        main_sizer.Add(self.text1, proportion=1,
                       flag=wx.EXPAND,
                       border=5)
        main_sizer.Add(button1, proportion=1,
                       flag=wx.EXPAND | wx.ALL,
                       border=5)
        main_sizer.Add(button2, proportion=1,
                       flag=wx.EXPAND | wx.ALL,
                       border=5)

        self.SetSizer(main_sizer)

    def on_button1(self, event):
        answer = self.text1.GetValue()
        with open('answers.txt', 'a') as f:
            now = datetime.now()
            f.write(now.strftime("%d-%m-%Y %H:%M:%S") + ': ')
            f.write(answer)
            f.write('\n')
        frame.Close()

    def on_button2(self, event):
        frame.Close()


class MyFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, title='Hello World')
        panel = MyPanel(self)
        self.Show()


if __name__ == '__main__':
    app = wx.App(redirect=False)
    frame = MyFrame()
    app.MainLoop()