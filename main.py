# question: Is this a question? answers: yes/no
# variables yes,no = false; if answer is yes, set yes to true
# output depend on if yes/no is true

import wx
import openQuestions


class Program(wx.Frame):
    panels = []
    question_number = 0

    def __init__(self):
        # wx.Frame.__init__(self, None, wx.ID_ANY, 'Program')

        # panel_one = Glowne(self)
        # self.panel_two = Glowne1(self)
        # self.panel_two.Hide()
        # self.SetSize((800, 600))
        # self.Centre()

        super().__init__(None, title='Goodbye World :] :>')
        self.panels.append(openQuestions.OpenQPanel(self, "Introduction!"))
        self.panels[self.question_number].Show()

        qs = ["Question 1: What is reason that you decided to go to the counsellor?", "Question 2"]
        for i in range(len(qs)):
            q = qs[i]
            self.panels.append(openQuestions.OpenQPanel(self, q))
            self.panels[i + 1].Hide()

        self.SetSize((800, 600))
        self.Centre()


if __name__ == '__main__':
    questions = {}
    app = wx.App(redirect=False)
    frame = Program()
    frame.Show()
    app.MainLoop()
