import sys
import threading

import wx

import bs
import readexcel as rxl

aw = bs.AutoWeb()

hasnorm = True

# 自动录入平时成绩
def AutoNorm(ef):
    global hasnorm
    cs = ef.getClasses()
    clst = aw.getClasses()

    for ckey in clst:
        if '课程设计' not in ckey:
            sclass = clst[ckey]
            for c in sclass:
                ci = cs.__next__()

                sos = ci.GetStudents()
                if list(sos.values())[0][0] is not None:
                    ci.norm = sclass[c][0]
                    if ci.norm is not None:
                        aw.openlink(ahref=ci.norm)
                        # 设置平时成绩比例
                        aw.setOptionByName("commonScale", ci.scale)

                        # 逐个录入成绩
                        for cn in sos:
                            aw.sendTextByName(cn, sos[cn][0], "norm")

                        # 临时保存并返回
                        try:
                            aw.browser.find_element_by_class_name('temp-save').click()
                            # time.sleep(5)
                        except:
                            pass
                        aw.openlink(None)
                        # aw.browser.find_element_by_class_name('back').click()

                        # 刷新数据
                        clst = aw.getClasses()
                        sclass = clst[ckey]
                else:
                    hasnorm = False
        else:
            hasnorm = False


# 自动录入考核成绩
def AutoExam(ef):
    cs = ef.getClasses()
    aw.browser.refresh()
    clst = aw.getClasses()

    for ckey in clst:
        sclass = clst[ckey]
        for c in sclass:
            ci = cs.__next__()

            ci.norm = sclass[c][0]
            if ci.norm is not None and hasnorm:
                if wx.MessageDialog(None, u"请先提交所有班级平时成绩后再录入考核成绩！", u"考核成绩",
                                    wx.OK | wx.ICON_QUESTION).ShowModal() == wx.ID_OK:
                    sys.exit()
                break
            ci.exam = sclass[c][1]
            if ci.exam is not None:
                aw.openlink(ahref=ci.exam)
                sos = ci.GetStudents()
                if not hasnorm:
                    if (None, '中等') in sos.values():
                        scores = 'fiveTypescore'
                    else:
                        scores = 'score'
                    score = aw.browser.find_element_by_id(scores)
                    score.click()

                # 逐个录入成绩
                for cn in sos:
                    if hasnorm:
                        aw.sendTextByName(cn, sos[cn][1], "exam")
                    else:
                        aw.sendOptionByValue(cn, sos[cn][1])

                # 临时保存并返回
                aw.browser.find_element_by_class_name('temp-save').click()
                # time.sleep(5)
                # aw.browser.find_element_by_class_name('back').click()
                aw.openlink(None)
                if not hasnorm:
                    aw.openlink(None)

                # 刷新数据
                clst = aw.getClasses()
                sclass = clst[ckey]


