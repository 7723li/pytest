from selenium import webdriver

option = webdriver.ChromeOptions()
option.binary_location = r"/home/lzx/Desktop/testpy/venv/bin/chromedriver"
driver = webdriver.Chrome(options=option)