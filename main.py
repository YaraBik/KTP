#!/usr/bin/env python

import os
import wx
from questions import initialize_questions


class Program(wx.Frame):
    """
    Class that takes care of the entire questionnaire and inference program.
    """

    def __init__(self):
        """
        Initializes object of Program class
        """
        super().__init__(None, title='Goodbye World :] :>')

        # initialize sizer
        sizer = wx.BoxSizer()
        self.SetSizer(sizer)

        # initialize question panels
        self.panels = initialize_questions(self)
        self.question_number = 0
        self.symptoms = []  # flags of "symptoms" that are present (used for question selection)

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

    def update_symptoms(self):
        """
        Update symptoms stored in the symptom list.
        """
        sy = self.panels[self.question_number].get_symptoms()

        if sy is None:
            return
        elif sy[0] == '!' and sy[1:] in self.symptoms:
            self.symptoms.remove(sy[1:])
        elif sy[0] != '!' and sy not in self.symptoms:
            self.symptoms.append(sy)

    def show_next_panel(self, event):
        """
        Shows next panel with satisfied prerequisites in the queue.
        """
        self.update_symptoms()
        i = 1
        while self.question_number + i < len(self.panels) and not self.panels[
            self.question_number + i].check_prerequisites(self.symptoms):
            self.panels[self.question_number + i].clear_inputs()
            i += 1

        if self.question_number + i >= len(self.panels):
            i = len(self.panels) - 1 - self.question_number

        self.panels[self.question_number + i].Show()
        self.panels[self.question_number].Hide()
        self.question_number += i
        # print('Next panel')
        self.Layout()

    def show_prev_panel(self, event):
        """
        Shows the previous panel that satisfies all its prerequisites.
        """
        self.update_symptoms()
        i = 1
        while not self.panels[self.question_number - i].check_prerequisites(self.symptoms):
            self.panels[self.question_number - i].clear_inputs()
            i += 1

        self.panels[self.question_number - i].Show()
        self.panels[self.question_number].Hide()
        self.question_number -= i
        # print('Previous panel')
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
        score = [0, 0, 0]
        for qpanel in self.panels:
            if qpanel.answer is None and qpanel.save_answer and qpanel.check_prerequisites(self.symptoms):
                print("Imagine this is a popup window: u hebt niet alle vragen beantwoord! niet goed!")
                return
            elif qpanel.answer is not None:
                qa.append(qpanel.question + ': ' + str(qpanel.answer))
                qscore = qpanel.get_scores()
                for i in range(len(score)):
                    score[i] += qscore[i]
        i = 0
        while os.path.isfile(os.getcwd() + '/reports/report' + str(i) + '.txt'):
            i += 1

        with open(os.getcwd() + '/reports/report' + str(i) + '.txt', 'a') as f:
            for item in qa:
                f.write('%s\n' % item)

            self.add_symptoms(f)

            f.write('\n Raw scores per category: \n')
            f.write("\t{}:\t{}".format("HEALTHY", score[0]))
            f.write("\t{}:\t{}".format("STRESS ", score[1]))
            f.write("\t{}:\t{}".format("BURNOUT", score[2]))

            total = sum(score)
            healthy = round(score[0] / total, 3)
            stress = round(score[1] / total, 3)
            burnout = round(score[2] / total, 3)

            f.write('\n Probabilities per category (based on scores): \n')
            f.write("\t{}:\t{}".format("HEALTHY", healthy))
            f.write("\t{}:\t{}".format("STRESS ", stress))
            f.write("\t{}:\t{}".format("BURNOUT", burnout))
            f.write("\n Based on the probabilities, the diagnosis is: ")

            highest = max(healthy, stress, burnout)
            if highest > 0.9:
                f.write("EXTREMELY LIKELY ")
            elif highest > 0.7:
                f.write("VERY LIKELY ")
            elif highest > 0.5:
                f.write("LIKELY ")
            else:
                f.write("POSSIBLE ")

            # lots of healthy and lots of burnout could mean stress
            if max(healthy, burnout) >= stress and (abs(healthy - burnout) <= 20.00):
                f.write("STRESS DUE TO HIGH SCORE FOR BOTH HEALTHY AND BURNOUT.")
            elif healthy > max(burnout, stress):
                f.write("HEALTHY")
                if burnout > healthy / 2:
                    f.write(" WITH SIGNS OF BURNOUT. THIS LEADS TO THE CONCLUSION STRESS")
                if stress > healthy / 2:
                    f.write(" WITH SIGNS OF STRESS")
                f.write(".")
            elif stress > burnout:
                f.write("STRESS")
                if burnout > stress / 2:
                    f.write(" WITH SIGNS OF BURNOUT")
                f.write(".")
            else:
                f.write("BURNOUT")
                if healthy > burnout / 2:
                    f.write(" WITH SIGNS OF BEING HEALTHY. THIS LEADS TO THE CONCLUSION STRESS")
                f.write(".")

            f.write("\n")

        self.Close()

    def add_symptoms(self, f):
        rating = ["identity", "social", "relationship", "meaningfulness", "living", "finances", "career", "relaxation", "health"]
        sleep = ["sleep_problems", "less_sleep", "difficulty_falling_asleep", "lack_energy_start_day", "worried"]
        effort = ["career", "problem_effort", "mental_exhaustion_during_effort", "mental_exhaustion_after_effort", "not_rested_effort", "physical_exhaustion_effort", "aversion_effort_activities", "ability_to_do_effort", "cynical_effort", "distracted_effort", "loss_control_emotions_effort", "annoyed_effort"]
        relaxation = ["relaxation", "problem_relaxation", "mental_exhaustion_relaxation", "physical_exhaustion_relaxation", "loss_interest_relaxation", "cynical_relaxation", "concentration_problem_relaxation", "irritated_relaxation", "strong_emotions_relaxation"]
        complaint = ["no_control", "rushed", "anxious", "chest_pain", "stomach_problems", "headache", "sore_muscles"]

        rating_symptoms = []
        sleep_symptoms = []
        effort_symptoms = []
        relaxation_symptoms = []
        complaint_symptoms = []
        for sy in self.symptoms:
            if sy in rating:
                rating_symptoms.append(sy)
            elif sy in sleep:
                sleep_symptoms.append(sy)
            elif sy in effort:
                effort_symptoms.append(sy)
            elif sy in relaxation:
                relaxation_symptoms.append(sy)
            elif sy in complaint:
                complaint_symptoms.append(sy)

        f.write('\nSYMPTOMPS PER CATEGORY\n')

        f.write('AREA OF LIFE SYMPTOMS: \n')
        for sy in rating_symptoms:
            f.write('%s, ' % sy)
        f.write('\n')

        f.write('SLEEP SYMPTOMS: \n')
        for sy in sleep_symptoms:
            f.write('%s, ' % sy)
        f.write('\n')

        f.write('EFFORT ACTIVITIES SYMPTOMS: \n')
        for sy in effort_symptoms:
            f.write('%s, ' % sy)
        f.write('\n')

        f.write('RELAXATION ACTIVITIES SYMPTOMS: \n')
        for sy in relaxation_symptoms:
            f.write('%s, ' % sy)
        f.write('\n')

        f.write('COMPLAINT SYMPTOMS: \n')
        for sy in complaint_symptoms:
            f.write('%s, ' % sy)
        f.write('\n')

    def autocomplete(self):
        """
        Autocompletes all questions.
        """
        import question_panels
        for qp in self.panels:
            i = self.question_number
            if isinstance(qp, question_panels.InfoPanel) and i == len(self.panels) - 1:
                self.submit_answers(0)
                return
            elif isinstance(qp, question_panels.OpenQPanel):
                qp.text.AppendText("haha autocomplete go brrrr")
            elif isinstance(qp, question_panels.ChoiceQPanel):
                from random import choice
                qp.answer = choice(list(qp.scores))
            elif isinstance(qp, question_panels.RangeQPanel):
                from random import randint
                qp.slider.SetValue(randint(qp.slider.GetMin(), qp.slider.GetMax()))
                qp.update_answer(0)
            self.show_next_panel(0)


if __name__ == '__main__':
    questions = {}
    app = wx.App(redirect=False)
    frame = Program()
    frame.Show()
    # frame.autocomplete()
    app.MainLoop()
