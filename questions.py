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

    qpanels.append(InfoPanel(parent, 'Thank you for completing these questions. Please press \'Submit answers\' to '
                                     'submit.'))

    return qpanels


def add_questions(parent, qpanels, filename):
    """
    Adds questions in a certain file to the master list of panels.
    :param parent: parent frame
    :param qpanels: List of panels
    :param filename: Name of the file in question
    """
    # generic answers
    freq_answers = [('Never',     [2, 0, 0]),
                    ('Rarely',    [1, 1, 0]),
                    ('Sometimes', [0, 2, 0]),
                    ('Often',     [0, 1, 1]),
                    ('Always',    [0, 0, 2])]  # generic frequency-related answers

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            qtext, qtype = line.split(";")
            qtype = qtype.replace("\n", "")
            # different question configurations
            if qtype == "info":  # info panel
                qpanels.append(InfoPanel(parent, qtext))
            elif qtype == "open":  # open question
                qpanels.append(OpenQPanel(parent, qtext))
            elif qtype == "range":  # standard 0 - 10 range question
                qpanels.append(RangeQPanel(parent, qtext, val=(0, 10)))
            elif qtype == "5choice":  # standard frequency-based multiple choice
                qpanels.append(ChoiceQPanel(parent, qtext, freq_answers))
            elif qtype == "2choice":  # yes-no question
                qpanels.append(ChoiceQPanel(parent, qtext))
            else:
                print("Skipped question:", line)
