# question: Is this a question? answers: yes/no
# variables yes,no = false; if answer is yes, set yes to true
# output depend on if yes/no is true

import wx
import openQuestions
import multipleChoice
from rangeQuestions import testFrame


class Program(wx.Frame):
    panels = []
    question_number = 0

    def __init__(self):
        super().__init__(None, title='Goodbye World :] :>')
        # p1 = multipleChoice.MultipleChoicePanel(self, "Question 1")

        sizer = wx.BoxSizer()
        self.SetSizer(sizer)

        self.panel_one = multipleChoice.MultipleChoicePanel(self, "Question 1")
        sizer.Add(self.panel_one, 1, wx.EXPAND)
        self.panel_one.btn.Bind(wx.EVT_BUTTON, self.show_panel_two)
        self.panel_two = multipleChoice.MultipleChoicePanel(self, "Question 2")
        sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.panel_two.btn.Bind(wx.EVT_BUTTON, self.show_panel_one)
        self.panel_two.Hide()
        self.SetSize((1000, 800))
        self.Centre()

    def show_panel_one(self, event):
        self.panel_one.Show()
        self.panel_two.Hide()
        self.Layout()

    def show_panel_two(self, event):
        self.panel_two.Show()
        self.panel_one.Hide()
        self.Layout()

        # self.panels.append(openQuestions.OpenQPanel(self, "Introduction!"))
        # self.panels[self.question_number].Show()
        #
        # qs = ["Question 1: What is reason that you decided to go to the counsellor?", "Question 2"]
        # for i in range(len(qs)):
        #     q = qs[i]
        #     self.panels.append(openQuestions.OpenQPanel(self, q))
        #     self.panels[i + 1].Hide()
        #
        # self.SetSize((800, 600))
        # self.Centre()


if __name__ == '__main__':
    questions = {}
    app = wx.App(redirect=False)
    # frame = testFrame()
    frame = Program()
    frame.Show()
    app.MainLoop()
