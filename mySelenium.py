# -*- coding: utf-8 -*- 
# @Filename : mySelenium.py           
# @Author : zhongbin
# @Time : 2023/12/14 15:35
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time  import sleep
import os
from Configs.configs import LOCATE_MODE,DATA_PATH,IMG_PATH
from Utlis.getCode import get_code_by_img


class MySelenium(object):
    """selenium方法的封装类"""
    def __init__(self):
        #获取浏览器驱动
        self.driver=None
        #浏览器超时时间
        self.timeout = 20
        #等待时间
        self.wait = None
        #验证码保存的名称 不一定使用
        self.code_img='code.png'

    @staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        name, value = locator
        return func(LOCATE_MODE[name], value)

    def my_find_element(self, locator):
        """寻找单个元素,此处locator为元组（By.ID,"id"）"""
        try:
            func=MySelenium.element_locator(lambda *args: self.wait.until(
            EC.presence_of_element_located(args)), locator)  # presence_of_element_located((By.ID,"acdid")) 显式等待
            return func
        except Exception as e:
            print(f"selenium方法执行失败可能是无此元素，错误信息如下！\n{e}")
            return None

    def my_find_elements(self, locator):
        """查找多个相同的元素"""
        return MySelenium.element_locator(lambda *args: self.wait.until(
            EC.presence_of_all_elements_located(args)), locator)

    def get_attrib(self, locator, value):
        """获取元素属性"""
        ele = self.my_find_element(locator)
        return ele.get_attribute(value)

    def find_element_drag(self, locator):
        """拖动到可见的元素去"""
        target = self.my_find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)

    def elements_num(self, locator):
        """获取相同元素的个数"""
        number = len(self.my_find_elements(locator))
        return number

    def element_text(self, locator):
        """获取当前的text"""
        ele=self.my_find_element(locator)
        if ele is not None:
            _text = ele.text
            return _text
        else:
            print("元素定位失败！")
            return 'null'

    ###后面的为测试用例会用到的函数名####
    def opne_brower(self, url):
        """
        打开浏览器的操作，需要设置驱动、等待器、最大化
        """
        #浏览器驱动
        if self.driver is None:
            self.driver = webdriver.Firefox()
            #等待器
            self.wait = WebDriverWait(self.driver, self.timeout)
            # 最大化浏览器
            self.driver.maximize_window()
        #打开url
            self.driver.set_page_load_timeout(60)
        try:
            #打开url
            self.driver.get(url)
            # #等待10s
            self.driver.implicitly_wait(10)
        except TimeoutException:
            #超时
            raise TimeoutException("打开超时!")

    def input_text(self, locator, txt):
        """
        在文本框中输入文本
        :param locator: 定位元素 :param txt: 输入的文本
        :return:
        """
        sleep(2)
        #定位到文本框元素
        ele = self.my_find_element(locator)
        if ele is not None:
            #输入前先清空输入框
            ele.clear()
            #输入对应的文本
            ele.send_keys(txt)
            sleep(1)
        else:
            print("文本框定位失败！")
            return "文本框定位失败！"



    def btn_click(self, locator):
        """按钮点击"""
        #定位到按钮元素，执行点击事件
        ele=self.my_find_element(locator)
        if ele is not None:
            ele.click()
            sleep(1)
        else:
            print("按钮定位失败！")

    def get_img_by_element(self,locator,imgpath):
        """获取元素的图片"""
        imgpath=os.path.join(IMG_PATH, imgpath)
        ele=self.my_find_element(locator)
        if ele is not None:
            ele.screenshot(imgpath)
        else:
            print("元素定位失败！")


    def get_code(self,locator):
        """获取验证码"""
        try:
            #验证码图片的地址
            imgpath = os.path.join(IMG_PATH, self.code_img)
            #定位到验证码图片的元素 并截图保存到imgpath
            self.my_find_element(locator).screenshot(imgpath)
            #调用接口识别图片转为字符串
            code=get_code_by_img(imgpath)
            return str(code)
        except Exception as e:
            print(f"获取验证码错误！请检查路径和识别的接口！{e}")
            return 'null'

    def input_code(self,locator,txt):
        """在验证码框中中输入验证码"""
        #获取验证码 txt的形式为 xpath,//*[@id='login_content']/div[1]/input
        code_locator=tuple(txt.split(","))
        code=self.get_code(code_locator)
        #输入验证码
        self.input_text(locator,code)
        sleep(1)


    def hold_on(self, locator):
        """定位元素进行悬停操作"""
        # 定位到要悬停的元素
        move = self.my_find_element(locator)
        if move is not None:
            # 对定位到的元素执行悬停操作
            ActionChains(self.driver).move_to_element(move).perform()
            sleep(0.5)
            return '点击操作执行成功！'
        else:
            print("元素定位失败！")
            return '元素定位失败'


    def hold_on_click(self, locator):
        """定位元素进行点击"""
        # 定位到要悬停的元素
        move = self.my_find_element(locator)
        if move is not None:
            # 对定位到的元素执行悬停操作点击
            ActionChains(self.driver).move_to_element(move).click().perform()
            sleep(0.5)
            return "元素操作成功！"
        else:
            print("元素定位失败！")
            return '元素定位失败！'


    def hold_on_double_click(self, locator):
        """定位元素进行双击"""
        # 定位到要悬停的元素
        move = self.my_find_element(locator)
        if move is not None:
            # 对定位到的元素执行悬停操作
            ActionChains(self.driver).move_to_element(move).double_click().perform()
            sleep(1)
        else:
            print("元素定位失败")


    def assert_text(self,locator,txt):
        """断言操作 验证元素标签是否正常"""
        now_txt=self.element_text(locator)
        assert now_txt == txt,'当前传入的值：%s，验证的值：%s' %(now_txt,txt)

    def input_enter(self, locator):
        """回车、tab等键入"""
        ele = self.my_find_element(locator)
        ele.send_keys(Keys.ENTER)

    def quit(self):
        # 关闭浏览器
        self.driver.quit()

    def switch_to_window(self,handles_number):
        """切换到页面"""
        handles = self.driver.window_handles
        try:
            number=int(handles_number)+1
            self.driver.switch_to.window(handles[number])
            # print(self.driver.current_window_handle,self.driver.window_handles)
            sleep(1)
        except:
            print("此页面不存在！")

    def get_img(self,imgname):
        """截图保存"""

        self.driver.get_screenshot_as_file(imgname)


    def exe_js(self,js):
        """执行js的方法"""
        self.driver.execute_script(js)
        sleep(5)

    def sleep(self,time):
        """加载时间"""
        sleep(int(time))



    """需要打开任意的url"""
    """需要定位并操作打开的窗口"""
    """需要定位并操作下拉框"""

    
