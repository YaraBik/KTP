import wx
import openQuestions
import multipleChoice
import rangeQuestions


class Program(wx.Frame):
    panels = []
    question_number = 0

    def __init__(self):
        super().__init__(None, title='Goodbye World :] :>')
        qs = [["Question 1: What is reason that you decided to go to the counsellor?", "open"], ["Question 2", "multi"], ["Question 3", "range"]]

        sizer = wx.BoxSizer()
        self.SetSizer(sizer)

        # TODO: Make special class for introduction/explanation between questions?
        self.panel_one = openQuestions.OpenQPanel(self, "Introduction")
        sizer.Add(self.panel_one, 1, wx.EXPAND)
        self.panel_one.next.Bind(wx.EVT_BUTTON, self.show_next_panel)
        self.panel_one.prev.Hide()
        self.panel_one.text1.Hide()
        self.panel_one.submit_button.Hide()
        self.panels.append(self.panel_one)

        for i in range(len(qs)):
            q = qs[i][0]

            # Make correct panel based on question type
            if qs[i][1] == "open":
                self.panel_two = openQuestions.OpenQPanel(self, q)
            elif qs[i][1] == "multi":
                self.panel_two = multipleChoice.MultipleChoicePanel(self, q)
            elif qs[i][1] == "range":
                self.panel_two = rangeQuestions.RangeQPanel(self, q)

            sizer.Add(self.panel_two, 1, wx.EXPAND)
            self.panel_two.prev.Bind(wx.EVT_BUTTON, self.show_prev_panel)

            # Only add next button when there is a panel after this
            if i < len(qs)-1:
                self.panel_two.next.Bind(wx.EVT_BUTTON, self.show_next_panel)
            else:
                self.panel_two.next.Hide()

            self.panel_two.Hide()
            self.panels.append(self.panel_two)

        self.SetSize((1000, 800))
        self.Centre()

    def show_next_panel(self, event):
        self.panels[self.question_number+1].Show()
        self.panels[self.question_number].Hide()
        self.question_number += 1
        self.Layout()

    def show_prev_panel(self, event):
        self.panels[self.question_number-1].Show()
        self.panels[self.question_number].Hide()
        self.question_number -= 1
        self.Layout()


if __name__ == '__main__':
    questions = {}
    app = wx.App(redirect=False)
    frame = Program()
    frame.Show()
    app.MainLoop()
