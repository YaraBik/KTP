import wx

# this file contains everything related to creating questions, but panels and questions are define in questions.py
# probably gotta change that later

prev_loc = (345, 50)
next_loc = (545, 50)


class ChoiceButton(wx.Button):
    """
    Button used by MultipleChoicePanel. Displays a possible option and updates question answer if selected.
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
    def __init__(self, parent, question):
        """
        Initializes general question panel. Please use this class's children instead.
        :param parent: Parent panel
        :param question: Question.
        """
        self.question = question
        self.answer = None  # stores question answer

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


class MultipleChoicePanel(QPanel):
    """
    Question where the answer is a single value selected from a list.
    """

    def __init__(self, parent, question, answers=('Yes', 'No')):
        """
        Initializes multiple choice question.
        :param parent: Parent frame
        :param question: Question
        :param answers: List of answers. If not provided, 'Yes' and 'No' are used.
        """
        super().__init__(parent, question)

        # initialize and add all buttons
        self.buttons = []
        for ans in answers:
            bt = ChoiceButton(self, label=ans)
            self.main_sizer.Add(bt, proportion=1,
                                flag=wx.EXPAND | wx.ALL,
                                border=5)
            self.buttons.append(bt)

    def update_buttons(self):
        """
        Iterate through all buttons and update button borders based on selected answer.
        """
        for bt in self.buttons:
            if bt.label == self.answer:
                bt.SetWindowStyleFlag(wx.SIMPLE_BORDER)
            else:
                bt.SetWindowStyleFlag(wx.NO_BORDER)


class RangeQPanel(QPanel):
    """
    Question where the answer is provided using a slider.
    """

    def __init__(self, parent, question, val=(1, 5)):
        """
        Initializes range question (e.g. pick a value from 0 to 5).
        :param parent: Parent frame
        :param question: Question
        :param val: Tuple containing slider minimum and maximum value
        """
        super().__init__(parent, question)

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

    def update_answer(self, event):
        """
        Updates question answer.
        """
        self.answer = self.slider.GetValue()