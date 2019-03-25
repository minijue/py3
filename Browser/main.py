import wx

import guiform

if __name__ == '__main__':
    app = wx.App()
    frame = guiform.MainFrame(None)
    frame.Show(True)
    app.MainLoop()
