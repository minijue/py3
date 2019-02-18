import wx

import toList


class MainFrame(wx.Frame):
    def __init__(self, superior):
        wx.Frame.__init__(self, parent=superior, id=wx.ID_ANY, title=u'华东交通大学 - 成绩自动录入', pos=(700, 400), \
                          size=(370, 220), style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        panel = wx.Panel(self, -1)
        self.label = wx.StaticText(panel, -1, u'请选择输入模式：', pos=(30, 30))
        self.raido1 = wx.RadioButton(panel, -1, u'从Excel文件导入', pos=(100, 60))
        self.raido2 = wx.RadioButton(panel, -1, u'手动粘贴', pos=(100, 90))

        self.buttonOK = wx.Button(panel, -1, u"确定", pos=(90, 136))
        self.Bind(wx.EVT_BUTTON, self.onButtonOK, self.buttonOK)

        self.buttonCancel = wx.Button(panel, -1, u"取消", pos=(190, 136))
        self.Bind(wx.EVT_BUTTON, self.onButtonCancel, self.buttonCancel)

    def onButtonOK(self, event):
        self.Show(False)
        if self.raido1.GetValue():
            print('hello')
        else:
            fr = MannulFrame(self)
            fr.Show(True)

    def onButtonCancel(self, event):
        self.Destroy()


class MannulFrame(wx.Frame):
    def __init__(self, superior):
        wx.Frame.__init__(self, parent=superior, id=wx.ID_ANY, title=u'手动粘贴成绩', pos=(700, 400), \
                          size=(370, 220), style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        panel = wx.Panel(self, -1)
        self.label = wx.StaticText(panel, -1, u'请将成绩列表复制后粘贴至下列文本框：', pos=(30, 30))
        self.text = wx.TextCtrl(panel, -1, "", pos=(30, 55), size=(300, 70), style=wx.TE_MULTILINE)

        self.buttonOK = wx.Button(panel, -1, u"确定", pos=(90, 136))
        self.Bind(wx.EVT_BUTTON, self.onButtonOK, self.buttonOK)

        self.buttonCancel = wx.Button(panel, -1, u"取消", pos=(190, 136))
        self.Bind(wx.EVT_BUTTON, self.onButtonCancel, self.buttonCancel)

    def onButtonOK(self, event):
        txt = self.text.GetValue()
        numl = toList.tonumlist(txt)

    def onButtonCancel(self, event):
        self.Parent.Show(True)
        self.Destroy()


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
