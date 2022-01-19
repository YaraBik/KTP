import wx

prev_loc = (345, 50)
next_loc = (545, 50)

null_score = [0, 0, 0]  # healthy, stress, burnout


class ChoiceButton(wx.Button):
    """
    Button used by ChoiceQPanel. Displays a possible option and updates question answer if selected.
    """

    def __init__(self, parent, label):
        """
        Initializes choice button.
        :param parent: Parent panel
        :param label: Button label
        """
        super().__init__(parent, label=label)
        self.parent = parent
        self.label = label
        self.Bind(wx.EVT_BUTTON, self.update_answer)

    def update_answer(self, event):
        """
        Updates parent question answer to button label when choice is selected.
        """
        self.parent.answer = self.label
        self.parent.update_buttons()


class QPanel(wx.Panel):
    """
    General question panel.
    """

    def __init__(self, parent, question):
        """
        Initializes general question panel. Please use this class's children instead.
        :param parent: Parent panel
        :param question: Question.
        """
        self.question = question
        self.answer = None  # stores question answer
        self.save_answer = True  # whether or not to save the answer (True by default)
        self.prerequisites = None  # set later
        self.symptom = None  # set later
        # prep ui stuff
        super().__init__(parent)
        self.xframe = parent
        self.SetSize((1000, 800))

        # two button slots that are used to progress/go back in the survey (can be edited by Program class)
        self.prev = wx.Button(self, -1, "Prev question", prev_loc)
        self.next = wx.Button(self, -1, "Next question", next_loc)

        qtext = wx.StaticText(self, label=question)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(qtext, proportion=1,
                            flag=wx.ALL | wx.BOTTOM,
                            border=5)
        self.SetSizer(self.main_sizer)

    def get_symptoms(self):
        """
        Returns the symptom or None based on the stored answer
        :returns symptom or None
        """
        return self.symptom

    def set_symptoms(self, symptom):
        """
        Sets symptoms to whatever's provided
        :param symptom: Provided symptom
        """
        self.symptom = symptom

    def set_prerequisites(self, psets):
        """
        Sets prerequisites to whatever's provided
        :param psets: Prerequisite sets (list of AND symptoms, only one list needs to be fulfilled for truth)
        """
        self.prerequisites = psets

    def clear_inputs(self):
        """
        Clears question input and answers and sets the answer to None.
        """
        self.answer = None

    def check_prerequisites(self, flags):
        """
        Check if the question's prerequisites to be asked are satisfied.
        :param flags: set of current flags/symptoms
        :returns True if prerequisites satisfied, otherwise False.
        """
        if self.prerequisites is None:
            return True

        for pset in self.prerequisites:  # every set of AND must be checked, if one goes through conditions are filled
            for i, pr in enumerate(pset):

                if pr[0] == '!' and pr[1:] in flags:  # check failure conditions for the set
                    continue
                elif pr[0] != '!' and pr not in flags:
                    continue

                if i + 1 == len(pset):  # all flags/symptoms satisfied, return True
                    return True
        return False

    def get_scores(self):
        """
        Retrieves the scores/state values or whatever you call them of the current answer.
        :returns list of 3 values
        """
        return null_score


class OpenQPanel(QPanel):
    """
    Open question. Not used for inference, but for general information (relevant in the real-life context).
    """

    def __init__(self, parent, question):
        """
        Initializes open question.
        :param parent: Parent frame
        :param question: Question
        """
        super().__init__(parent, question)

        # make text field
        self.text = wx.TextCtrl(self, -1, size=(175, 50))
        self.text.Bind(wx.EVT_TEXT, self.update_answer)

        # add all
        self.main_sizer.Add(self.text, proportion=1,
                            flag=wx.EXPAND,
                            border=10)

    def update_answer(self, event):
        """
        Update answer based on text box content.
        :return:
        """
        self.answer = self.text.GetValue()

    def clear_inputs(self):
        super().clear_inputs()
        self.text.Clear()


