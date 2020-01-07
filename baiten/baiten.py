from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib import parse
import sys, os, logging, time, random

# 日志输出
logging.basicConfig(filename='baiten.log', 
                    filemode="w", 
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%d-%M-%Y %H:%M:%S", 
                    level=logging.DEBUG)

# 系统平台
sys_platform = sys.platform.lower()
logging.info("\n")
logging.info("platform : " + sys_platform)

'''
从每个专利的专属链接提取数据
'''
def get_data_from_url(browser_driver, url):
    browser_driver.get(url)
    time.sleep(random.randrange(1,5))

    # 打表 字段对应数据
    main_matter_label2data = dict()
    main_matter_label2data["申请号"] = str()
    main_matter_label2data["申请日"] = str()
    main_matter_label2data["公开号"] = str()
    main_matter_label2data["授权公告日"] = str()
    main_matter_label2data["申请（专利权）人"] = str()
    main_matter_label2data["发明人"] = str()    

    # 主要事项 及其 描述字段
    main_matters_labels_xpath = browser_driver.find_elements_by_xpath('//ul[@class="abst-info fn-clear"]/li')
    for i in range(len(main_matters_labels_xpath)):
        key_value = main_matters_labels_xpath[i].text.split('\n')
        label_key = key_value[0]
        if main_matter_label2data.get(label_key) == None:
            continue
        
        main_matter_label2data[label_key] = key_value[1]
    
    patentType_pantentName_xpath = browser_driver.find_element_by_xpath('//span[@class="title Js_hl"]')
    patentType_pantentName = patentType_pantentName_xpath.text.strip().split(" ")

    main_matter_label2data["专利类型"] = patentType_pantentName[0].replace('[', '').replace(']', '')
    main_matter_label2data["专利名"] = patentType_pantentName[-1]
    main_matter_label2data["法律状态"] = browser_driver.find_element_by_xpath('//div[@class="law-status law-status2"]/p').text

    print(url)
    with open("debug.txt", "ab+") as debugtxt:
        debugtxt.write((str(main_matter_label2data) + "\n").encode("utf-8"))

'''
获取每个专利的专属链接
'''
def get_child_urls(browser_driver, go_url):
    child_urls = []

    logging.info("processing url %s", go_url)
    browser_driver.get(go_url)
    time.sleep(random.randrange(1,5))   # 稍作停顿

    public_id_list = browser_driver.find_elements_by_xpath('//a[contains(@title, "公开号") and @class="c-blue"]')
    for public_id in public_id_list:
        child_urls.append(public_id.get_attribute("href"))
    
    return child_urls

'''
启动浏览器
'''
def start_browser(browser_driver):
    # 搜索关键字
    key_word = str("广州医软智能科技有限公司")
    key_word_urlencode_1 = parse.quote(key_word.encode("utf-8"))
    key_word_urlencode_2 = parse.quote(key_word_urlencode_1.encode("utf-8"))    # 两次转码

    # 单页搜索数据量 10个
    single_page_obj_num = 10
    origin_url = "https://www.baiten.cn/results/s/" + key_word_urlencode_2 + "/.html?type=s#/"  

    # 所有专利的单独链接
    child_url_set = []

    # go to collect from page 1
    child_urls = get_child_urls(browser_driver, origin_url + str(single_page_obj_num) + "/" + str(1))
    child_url_set.extend(child_urls)

    # 总共含有的页数
    all_page_num_xpath = browser_driver.find_element_by_xpath('//span[@class="btui-paging-totalPage"]/em')
    all_page_num = int(all_page_num_xpath.text.strip())
    logging.info("totally contains %d pages", all_page_num)

    # go to collect from page 2 until end
    for page in range(2, all_page_num + 1):
        child_urls = get_child_urls(browser_driver, origin_url + str(single_page_obj_num) + "/" + str(page))
        child_url_set.extend(child_urls)

    # 总共有 xx 个专利
    logging.info("totally contains %d objects", len(child_url_set))

    # 从这些链接里提取数据
    for url in child_url_set:
        assert(type(url) is str)
        get_data_from_url(browser_driver, url)

    browser_driver.close()

'''
启动函数
返回浏览器应用
'''
def get_driver(driver_path):
    display = None
    if sys_platform == "linux":
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

    # 尝试启动firefox浏览器
    try:
        browser_driver = webdriver.Firefox(executable_path= driver_path)
    except:
        return None

    return browser_driver

'''
main函数
'''
def main():
    # binPath : 自备二进制文件存放路径
    binPath = os.path.join(os.path.dirname(__file__), "bin")
    
    # firefox_path  : firefox安装路径
    # driver_path   : 自备浏览器驱动存放路径
    if sys_platform == "linux":
        firefox_path = r"/usr/bin/firefox"
        driver_path = os.path.join(binPath, "geckodriver")
    elif sys_platform == "win32":
        firefox_path = r"C:\Program Files\Mozilla Firefox"
        driver_path = os.path.join(binPath, "geckodriver.exe")
    else:
        firefox_path = ""
        driver_path = ""

    # 驱动不存在
    if "" == driver_path or not os.path.exists(driver_path):
        logging.error("did not find firefox-Driver geckodriver")
        return False

    # 浏览器不存在
    if "" == firefox_path or not os.path.exists(driver_path):
        logging.error("did not find firefox-Browser")

        # 林努克丝  环境可以自动安装
        # 温斗士    环境下只能手动安装
        if sys_platform == "linux":
            logging.info("install firefox begin")
            logging.info((os.popen("sudo apt-get install firefox").read()))
            logging.info("install firefox finish")

        return False

    logging.info("firefox_path : " + firefox_path)
    logging.info("driver_path : " + driver_path)

    random.seed(time.time())
    
    # 获取浏览器驱动
    browser_driver = get_driver(driver_path)
    if browser_driver is None:
        return False

    # 开启浏览器
    start_browser(browser_driver)

    return True

if __name__ == "__main__":
    main()
    if sys_platform == "linux":
        killff = os.popen("kill -9 $(pidof firefox)").read()
        logging.debug("kill firefox " + killff)
