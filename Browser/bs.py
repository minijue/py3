from threading import Thread

from selenium import webdriver
from selenium.webdriver.support.select import Select

if __name__ == '__main__':
    print("Please use me as a module.")


class AutoWeb:
    def __init__(self):
        self.__browser = webdriver.Chrome()
        self.__browser.maximize_window()

        self.__browser.get('http://portal.ecjtu.edu.cn:8080/form/forward.action?path=/portal/portal&p=hjdHome#sd=1012')
        self.__browser.implicitly_wait(10)

        usr = self.__browser.find_element_by_name('username')
        pwd = self.__browser.find_element_by_name('password')
        with open('user.txt', 'r') as uf:
            uname = uf.readline()
            upwd = uf.readline()
            usr.send_keys(uname)
            pwd.send_keys(upwd)

        btn = self.__browser.find_element_by_class_name('login_box_landing_btn')
        btn.click()

        self.__browser.implicitly_wait(10)

        app_one = self.__browser.find_element_by_link_text(u'教务综合管理系统')
        app_one.click()

        window = self.__browser.window_handles
        self.__browser.switch_to.window(window[-1])

        score = self.__browser.find_element_by_xpath("//li[@class='score']")
        score.click()

    def getterms(self):  # 获取所有的学期数据
        try:
            # 选择学期，测试用代码，实际不需要
            select = self.__browser.find_element_by_xpath("//select[@id='m-term']")
            options_list = Select(select).options
            # options_list = select.find_elements_by_tag_name('option')
            termlst = []

            for option in options_list:
                termlst.append(option.text)
            return termlst
        except:
            print("element not found.")

    def sendTextByName(self, name, score, isnorm):
        ntd = self.__browser.find_element_by_xpath(f"//input[@value='{name}']")
        nname = ntd.get_attribute('name')
        nname = nname[:nname.find('.')]

        if isnorm == "norm":
            nname = nname + '.commonScore'
        elif isnorm == "exam":
            nname = nname + '.examScore'
        else:
            nname = nname + '.score'

        etd = self.__browser.find_element_by_xpath(f"//input[@name='{nname}']")
        etd.clear()
        s = str(score)
        i = s.find('.')
        if i > -1:
            s = s[:i + 3]
        etd.send_keys(s)

    def sendOptionByValue(self, name, selection):
        try:
            strxpath = f"//input[@value='{name}']"
            ctl = self.__browser.find_element_by_xpath(strxpath)
            nname = ctl.get_attribute('name')
            nname = nname[:nname.find('.')]
            nname = nname + '.fiveTypeScore'

            etd = self.__browser.find_element_by_xpath(f"//select[@name='{nname}']")
            Select(etd).select_by_visible_text(selection)
        except:
            print(f"AutoWeb.selectCombo: element {name} not found.")

    def selectCombo(self, index):  # 自动选择学期列表
        try:
            select = self.__browser.find_element_by_xpath("//select[@id='m-term']")
            Select(select).select_by_index(index)
        except:
            print("AutoWeb.selectCombo: element m-term not found.")

    def getClasses(self):  # 获取所有班级和小班数据
        th = MyThread(self.__browser)
        while not th.isFinished:
            continue
        return th.listOfClasses

    def getValuesByName(self, name):
        try:
            strxpath = f"//select[@name='{name}']"
            ctl = Select(self.__browser.find_element_by_xpath(strxpath))
            lst = []
            for o in ctl.options:
                lst.append(o.text)
            return lst, ctl.first_selected_option.text
        except:
            print(f"AutoWeb.selectCombo: element {name} not found.")

    def setOptionByName(self, name, selection):
        try:
            strxpath = f"//select[@name='{name}']"
            ctl = Select(self.__browser.find_element_by_xpath(strxpath))
            if str(selection).isdigit():
                ctl.select_by_index(selection)
            else:
                selection = selection[:selection.find('%')]
                index = int(selection) // 5 - 1
                ctl.select_by_index(index)
        except:
            print(f"AutoWeb.selectCombo: element {name} not found.")

    def openlink(self, ahref):
        if ahref is not None:
            ahref.click()
        else:
            self.__browser.back()

    def executejs(self, strlst, isnorm=True):
        # 将成绩列表整理成逗号分隔的字符串
        if ',' not in strlst:
            slst = strlst.split()
            strlst = ','.join(slst)

        # 组织 javascript 脚本字符串，分别用于平时成绩和考核成绩
        tablename = 'listCommonScoreInput' if isnorm else 'listScoreInput'
        score = 'commonScore' if isnorm else 'examScore'
        if isnorm == "total":  # 录入总评成绩
            score = "score"
        strjs = "var arr = new Array(strlst)\nfor (var i=0;i<arr.length;i++)\n{\n      var arrname = 'tablename['+i+'].commonScore'\n document.getElementsByName(arrname)[0].value = arr[i]\n}"
        strjs = strjs.replace('strlst', strlst).replace('tablename', tablename).replace('commonScore', score)

        self.__browser.execute_script(strjs)

    @property  # 浏览器属性，用于在不同模块控制浏览器
    def browser(self):
        return self.__browser


