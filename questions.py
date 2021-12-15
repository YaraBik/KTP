from question_panels import OpenQPanel, ChoiceQPanel, RangeQPanel, InfoPanel


# this file only has the representation for questions and such. panels are done in question_panels.py
# there's probably a better way of doing it than the way it is now but this is what's here now


def initialize_questions(parent):
    """
    Initializes a set of question panels as a list
    :param parent: Parent frame
    :returns list of question panels
    """

    # generic answers
    freq_answers = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always'] # generic frequency-related answers

    # generic conditions
    sus_range = [0, 1, 2, 3] # 1-5 scale "low" numbers

    # add questions
    qpanels = []
    qpanels.append(InfoPanel(parent, 'This is an informative text'))
    qpanels.append(OpenQPanel(parent, 'What is the reason you decided to go to the counselor?'))
    qpanels.append(ChoiceQPanel(parent, 'How often do you sleep less than usual?', freq_answers))
    social_life = RangeQPanel(parent,
                              'Rate your social life from 1 to 5, with 1 being the worst and 5 being excellent.')
    qpanels.append(social_life)
    qpanels.append(InfoPanel(parent, 'Lmao', conditions=[(social_life, sus_range)]))
    qpanels.append(ChoiceQPanel(parent, 'Do you suffer from headaches?'))

    return qpanels
