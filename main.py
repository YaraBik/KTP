import os
import wx
from questions import initialize_questions


class Program(wx.Frame):

    def __init__(self):
        super().__init__(None, title='Goodbye World :] :>')

        # initialize sizer
        sizer = wx.BoxSizer()
        self.SetSizer(sizer)

        # initialize question panels
        self.panels = initialize_questions(self)
        self.question_number = 0

        # TODO: Make special class for introduction/explanation between questions?
        # self.panel_one = openQuestions.OpenQPanel(self, "Introduction")

        i = 0
        for qpanel in self.panels:
            # add panel to frame
            sizer.Add(qpanel, 1, wx.EXPAND)

            # add previous question button
            if i > 0:
                qpanel.prev.Bind(wx.EVT_BUTTON, self.show_prev_panel)
            else:
                qpanel.prev.Hide()

            # add next question button
            if i < len(self.panels) - 1:
                qpanel.next.Bind(wx.EVT_BUTTON, self.show_next_panel)
            else:
                self.add_submit(qpanel)

            # hide panel
            qpanel.Hide()

            i += 1

        # show questions starting from the first question
        self.panels[self.question_number].Show()
        self.SetSize((1000, 800))
        self.Centre()

    def show_next_panel(self, event):
        self.panels[self.question_number + 1].Show()
        self.panels[self.question_number].Hide()
        self.question_number += 1
        print('Next panel')
        self.Layout()

    def show_prev_panel(self, event):
        self.panels[self.question_number - 1].Show()
        self.panels[self.question_number].Hide()
        self.question_number -= 1
        print('Previous panel')
        self.Layout()

    def add_submit(self, qpanel):
        """
        Creates submit button to submit answers
        :param qpanel: Final panel in the survey
        """
        qpanel.next.SetLabel("Submit answers")
        qpanel.next.Bind(wx.EVT_BUTTON, self.submit_answers)

    def submit_answers(self, event):
        """
        Currently saves all questions and answers, then closes the program. In the future it should process the
        results of the questions and produce some 100% emoji expert knowledge. Refuses to save or close if questions
        are left unanswered.
        """
        qa = []
        for qpanel in self.panels:
            if qpanel.answer is None:
                print("Imagine this is a popup window: u hebt niet alle vragen beantwoord! niet goed!")
                return
            qa.append(qpanel.question + ': ' + str(qpanel.answer))
        i = 0
        while os.path.isfile(os.getcwd() + '/reports/report' + str(i) + '.txt'):
            i += 1

        with open(os.getcwd() + '/reports/report' + str(i) + '.txt', 'a') as f:
            for item in qa:
                f.write('%s\n' % item)

        self.Close()


if __name__ == '__main__':
    questions = {}
    app = wx.App(redirect=False)
    frame = Program()
    frame.Show()
    app.MainLoop()
