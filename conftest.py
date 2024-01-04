# -*- coding: utf-8 -*-
# @Filename : conftest.py
# @Author : zhongbin
# @Time : 2023/12/7 14:59
import pytest,os
from Utlis.mySelenium import MySelenium
ms= None
"""所有测试.py文件执行前执行一次"""
@pytest.fixture(scope='session', autouse=True)
def ms(request):
    print("测试开始!")
    global ms
    if ms is None:
        ms =MySelenium()
    def fn():
        if ms is not None:
            ms.quit()
        print("用例结束，关闭浏览器！")
    # 来看addfinalizer，叫它终结器。
    # 在用法上，addfinalizer跟yield是不同的，需要你去注册作为终结器使用的函数
    # 对于yield来说，在yield之前的在用例执行之前执行，之后的在用例执行之后执行
    request.addfinalizer(fn)
    return ms