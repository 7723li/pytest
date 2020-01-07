from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import sys, os, shutil, logging

# 日志输出
logging.basicConfig(filename='baiten.log', 
                    filemode="a+", 
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%d-%M-%Y %H:%M:%S", 
                    level=logging.DEBUG)

# 系统平台
sysPlatform = sys.platform.lower()
logging.debug("\n")
logging.debug("platform : " + sysPlatform)

'''
手动将所有firefox进程删除 避免长时间积累导致服务器负载过重
'''
def kill_all_firefox_progress():
    # TODO lzx
    return

'''
启动函数
返回浏览器应用
'''
def start(driverPath):
    display = None
    if sysPlatform == "linux":
        # linux服务器环境下没有显示部件 需要特别配置
        try:
            from pyvirtualdisplay import Display
        except:
            # 安装 pyvirtualdisplay
            logging.info("install pyvirtualdisplay begin")
            logging.info(os.popen("pip3 install pyvirtualdisplay").read())
            logging.info("install pyvirtualdisplay finish")

            # 安装 xvfb
            logging.info("install xvfb begin")
            logging.info(os.popen("sudo apt-get install xvfb").read())
            logging.info("install xvfb finish")

        display = Display(visible=False, size=(900, 800))
        display.start()

    # 尝试启动浏览器进行
    try:
        driver = webdriver.Firefox(executable_path= driverPath)
    except:
        return None

    return driver

'''
获取数据
'''
def getData(driver):
    driver.get("https://www.baiten.cn/")

    # search
    search_box = driver.find_element_by_xpath('//input[@class="m-search-input-input Js_searchInput"]')
    search_box.send_keys("医软智能科技有限公司")

    search_btn = driver.find_element_by_xpath('//input[@class="m-search-submit"]')
    search_btn.send_keys(Keys.RETURN)

    # page switch
    print (driver.current_url)

    # driver.close()

def processHTML(html):
    return

'''
main函数
'''
def main():
    # binPath : 二进制文件存放路径
    binPath = os.path.join(os.path.dirname(__file__), "bin")
    
    # FireFoxPath : firefox安装路径
    # driverPath : 浏览器驱动存放路径
    if sysPlatform == "linux":
        FireFoxPath = r"/usr/bin/firefox"
        driverPath = os.path.join(binPath, "geckodriver")
    elif sysPlatform == "win32":
        FireFoxPath = r"C:\Program Files\Mozilla Firefox"
        driverPath = os.path.join(binPath, "geckodriver.exe")
    else:
        FireFoxPath = ""
        driverPath = ""

    # 驱动不存在
    if "" == driverPath or not os.path.exists(driverPath):
        logging.error("did not find firefox-Driver geckodriver")
        return False

    # 浏览器不存在
    if "" == FireFoxPath or not os.path.exists(driverPath):
        logging.error("did not find firefox-Browser")

        # Windows环境下只能手动安装
        if sysPlatform == "linux":
            logging.info("install firefox begin")
            logging.info((os.popen("sudo apt-get install firefox").read()))
            logging.info("install firefox finish")

        return False

    logging.info("FireFoxPath : " + FireFoxPath)
    logging.info("driverPath : " + driverPath)
    
    driver = start(driverPath)
    if driver is None:
        return False

    getData(driver)

    return True

if __name__ == "__main__":
    main()
    if sysPlatform == "linux":
        kill_all_firefox_progress()
