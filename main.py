# question: Is this a question? answers: yes/no
# variables yes,no = false; if answer is yes, set yes to true
# output depend on if yes/no is true

import wx


def main():
    print("Wat is reason that you decided to go to the counsellor?")
    input_msg = "answer with 'yes' or 'no': "
    while True:
        ans = input(input_msg)
        ans = ans.lower()
        if ans == 'yes':
            print("Correct answer!")
            break
        elif ans == 'no':
            print("Wrong answer!")
            input_msg = "answer with 'yes': "
        else:
            print("Invalid input!")


class MyPanel(wx.Panel):
    frame = False

    def __init__(self, parent):
        super().__init__(parent)
        frame = parent

        button1 = wx.Button(self, label='Yes')
        button1.Bind(wx.EVT_BUTTON, self.on_button1)

        button2 = wx.Button(self, label='No')
        button2.Bind(wx.EVT_BUTTON, self.on_button2)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(button1, proportion=1,
                       flag=wx.ALL | wx.CENTER | wx.EXPAND,
                       border=5)
        main_sizer.Add(button2, 0, wx.ALL, 5)
        self.SetSizer(main_sizer)

    def on_button1(self, event):
        frame.Close()

    def on_button2(self, event):
        frame.Close()


class MyFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, title='Hello World')
        panel = MyPanel(self)
        self.Show()


if __name__ == '__main__':
    app = wx.App(redirect=False)
    frame = MyFrame()
    app.MainLoop()