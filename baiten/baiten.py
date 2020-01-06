from selenium import webdriver
from pyvirtualdisplay import Display
import sys, os, shutil

def run(driverPath):
    driver = webdriver.Firefox(executable_path= driverPath)
    driver.get("www.baidu.com")
    driver.close()

def main():
    binPath = os.path.join(os.path.dirname(__file__), "bin") # 二进制文件存放路径
    
    sysPlatform = sys.platform.lower()
    if sysPlatform == "linux":
        driverPath = os.path.join(binPath, "geckodriver")
    elif sysPlatform == "win32":
        driverPath = os.path.join(binPath, "geckodriver.exe")
    else:
        driverPath = ""

    if "" == driverPath or not os.path.exists(driverPath):
        return False
    
    #driverBinary = FirefoxBinary('C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
    run(driverPath)
    return True

if __name__ == "__main__":
    main()