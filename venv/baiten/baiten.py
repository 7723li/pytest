from selenium import webdriver
import sys

option = webdriver.ChromeOptions()

sysPlatform = sys.platform  # 系统类型
if sysPlatform == "linux":
    option.binary_location = r"/home/lzx/Desktop/testpy/venv/bin/chromedriver"
elif sysPlatform == "win32":
    None

driver = webdriver.Chrome(options=option)