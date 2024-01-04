# -*- coding: utf-8 -*-
# @Filename : Test_MSZX.py
# @Author : zhongbin
# @Time : 2023/12/29 16:05
import re, os, sys
import allure
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))
import pytest
from testcase import Testcase
from Configs.configs import IMG_PATH
from time import sleep
import PIL
from Utlis.mySelenium import MySelenium
#获取表格
zhihuijiaoyu_zhpf=Testcase('智慧教育-名师在线.xlsx')
#获取步骤
steps=zhihuijiaoyu_zhpf.steps()
#截图保存的地址
res_img_path=os.path.join(IMG_PATH, "mszx")
if os.path.exists(res_img_path):
    print("文件夹存在")
else:
    os.mkdir(res_img_path)


@allure.feature("智慧教育-名师在线互联网-UI测试")
class TestMszx:
    @allure.title('执行步骤：{steps_name}')
    @pytest.mark.parametrize("steps_name,steps_fuction,By,locate,operate_vale,ms",steps)
    def test_mszx(self,steps_name,steps_fuction,By,locate,operate_vale,ms):
        # 步骤的名称、步骤的函数名、By的类型、定位符、操作值、myselenuium对象
        # print(steps_name,steps_fuction,By,locate,operate_vale,ms)
        with allure.step(f"执行{steps_name}"):
            if By is not None:
                if operate_vale is not None:
                    # 有文本输入 比如普通文本框
                    getattr(ms, steps_fuction)((By, locate), operate_vale)
                else:
                    # 无文本值 一般为点击事件
                    getattr(ms, steps_fuction)((By, locate))
            elif operate_vale is not None:
                # 一般为打开浏览器open_brower(url)
                getattr(ms, steps_fuction)(operate_vale)
            else:
                # 无操作函数
                getattr(ms, steps_fuction)()
        sleep(0.5)
        #运行结果截图
        filename=os.path.join(res_img_path,f'{steps_name}.png')
        # 截图
        ms.get_img(filename)
        #放入报告中
        with allure.step("保存图片"):
            allure.attach.file(filename,attachment_type=allure.attachment_type.PNG)



