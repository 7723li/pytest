from selenium import webdriver
from pyvirtualdisplay import Display
import sys, os

def run(driverPath):
    options = webdriver.FirefoxOptions()
    options.bineryPath = driverPath

    driver = webdriver.Firefox(firefox_options=options)
    driver.get("www.baidu.com")
    driver.close()

def main():
    binPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin")   # 二进制文件夹 ubuntu环境下 作为虚拟环境充当系统路径
    
    sysPlatform = sys.platform.lower()
    if sysPlatform == "linux":
        driverPath = os.path.join(binPath, "geckodriver")
    elif sysPlatform == "win32":
        driverPath = os.path.join(binPath, "geckodriver.exe")

    if not os.path.exists(driverPath):
        return False
    
    run(driverPath)
    return True

if __name__ == "__main__":
    main()