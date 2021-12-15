from question_panels import OpenQPanel, ChoiceQPanel, RangeQPanel, InfoPanel, QType


# this file only has the representation for questions and such. panels are done in question_panels.py
# there's probably a better way of doing it than the way it is now but this is what's here now


def get_questions():
    """
    Returns 2d list containing information required to initialize all questions required for the system.

    :returns List of questions
    """

    # master list of questions
    questions = [
        ['This is an informative text', QType.INFO],
        ['What is the reason you decided to go to the counselor?', QType.OPEN],
        ['How often do you sleep less than usual?', QType.CHOICE, ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']],
        ['Rate your social life from 1 to 5, with 1 being the worst and 5 being excellent.', QType.RANGE, [1, 5],
         'soclife'],
        ['Lmao', QType.INFO, None, None, ('soclife', 5)],
        ['Do you suffer from headaches?', QType.CHOICE]
    ]

    return questions


def initialize_questions(parent):
    """
    Initializes a set of question panels as a list
    :param parent: Parent frame
    :returns list of question panels
    """

    freq_answers = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']
    sus_range = [0, 1, 2, 3]
    qpanels = []
    qpanels.append(InfoPanel(parent, 'This is an informative text'))
    qpanels.append(OpenQPanel(parent, 'What is the reason you decided to go to the counselor?'))
    qpanels.append(ChoiceQPanel(parent, 'How often do you sleep less than usual?', freq_answers))
    social_life = RangeQPanel(parent,
                              'Rate your social life from 1 to 5, with 1 being the worst and 5 being excellent.')
    qpanels.append(social_life)
    qpanels.append(InfoPanel(parent, 'Lmao', conditions= [(social_life, sus_range)]))
    qpanels.append(ChoiceQPanel(parent, 'Do you suffer from headaches?'))

    return qpanels


'''def initialize_questions(parent):
    """
    Initializes a set of question panels as a list
    :param parent: Parent frame
    :returns list of question panels
    """
    qpanels = []
    for q in get_questions():
        qtext = q[0]
        qtype = q[1]
        try:
            qtag = q[3]
        except IndexError:
            pass
        try:
            qcond = q[4]
        except IndexError:
            pass

        if qtype == QType.OPEN:
            qpanel = OpenQPanel(parent, qtext)
        elif qtype == QType.CHOICE:
            # initialize as multiple choice
            try:
                qans = q[2]
                qpanel = ChoiceQPanel(parent, qtext, qans)
            except IndexError:
                qpanel = ChoiceQPanel(parent, qtext)
        elif qtype == QType.RANGE:
            # initialize frame as scale question
            try:
                qrange = q[2]
                qpanel = RangeQPanel(parent, qtext, qrange)
            except IndexError:
                qpanel = RangeQPanel(parent, qtext)
        elif qtype == QType.INFO:
            qpanel = InfoPanel(parent, qtext)
        else:
            print(f"Invalid question type for question {q[0]}")
            print(f"Question type {q[1]} not recognized!")
            continue
        qpanels.append(qpanel)
    return qpanels'''
