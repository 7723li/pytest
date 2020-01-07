from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from urllib import parse
import sys, os, logging, time, random
import database

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

# 针对佰腾应用的数据库
baidten_db = database.baidten_db()

'''
shit fucking happends
有时候页面未加载完 会造成xpath取节点时崩溃
'''
def avoid_being_fuck_by_selenium_xpath(browser_driver, xpath_code):
    max_retry_times = 20
    load_sunccess = False
    res = None

    while False == load_sunccess and max_retry_times > 0:
        try:
            res = browser_driver.find_elements_by_xpath(xpath_code)
            load_sunccess = True
        except NoSuchElementException:
            time.sleep(1)
            max_retry_times -= 1

    if res is None:
        logging.debug("fuck by selenium")

    assert(res is not None)
    return res

def kill_process(prog_name):
    cmd = "ps -ef | grep \"" + prog_name + "\" | grep -v grep | awk '{print $2}'"
    find_res = os.popen(cmd).read().split('\n')

    logging.info("find %d %s running", len(find_res), prog_name)

    kill = 0
    for pid in find_res:
        os.popen("kill " + pid).read()
        kill += 1

    logging.info("kill %d %s", kill, prog_name)

'''
从每个专利的专属链接提取数据
'''
def get_data_from_url(browser_driver, url):
    get_url_success = False
    retry_times = 0
    while not get_url_success and retry_times < 5:
        try:
            browser_driver.get(url)
            get_url_success = True
        except NoSuchElementException:
            try:
                is_banded_xpath = avoid_being_fuck_by_selenium_xpath(browser_driver, '//div[@class="payValidate"]')[0]
                logging.debug("be baned : " + is_banded_xpath.text)
            except:
                retry_times += 1

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
    main_matters_labels_xpath = avoid_being_fuck_by_selenium_xpath(browser_driver, '//ul[@class="abst-info fn-clear"]/li')
    for i in range(len(main_matters_labels_xpath)):
        key_value = main_matters_labels_xpath[i].text.split('\n')
        label_key = key_value[0]
        if main_matter_label2data.get(label_key) == None:
            continue
        
        main_matter_label2data[label_key] = key_value[1]
    
    patentType_pantentName_xpath = avoid_being_fuck_by_selenium_xpath(browser_driver, '@class="title Js_hl"')[0]
    patentType_pantentName = patentType_pantentName_xpath.text.strip().split(" ")

    main_matter_label2data["专利类型"] = patentType_pantentName[0].replace('[', '').replace(']', '')
    main_matter_label2data["专利名"] = patentType_pantentName[-1]
    main_matter_label2data["法律状态"]  = avoid_being_fuck_by_selenium_xpath(browser_driver, '//div[@class="law-status law-status2"]/p')[0].text

    print(url)
    baidten_db.insert_one(main_matter_label2data)

'''
获取每个专利的专属链接
'''
def get_child_urls(browser_driver, go_url):
    child_urls = []

    logging.info("processing url %s", go_url)
    for i in range(3):
        browser_driver.get(go_url)
        time.sleep(1)

    time.sleep(random.randrange(1,5))   # 稍作停顿

    public_id_list = avoid_being_fuck_by_selenium_xpath(browser_driver, '//a[contains(@title, "公开号") and @class="c-blue"]')
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
    all_page_num_xpath = avoid_being_fuck_by_selenium_xpath(browser_driver, '//span[@class="btui-paging-totalPage"]/em')[0]
    all_page_num = int(all_page_num_xpath.text.strip())
    logging.info("totally contains %d pages", all_page_num)

    # go to collect from page 2 until end
    for page in (2, all_page_num + 1):
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
    kill_process("firefox")

    main()

    kill_process("firefox")