class MainFrame(wx.Frame):
    def __init__(self, superior):

        wx.Frame.__init__(self, parent=superior, id=wx.ID_ANY, title=u'华东交通大学 - 成绩自动录入', pos=(700, 400),
                          size=(370, 220),
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.Bind(wx.EVT_CLOSE, self.onClose)

        panel = wx.Panel(self, -1)
        self.label = wx.StaticText(panel, -1, u'请选择输入模式：', pos=(30, 30))
        self.radio1 = wx.RadioButton(panel, -1, u'从Excel文件导入', pos=(100, 60))
        self.radio2 = wx.RadioButton(panel, -1, u'手动粘贴', pos=(100, 90))

        self.buttonOK = wx.Button(panel, -1, u"确定", pos=(90, 136))
        self.Bind(wx.EVT_BUTTON, self.onButtonOK, self.buttonOK)

        self.buttonCancel = wx.Button(panel, -1, u"取消", pos=(190, 136))
        self.Bind(wx.EVT_BUTTON, self.onButtonCancel, self.buttonCancel)

    def onClose(self, event):
        aw.browser.quit()
        self.Destroy()

    def onButtonOK(self, event):
        self.Show(False)

        if self.radio1.GetValue():
            # 自动从 Excel 文件导入界面
            fr = ExcelFrame(self)
            fr.Show(True)
        else:
            # 手动
            tlst = aw.getterms()
            if len(tlst) != 0:
                fr = MannulFrame(self, tlst)
                fr.Show(True)
            else:
                aw.browser.quit()
                self.Destroy()

    def onButtonCancel(self, event):
        self.onClose(event)


class ExcelFrame(wx.Frame):
    def __init__(self, superior):
        wx.Frame.__init__(self, parent=superior, id=wx.ID_ANY, title=u'从Excel文件导入', pos=(700, 400), \
                          size=(450, 160),
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.Bind(wx.EVT_CLOSE, self.onClose)

        panel = wx.Panel(self, -1)

        self.label1 = wx.StaticText(panel, -1, u'请选择 Excel 文件路径：', pos=(30, 30))
        self.pathText = wx.TextCtrl(panel, -1, "", pos=(170, 25), size=(170, 25), style=wx.TE_LEFT)
        self.btnBrowse = wx.Button(panel, -1, "...", pos=(350, 25), size=(50, 25))
        self.Bind(wx.EVT_BUTTON, self.onBtnBrowse, self.btnBrowse)

        self.buttonOK = wx.Button(panel, -1, u"确定", pos=(120, 76))
        self.Bind(wx.EVT_BUTTON, self.onButtonOK, self.buttonOK)

        self.buttonCancel = wx.Button(panel, -1, u"取消", pos=(220, 76))
        self.Bind(wx.EVT_BUTTON, self.onButtonCancel, self.buttonCancel)

    def onClose(self, event):
        aw.browser.quit()
        self.Parent.Destroy()
        self.Destroy()

    def onBtnBrowse(self, event):
        wildcard = u"Excel 文件 (*.xlsx, *.xls)|*.xlsx;*.xls|All files (*.*)|*.*"
        with wx.FileDialog(self, "打开成绩文件", wildcard=wildcard, style=wx.FD_OPEN) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_OK:
                self.pathText.SetValue(fileDialog.GetPath())

    def onButtonOK(self, event):
        # 打开 excel 文件，自动完成平时成绩录入并自动保存
        self.Enable(False)
        pa = self.pathText.GetLineText(0)
        if pa != '':
            ef = rxl.ExcelFile(pa)
            t1 = threading.Thread(target=AutoNorm, name="", args=(ef,))
            t1.start()
            t1.join()

            # 确认平时成绩后，自动录入考核成绩
            with wx.MessageDialog(None, u"平时成绩录入完毕，请手工核对并提交后，单击确定继续录入考核成绩", u"平时成绩",
                                  wx.YES_NO | wx.ICON_QUESTION) as dlg:
                if dlg.ShowModal() == wx.ID_YES:
                    t2 = threading.Thread(target=AutoExam, name="", args=(ef,))
                    t2.start()
                    t2.join()

        self.onClose(None)
        wx.MessageDialog(None, u"考核成绩录入完毕，请不要忘记手工核对并提交！", u"考核成绩",
                         wx.OK | wx.ICON_QUESTION).ShowModal()

    def onButtonCancel(self, event):
        self.Parent.Show(True)
        self.Destroy()


class MannulFrame(wx.Frame):
    def __init__(self, superior, keys):
        wx.Frame.__init__(self, parent=superior, id=wx.ID_ANY, title=u'选择班级', pos=(700, 400), \
                          size=(450, 220),
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.Bind(wx.EVT_CLOSE, self.onClose)

        panel = wx.Panel(self, -1)

        self.sclass = {}
        self.norm = None

        self.label1 = wx.StaticText(panel, -1, u'请选择学期：', pos=(30, 30))
        self.combo1 = wx.ComboBox(panel, -1, value=keys[0], choices=keys, pos=(130, 26), size=(290, 26))
        self.Bind(wx.EVT_COMBOBOX, self.onTermSelected, self.combo1)

        self.label2 = wx.StaticText(panel, -1, u'请选择班级：', pos=(30, 65))
        self.combo2 = wx.ComboBox(panel, -1, value='', choices=[], pos=(130, 61), size=(290, 26))
        self.Bind(wx.EVT_COMBOBOX, self.onClassSelected, self.combo2)

        self.label3 = wx.StaticText(panel, -1, u'请选择小班：', pos=(30, 100))
        self.combo3 = wx.ComboBox(panel, -1, value=u'选择小班，打开成绩录入页面', choices=[], pos=(130, 96), size=(290, 26))
        self.Bind(wx.EVT_COMBOBOX, self.onSClassSelected, self.combo3)

        self.radio1 = wx.RadioButton(panel, -1, u'平时成绩', pos=(130, 140))
        self.radio1.SetValue(True)
        self.radio2 = wx.RadioButton(panel, -1, u'考核成绩', pos=(230, 140))

        self.Bind(wx.EVT_CLOSE, self.onClose)

        # 默认选中的学期
        self.combo1.SetSelection(0)
        self.onTermSelected(None)

    def onClose(self, event):
        aw.browser.quit()
        self.Parent.Destroy()
        self.Destroy()

    def onTermSelected(self, event):
        aw.selectCombo(self.combo1.GetSelection())
        # 获取所有班级列表（字典，值是对应的小班dict），并显示名称
        self.clst = aw.getClasses()
        self.combo2.Set(list(self.clst.keys()))

        self.combo2.SetSelection(0)

        # 小班选择
        self.onClassSelected(event)

    def onClassSelected(self, event):
        key = self.combo2.GetStringSelection()
        if key != '':
            # 获取所有小班列表（字典，值是超链接list），并显示其名称
            self.sclass = self.clst[key]
            keys = self.sclass.keys()
            self.combo3.Set(list(keys))

            self.combo3.Insert(u'选择小班，打开成绩录入页面', 0)
            self.combo3.SetSelection(0)

    def onSClassSelected(self, event):
        # 打开小班对应的录入页面
        if self.combo3.GetSelection() > 0:
            sc = self.combo3.GetStringSelection()
            self.norm = self.sclass[sc][0]
            exam = self.sclass[sc][1]
            finished = False
            if (self.norm == exam) and (self.norm is None):
                wx.MessageBox(u'录入权限尚未开放', u'提示！')
            else:
                if self.norm == exam:
                    wx.MessageBox(u'录入已完成，仅可查看', u'提示！')
                    finished = True

                if self.norm is None:
                    self.radio2.SetValue(True)

                if exam is None:
                    self.radio1.SetValue(True)

                link = exam if self.radio2.GetValue() else self.norm
                aw.openlink(ahref=link)

                if not finished:
                    self.Show(False)

                    fr = PasteFrame(self, finished, self.radio1.GetValue())
                    fr.Show(True)


class PasteFrame(wx.Frame):
    def __init__(self, superior, finished, isNorm):
        wx.Frame.__init__(self, parent=superior, id=wx.ID_ANY, title=u'手动粘贴成绩', pos=(700, 400), \
                          size=(450, 250),
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.isNorm = isNorm
        self.scores = {'百分制': 'score', '两级分制': 'twoTypescore', '五级分制': 'fiveTypescore'}
        panel = wx.Panel(self, -1)

        self.Parent.__class__ = MannulFrame

        lbltxt = u'平时成绩比例：' if self.isNorm else u'成绩类型：'
        self.label1 = wx.StaticText(panel, -1, lbltxt, pos=(30, 15))
        self.combo = wx.ComboBox(panel, -1, pos=(120, 13))

        lbltxt = u'请将成绩列表复制后粘贴至下列文本框：'
        self.label2 = wx.StaticText(panel, -1, lbltxt, pos=(30, 55))
        self.text = wx.TextCtrl(panel, -1, "", pos=(30, 85), size=(390, 70), style=wx.TE_MULTILINE)

        self.buttonOK = wx.Button(panel, -1, u"确定", pos=(130, 170))
        if finished:
            self.text.SetEditable(False)
            self.buttonOK.Disable()
        else:
            if self.isNorm:
                lstoption, v = aw.getValuesByName("commonScale")
                self.combo.Set(lstoption)
                self.combo.SetValue(v)
            else:
                if self.Parent.norm is not None:
                    try:  # 需要选择成绩类型
                        _ = aw.browser.find_element_by_id("score")
                        self.combo.Set(list(self.scores.keys()))
                        self.combo.SetValue('百分制')

                        self.text.SetEditable(False)
                        self.buttonOK.Disable()
                    except:  # 不需要选择
                        self.combo.Disable()
                        self.text.SetEditable(True)
                        self.buttonOK.Enable()
                else:
                    self.combo.Disable()
                    self.text.SetEditable(True)
                    self.buttonOK.Enable()

            self.Bind(wx.EVT_COMBOBOX, self.onSelectScale, self.combo)
            self.Bind(wx.EVT_BUTTON, self.onButtonOK, self.buttonOK)

        self.buttonCancel = wx.Button(panel, -1, u"取消", pos=(230, 170))
        self.Bind(wx.EVT_BUTTON, self.onButtonCancel, self.buttonCancel)

        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onSelectScale(self, event):
        if self.isNorm:
            aw.setOptionByName("commonScale", self.combo.GetSelection())
        else:
            if self.text.IsEditable() is False:
                v = self.combo.GetStringSelection()
                try:
                    score = aw.browser.find_element_by_id(self.scores[v])
                    score.click()
                    self.combo.Disable()
                except:
                    pass
                finally:
                    self.text.SetEditable(True)
                    self.buttonOK.Enable()

    def onButtonOK(self, event):
        txt = self.text.GetValue()
        sel = self.combo.GetStringSelection()
        type = list(self.scores.keys())
        if sel in type:
            aw.executejs(txt, 'total')  # 直接录入总评成绩
        else:
            aw.executejs(txt, self.isNorm)

        # 录入完临时保存成绩
        aw.browser.find_element_by_class_name('temp-save').click()

        # 返回
        aw.openlink(None)

        self.Parent.Show(True)
        self.Parent.onTermSelected(None)
        self.Destroy()

    def onButtonCancel(self, event):
        aw.openlink(None)
        if u'分' in self.combo.GetStringSelection():
            aw.openlink(None)

        self.Parent.Show(True)
        self.Parent.onTermSelected(None)
        self.Destroy()

    def onClose(self, event):
        aw.browser.quit()
        self.Parent.Destroy()
        self.root.Destroy()
        self.Destroy()


if __name__ == '__main__':
    print("Please use me as a module.")
