from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import sys, os, shutil, logging

# logger
logging.basicConfig(filename='baiten.log', 
                    filemode="a+", 
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%d-%M-%Y %H:%M:%S", 
                    level=logging.DEBUG)

sysPlatform = sys.platform.lower()
logging.debug("\n")
logging.debug("platform : " + sysPlatform)

def run(driverPath):
    if sysPlatform == "linux":
        # linux服务器环境下没有显示部件 需要特别配置
        try:
            from pyvirtualdisplay import Display
        except:
            logging.info("install pyvirtualdisplay begin")
            logging.info(os.popen("pip3 install pyvirtualdisplay").read())
            logging.info("install pyvirtualdisplay finish")

            logging.info("install xvfb begin")
            logging.info(os.popen("sudo apt-get install xvfb").read())
            logging.info("install xvfb finish")

        display = Display(visible=False, size=(900, 800))
        display.start()

    try:
        driver = webdriver.Firefox(executable_path= driverPath)
    except:
        driver = None
        return False
    
    driver.get("https://www.baidu.cn/")
    driver.close()


    display.stop()

    return True

def main():
    binPath = os.path.join(os.path.dirname(__file__), "bin") # 二进制文件存放路径
    
    if sysPlatform == "linux":
        FireFoxPath = r"/usr/bin/firefox"
        driverPath = os.path.join(binPath, "geckodriver")
    elif sysPlatform == "win32":
        FireFoxPath = r"C:\Program Files\Mozilla Firefox"
        driverPath = os.path.join(binPath, "geckodriver.exe")
    else:
        FireFoxPath = ""
        driverPath = ""

    if "" == driverPath or not os.path.exists(driverPath):
        logging.error("did not find firefox-Driver geckodriver")
        return False

    if "" == FireFoxPath or not os.path.exists(driverPath):
        logging.error("did not find firefox-Browser")

        if sysPlatform == "linux":
            logging.info("install firefox begin")
            logging.info((os.popen("sudo apt-get install firefox").read()))
            logging.info("install firefox finish")

        return False

    logging.info("FireFoxPath : " + FireFoxPath)
    logging.info("driverPath : " + driverPath)
    
    return run(driverPath)

if __name__ == "__main__":
    main()