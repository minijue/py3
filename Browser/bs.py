from threading import Thread

from selenium import webdriver
from selenium.webdriver.support.select import Select

if __name__ == '__main__':
    print("Please use me as a module.")


class AutoWeb:
    def __init__(self):
        # self.__browser = webdriver.Chrome(executable_path=r'C:\Users\jue95\AppData\Local\Google\Chrome\Application\chromedriver.exe') # for Windows
        self.__browser = webdriver.Chrome()

    def openweb(self):
        self.__browser.get('http://portal.ecjtu.edu.cn:8080/form/forward.action?path=/portal/portal&p=hjdHome#sd=1012')
        try:
            usr = self.__browser.find_element_by_name('username')
            pwd = self.__browser.find_element_by_name('password')
            usr.send_keys('1864')
            pwd.send_keys('ecjtuWj952')

            btn = self.__browser.find_element_by_class_name('login_box_landing_btn')
            btn.click()

            self.__browser.implicitly_wait(10)

            app_one = self.__browser.find_element_by_class_name('app_one_title')
            app_one.click()

            window = self.__browser.window_handles
            self.__browser.switch_to.window(window[-1])

            score = self.__browser.find_element_by_xpath("//li[@class='score']")
            score.click()
        except:
            print("element not found.")

    def getterms(self):  # 获取所有的学期数据
        try:
            self.openweb()
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

    def selectCombo(self, index):  # 自动选择学期列表
        try:
            select = self.__browser.find_element_by_xpath("//select[@id='m-term']")
            Select(select).select_by_index(index)
        except:
            print("AutoWeb.selectCombo: element not found.")

    def getClasses(self):  # 获取所有班级和小班数据
        th = MyThread(self.__browser)
        while not th.isFinished:
            continue
        return th.listOfClasses

    def openlink(self, ahref):
        if ahref is not None:
            ahref.click()
        else:
            self.__browser.back()

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
                                if (cattr is not None) and (cattr != ''):
                                    ctd_list = ctrx.find_elements_by_tag_name('td')
                                    # 列表，依次包括小班名称，平时成绩链接，考核成绩链接
                                    tdl = []

                                    if cattr != 'finish':
                                        norm = ctd_list[3].find_element_by_tag_name('a')
                                        exam = ctd_list[4].find_element_by_tag_name('a')
                                    else:  # 录入权限已关闭，仅可查看
                                        norm = exam = ctd_list[5].find_element_by_tag_name('a')

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