class ChoiceQPanel(QPanel):
    """
    Question where the answer is a single value selected from a list.
    """

    def __init__(self, parent, question, answers=(('Yes', [0, 0, 2]), ('No', [2, 0, 0]))):
        """
        Initializes multiple choice question.
        :param parent: Parent frame
        :param question: Question
        :param answers: List of answers and their associated scores. If not provided, 'Yes' and 'No' are used.
        """
        super().__init__(parent, question)

        # create score dictionary
        self.scores = {}
        for ans, score in answers:
            self.scores[ans] = score

        # initialize and add all buttons
        self.buttons = []
        for ans, _ in answers:
            bt = ChoiceButton(self, label=ans)
            self.main_sizer.Add(bt, proportion=1,
                                flag=wx.EXPAND | wx.ALL,
                                border=5)
            self.buttons.append(bt)

    def clear_inputs(self):
        super().clear_inputs()
        for bt in self.buttons:
            bt.ClearBackground()

    def update_buttons(self):
        """
        Iterate through all buttons and update button borders based on selected answer.
        """
        for bt in self.buttons:
            if bt.label == self.answer:
                bt.SetWindowStyleFlag(wx.SIMPLE_BORDER)
            else:
                bt.SetWindowStyleFlag(wx.NO_BORDER)

    def get_scores(self):
        if self.answer is not None:
            return self.scores[self.answer]
        else:
            return null_score

    def get_symptoms(self):
        """
        Returns the symptom or None based on the stored answer
        :returns symptom or None
        """
        if self.answer in ['Sometimes', 'Often', 'Always']:
            return self.symptom
        else:
            return '!' + self.symptom


class RangeQPanel(QPanel):
    """
    Question where the answer is provided using a slider.
    """

    def __init__(self, parent, question, val=(1, 5), max_scores=(0, 0, 2)):
        """
        Initializes range question (e.g. pick a value from 1 to 5).
        :param parent: Parent frame
        :param question: Question
        :param max_scores: State values for the question (maximum scores for each category)
        :param val: Tuple containing slider minimum and maximum value
        """
        super().__init__(parent, question)

        self.symptom_threshold = 8  # anything below this value counts as a symptom
        self.max_scores = max_scores

        # if min value is more than max, swap
        if val[0] > val[1]:
            val[0], val[1] = val[1], val[0]

        # make slider and bind it
        self.slider = wx.Slider(self, -1, minValue=val[0], maxValue=val[1],
                                style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.slider.SetTickFreq(1)
        self.slider.Bind(wx.EVT_SLIDER, self.update_answer)
        # add slider
        self.main_sizer.Add(self.slider, proportion=1,
                            flag=wx.EXPAND,
                            border=10)

    def set_threshold(self, th):
        """
        Sets symptom threshold
        :param th: Integer
        """
        self.symptom_threshold = th

    def update_answer(self, event):
        """
        Updates question answer.
        """
        self.answer = self.slider.GetValue()

    def clear_inputs(self):
        super().clear_inputs()
        avg = int((self.slider.GetMin() + self.slider.GetMax()) / 2)
        self.slider.SetValue(avg)

    def get_scores(self):
        if self.answer is not None:
            return [self.answer * val / self.slider.GetMax() for val in self.max_scores]
        else:
            return null_score

    def get_symptoms(self):
        """
        Returns the symptom or None based on the stored answer
        :returns symptom or None
        """
        if self.answer is None:
            return None

        if self.answer < self.symptom_threshold:  # if they rate something less than that, there's a problem.
            return self.symptom
        else:
            return '!' + self.symptom


class InfoPanel(QPanel):
    """
    Panel with informative text.
    """

    def __init__(self, parent, text):
        """
        Initializes information panel.
        :param parent: Parent frame
        :param text: Info text
        """
        super().__init__(parent, text)
        self.save_answer = False
