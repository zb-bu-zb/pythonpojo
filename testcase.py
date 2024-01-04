# -*- coding: utf-8 -*- 
# @Filename : testcase.py           
# @Author : zhongbin
# @Time : 2023/12/14 16:17
from Utlis.parseExcel import ParseExcel
from Utlis.mySelenium import MySelenium
from Configs.configs import TESTCASE_PATH
from time import sleep
import allure
import os

class Testcase(object):

    def __init__(self,filename):
        #操作表的位置
        self.filename= os.path.join(TESTCASE_PATH,filename)
        #操作表的类对象
        self.pe = ParseExcel(self.filename)
        #调用selenium的对象
        self.ms=MySelenium()
        #子表sheet名称
        self.testcase_sheet='用例'
        self.steps_sheet='步骤'
        self.result_sheet='结果'

        #用例子表的属性对应的列位置
        self.testcase_dict=dict()
        #步骤子表的属性对应的列序号
        self.steps_dict=dict()

        #初始化一些值
        self.init_dict()
        self.init_testcase_value()
        self.init_steps_value()

    def init_dict(self):

        index1,index2=0,0
        #初始化用例子表的标题和对应的序列号
        for data in self.pe.getRowValue(self.testcase_sheet, 1):
            self.testcase_dict[data]=index1
            index1+=1
        for data in self.pe.getRowValue(self.steps_sheet, 1):
            self.steps_dict[data] = index2
            index2 += 1

    def init_testcase_value(self):
        """初始化testcase的一些属性"""
        self.testcase_id=self.testcase_dict['用例编号']
        self.testcase_name = self.testcase_dict['用例名称']
        self.testcase_content = self.testcase_dict['用例描述']
        self.testcase_stepsnumber = self.testcase_dict['步骤数']
        self.testcase_isrun = self.testcase_dict['是否执行']
        self.testcase_overtime = self.testcase_dict['执行结束时间']
        self.testcase_reult = self.testcase_dict['结果']

    def init_steps_value(self):
        """初始话步骤表的一些属性对应的序号"""
        self.steps_id = self.steps_dict['步骤编号']
        self.steps_testcase_id = self.steps_dict['用例编号']
        self.steps_no = self.steps_dict['步骤序号']
        self.steps_name = self.steps_dict['步骤名称']
        self.steps_keyword=self.steps_dict['关键字'] #用于定位元素
        self.steps_by = self.steps_dict['操作（BY）']  # 用于定位元素
        self.steps_locator = self.steps_dict['定位表达式']  # 用于定位元素
        self.steps_operate_value = self.steps_dict['操作值']  # 用于定位元素
        self.steps_time = self.steps_dict['测试执行时间']  # 用于定位元素
        self.steps_result = self.steps_dict['测试结果']  # 用于定位元素

    def run_case(self):
        testcase=self.pe.getRowValue(self.testcase_sheet,2)
        #步骤总数
        stepsnumber=testcase[self.testcase_stepsnumber]
        #用例的名称
        testcase_name=testcase[self.testcase_name]
        print(f"用例{testcase_name}开始执行，步骤数为：{stepsnumber}")
        for i in range(2, stepsnumber+2):
            steps = self.pe.getRowValue('步骤', i)
            # 执行步骤
            steps_no = steps[self.steps_no]
            # 执行步骤
            steps_name = steps[self.steps_name]
            # 执行函数名称
            steps_fuction = steps[self.steps_keyword]
            # 操作类型xpath link_text
            By = steps[self.steps_by]
            # 定位的表达式
            locate = steps[self.steps_locator]
            # 操作值
            operate_vale = steps[self.steps_operate_value]
            print(f'{steps_no}、{steps_name}: {steps_fuction}---{operate_vale}')
            try:
                sleep(1)
                if By is not None:
                    if operate_vale is not None:
                        # 有文本输入 比如普通文本框
                        getattr(self.ms, steps_fuction)((By, locate), operate_vale)
                    else:
                        # 无文本值 一般为点击事件
                        getattr(self.ms, steps_fuction)((By, locate))
                elif operate_vale is not None:
                    # 一般为打开浏览器open_brower(url)
                    getattr(self.ms, steps_fuction)(operate_vale)
                else:
                    # 无操作函数
                    getattr(self.ms, steps_fuction)()
            except Exception as e:
                print(f"步骤{steps_no}执行失败!")
                self.ms.quit()
                break
        self.ms.quit()

    def run_step(self,steps_name=None,steps_fuction=None,By=None,locate=None,operate_vale=None):
        try:
            sleep(1)
            if By is not None:
                if operate_vale is not None:
                    # 有文本输入 比如普通文本框
                    getattr(self.ms, steps_fuction)((By, locate), operate_vale)
                else:
                    # 无文本值 一般为点击事件
                    getattr(self.ms, steps_fuction)((By, locate))
            elif operate_vale is not None:
                # 一般为打开浏览器open_brower(url)
                getattr(self.ms, steps_fuction)(operate_vale)
            else:
                # 无操作函数
                getattr(self.ms, steps_fuction)()
        except Exception as e:
            print(f"步骤{steps_name}执行失败!")
            self.ms.quit()
        self.ms.quit()


    def steps(self):
        steps = self.pe.getAllRow('步骤')
        result = list()
        for v in steps[1:]:
            # 执行步骤
            steps_no = v[self.steps_no]
            # 执行步骤
            steps_name = str(steps_no)+"_"+v[self.steps_name]
            # 执行函数名称
            steps_fuction = v[self.steps_keyword]
            # 操作类型xpath link_text
            By = v[self.steps_by]
            # 定位的表达式
            locate = v[self.steps_locator]
            # 操作值
            operate_vale = v[self.steps_operate_value]

            result.append((steps_name,steps_fuction,By,locate,operate_vale,self.ms))
        return result






# if __name__ == '__main__':
#     zhihuijiaoyu_zhpf=Testcase('智慧教育-名师在线.xlsx')
#     zhihuijiaoyu_zhpf.steps()
    # zhihuijiaoyu_mszx = Testcase('智慧教育-名师在线.xlsx')
    # zhihuijiaoyu_mszx.run_case()
    #
    # zhihuijiaoyu_jzjy = Testcase('智慧教育-精准教研.xlsx')
    # zhihuijiaoyu_jzjy.run_case()


    # zhihuijiaoyu_jykb = Testcase('智慧教育-教育看板.xlsx')
    # zhihuijiaoyu_jykb.run_case()





