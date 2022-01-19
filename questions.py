from question_panels import OpenQPanel, ChoiceQPanel, RangeQPanel, InfoPanel
import os


def init_panel(parent, question_line, type_line):
    """
    Initializes question from info in file lines.
    :param parent: Parent frame.
    :param question_line: Question line.
    :param type_line: Type line.
    :returns Initialized panel
    """
    # generic answers
    freq_answers = [('Never', [10, 0, 0]),
                    ('Rarely', [5, 5, 0]),
                    ('Sometimes', [0, 10, 0]),
                    ('Often', [0, 5, 5]),
                    ('Always', [0, 0, 10])]  # generic frequency-related answers

    qtext = question_line[4:]
    qtype = type_line[4:]
    # print(f"QUESTION: {qtext}")
    qtext = qtext.removeprefix(' ')
    qtype = qtype.removeprefix(' ')
    qtext = qtext.removesuffix('\n')
    qtype = qtype.removesuffix('\n')

    if qtype == "FREQ":
        return ChoiceQPanel(parent, qtext, freq_answers)
    elif qtype == "OPEN":
        return OpenQPanel(parent, qtext)
    elif qtype == "INFO":
        return InfoPanel(parent, qtext)
    elif qtype == "RATE":
        qp = RangeQPanel(parent, qtext, val=(0, 10), max_scores=(0, 0, 0))
        qp.set_threshold(5)
        return qp
    elif qtype == "RATE7":
        qp = RangeQPanel(parent, qtext, val=(0, 10), max_scores=(0, 0, 0))
        qp.set_threshold(7)
        return qp
    elif qtype == "RATE8":
        qp = RangeQPanel(parent, qtext, val=(0, 10), max_scores=(0, 0, 0))
        qp.set_threshold(8)
        return qp
    elif qtype == "RATE9":
        qp = RangeQPanel(parent, qtext, val=(0, 10), max_scores=(0, 0, 0))
        qp.set_threshold(9)
        return qp
    else:
        print(f"{qtype} is not a question type!")


def set_panel_prereq(qp, prereq_line):
    """
    Adds prerequisite symptoms to the question.
    :param qp: Question panel
    :param prereq_line: Prerequisite line
    :return: 
    """
    prerequisites = prereq_line[4:]
    prerequisites = prerequisites.removeprefix(' ')
    prerequisites = prerequisites.split(', ')
    for i, s in enumerate(prerequisites):
        pset = s.split(' or ')
        for j, p in enumerate(pset):
            p = p.removeprefix(' ')
            p = p.removesuffix(' ')
            p = p.removesuffix('\n')
            pset[j] = p
        prerequisites[i] = pset
    if prerequisites == [['']]:
        prerequisites = None
    # print(f"PREREQUISITES: {prerequisites}")
    qp.set_prerequisites(prerequisites)


def set_panel_symptoms(qp, symptoms_line):
    """
    Adds (consequent) symptoms to the question.
    :param qp: Question panel
    :param symptoms_line: Symptom line
    """

    symptom = symptoms_line[4:]
    symptom = symptom.removeprefix(' ')
    symptom = symptom.removesuffix('\n')
    #print(f"SYMPTOM: {symptom}")
    qp.set_symptoms(symptom)


def add_questions(parent, qpanels, filename):
    """
    Adds questions in a certain file to the master list of panels.
    :param parent: parent frame
    :param qpanels: List of panels
    :param filename: Name of the file in question
    """

    with open(filename) as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            if lines[i][0:4].upper() == "QUE:" and lines[i + 1][0:4].upper() == "TYP:" and lines[i + 2][
                                                                                           0:4].upper() == "PRE:" and \
                    lines[i + 3][0:4].upper() == "SYM:":
                qp = init_panel(parent, lines[i], lines[i + 1])
                set_panel_prereq(qp, lines[i + 2])
                set_panel_symptoms(qp, lines[i + 3])

                qpanels.append(qp)
                i += 5 # jump forward 5 lines
            else:
                print(
                    f'Incorrect input in lines {i}-{i + 4}. Correct format is "QUE,TYP,PRE,SYM, followed by a blank line"')


def initialize_questions(parent):
    """
    Initializes a set of question panels as a list
    :param parent: Parent frame
    :returns list of question panels
    """

    # generic prerequisites
    sus_range = [0, 1, 2, 3]  # 1-5 scale "low" numbers

    # add questions
    qpanels = []
    add_questions(parent, qpanels, os.getcwd() + '/questions/questions.txt')

    qpanels.append(InfoPanel(parent, 'Thank you for completing these questions. Please press \'Submit answers\' to '
                                     'submit.'))
    return qpanels
