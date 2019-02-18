if __name__ == '__main__':
    print("Please use me as a module.")

def openweb(browser):
    browser.get('http://portal.ecjtu.edu.cn:8080/form/forward.action?path=/portal/portal&p=hjdHome#sd=1012')
    try:
        usr = browser.find_element_by_name('username')
        pwd = browser.find_element_by_name('password')
        usr.send_keys('1864')
        pwd.send_keys('ecjtuWj952')

        btn = browser.find_element_by_class_name('login_box_landing_btn')
        btn.click()

        browser.implicitly_wait(10)

        app_one = browser.find_element_by_class_name('app_one_title')
        app_one.click()

        window = browser.window_handles
        browser.switch_to.window(window[-1])

        score = browser.find_element_by_xpath("//li[@class='score']")
        score.click()
    except:
        print("element not found.")

