# question: Is this a question? answers: yes/no
# variables yes,no = false; if answer is yes, set yes to true
# output depend on if yes/no is true

import wx
from openQuestions import OpenQFrame


if __name__ == '__main__':
    questions = {}
    app = wx.App(redirect=False)
    frame = OpenQFrame()
    app.MainLoop()