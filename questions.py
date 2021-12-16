from question_panels import OpenQPanel, ChoiceQPanel, RangeQPanel, InfoPanel
import os


# this file only has the representation for questions and such. panels are done in question_panels.py
# there's probably a better way of doing it than the way it is now but this is what's here now


def initialize_questions(parent):
    """
    Initializes a set of question panels as a list
    :param parent: Parent frame
    :returns list of question panels
    """

    # generic conditions
    sus_range = [0, 1, 2, 3]  # 1-5 scale "low" numbers

    # add questions
    qpanels = []
    add_questions(parent, qpanels, os.getcwd() + '/questions/general.txt')
    add_questions(parent, qpanels, os.getcwd() + '/questions/areas_of_life.txt')
    add_questions(parent, qpanels, os.getcwd() + '/questions/sleep.txt')
    add_questions(parent, qpanels, os.getcwd() + '/questions/activities.txt')
    add_questions(parent, qpanels, os.getcwd() + '/questions/complaints.txt')

    return qpanels


def add_questions(parent, qpanels, filename):
    # generic answers
    freq_answers = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']  # generic frequency-related answers

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            qtext, qtype = line.split(";")
            qtype = qtype.replace("\n", "")

            if qtype == "info":
                qpanels.append(InfoPanel(parent, qtext))
            elif qtype == "open":
                qpanels.append(OpenQPanel(parent, qtext))
            elif qtype == "range":
                qpanels.append(RangeQPanel(parent, qtext))
            elif qtype == "5choice":
                qpanels.append(ChoiceQPanel(parent, qtext, freq_answers))
            elif qtype == "2choice":
                qpanels.append(ChoiceQPanel(parent, qtext))
            else:
                print("Skipped question:", line)
