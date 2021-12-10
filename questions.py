from enum import Enum
from question_panels import OpenQPanel, MultipleChoicePanel, RangeQPanel


# this file only has the representation for questions and such. panels are done in question_panels.py
# there's probably a better way of doing it than the way it is now but this is what's here now

class QType(Enum):
    OPEN = 0
    CHOICE = 1
    RANGE = 2


def get_questions():
    """
    Returns list of information required to initialize a question, such as the question text, question type,
    and answers. We will need a more complex system of question selection than just going through a list,
    but this is merely a fraction of the power of our eternally scalable system.

    The amount of spaghetti is only limited by the size of the pot, and brother,
    |                                                                 |
    |                                                                 |
    |                                                                 |
    |                                                                 |
    |                                                                 |
    |                                                                 |
    |                                                                 |
    |                                                                 |
    |_________________________________________________________________|
    That's a big pot.

    :returns List of questions
    """

    questions = [
        ['What is the reason you decided to go to the counselor?', QType.OPEN],
        ['How often do you sleep less than usual?', QType.CHOICE, ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']],
        ['Rate your social life from 1 to 5, with 1 being the worst and 5 being excellent.', QType.RANGE, [1, 5]],
        ['Do you suffer from headaches?', QType.CHOICE]
    ]

    return questions


def initialize_questions(parent):
    """
    Initializes all questions panels as a list
    :param parent: Parent frame
    :returns list of question panels
    """
    qpanels = []
    for q in get_questions():
        qtype = q[1]
        qtext = q[0]
        if qtype == QType.OPEN:
            qpanel = OpenQPanel(parent, qtext)
        elif qtype == QType.CHOICE:
            # initialize as multiple choice
            try:
                qans = q[2]
                qpanel = MultipleChoicePanel(parent, qtext, qans)
            except IndexError:
                qpanel = MultipleChoicePanel(parent, qtext)
        elif qtype == QType.RANGE:
            # initialize frame as scale question
            try:
                qrange = q[2]
                qpanel = RangeQPanel(parent, qtext, qrange)
            except IndexError:
                qpanel = RangeQPanel(parent, qtext)
        else:
            print(f"Invalid question type for question {q[0]}")
            print(f"Question type {q[1]} not recognized!")
            continue
        qpanels.append(qpanel)
    return qpanels