class MyThread(Thread):  # 后台线程完成班级选择页面的解析
    def __init__(self, b):
        Thread.__init__(self)

        self.__browser = b
        self.__clslst = {}
        self.__finish = False

        self.start()

    def run(self):
        key = ''
        smallc = ''

        try:
            tbl = self.__browser.find_element_by_id('task-tab')
            tr_list = tbl.find_elements_by_tag_name('tr')  # 所有行，包括标题栏和小班

            # for trx in tr_list:
            i = 1  # 跳过标题栏
            while i < len(tr_list):
                trx = tr_list[i]
                td_list = trx.find_elements_by_tag_name('td')
                if td_list is not None and len(td_list) > 1:  # 数据栏，标题栏不含td
                    attr = trx.get_attribute('class')
                    if attr.startswith('small-class'):  # 嵌套的小班表格
                        vlist = {}
                        if key != '' and (smallc in attr):  # 小班编号相同
                            ctbl = trx.find_element_by_tag_name('tbody')
                            ctr_list = ctbl.find_elements_by_tag_name('tr')
                            # for ctrx in ctr_list:
                            j = 1  # 跳过标题栏
                            while j < len(ctr_list):
                                ctrx = ctr_list[j]
                                cattr = ctrx.get_attribute('class')
                                # if cattr is not None:
                                ctd_list = ctrx.find_elements_by_tag_name('td')
                                # 列表，依次包括小班名称，平时成绩链接，考核成绩链接
                                tdl = []

                                if cattr == 'finish':  # 录入已完成，权限已关闭，仅可查看
                                    norm = exam = ctd_list[5].find_element_by_tag_name('a')
                                else:  # 录入权限开放
                                    if u'已录入' in ctd_list[3].text or u'修改' in ctd_list[3].text:
                                        norm = None
                                    else:
                                        norm = ctd_list[3].find_element_by_tag_name('a')

                                    if u'已录入' in ctd_list[4].text:
                                        exam = None
                                    else:
                                        exam = ctd_list[4].find_element_by_tag_name('a')

                                    if norm == exam is None:
                                        norm = exam = ctd_list[5].find_element_by_tag_name('a')

                                    # else:
                                    #     norm = exam = None

                                    tdl.append(norm)
                                    tdl.append(exam)
                                    vlist[ctd_list[1].text] = tdl

                                j = j + 1

                            self.__clslst[key] = vlist
                            i = i + j
                    elif attr == '':  # 教学班级，点击'分班录入'打开小班表格
                        key = td_list[1].text
                        expand = td_list[7].find_element_by_tag_name('a')
                        expand.click()

                        smallc = expand.get_attribute('data')  # 获取小班编号
                    # else:  # 跳过标题栏
                    #     continue
                i = i + 1
            self.__finish = True
        except:
            print("AutoWeb.getclasses: element not found.")

    @property
    def listOfClasses(self):
        return self.__clslst

    @property
    def isFinished(self):
        return self.__finish
