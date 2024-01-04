# -*- coding: utf-8 -*- 
# @Filename : configs.py           
# @Author : zhongbin
# @Time : 2023/12/14 15:22

import os
from selenium.webdriver.common.by import By


"""根目录"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""Data存放数据文件 比如验证码图片、文档、表格"""
DATA_PATH = os.path.join(BASE_DIR, 'Data')

#图片的位置
IMG_PATH=os.path.join(BASE_DIR,'Data//imgs')

"""页面"""
LOG_PATH = os.path.join(BASE_DIR, 'Logs')

"""报告输出目录"""
RESULT_PATH = os.path.join(BASE_DIR, 'Result')

"""数据输出的文件"""
TESTCASE_PATH = os.path.join(BASE_DIR, 'Testcase')

"""元素定位的类型"""
LOCATE_MODE = {
    'css': By.CSS_SELECTOR,
    'xpath': By.XPATH,
    'name': By.NAME,
    'id': By.ID,
    'class': By.CLASS_NAME,
    'link_text': By.LINK_TEXT
    }


