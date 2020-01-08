from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from urllib import parse
import sys, os, logging, time, datetime
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
baidten_db = database.baidten_db(sys_platform)

# linux服务器环境下没有显示环境 需要特别配置
display = None
if sys_platform == "linux":
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

'''
退出进程
'''
def exit_all(browser_driver, exit_code = 0, log_data = ""):
    if log_data != "":
        logging.debug("be baned: xpath is " + log_data)

    browser_driver.close()
    if None != display:
        display.stop()
    
    os._exit(exit_code)
    kill_process("firefox")

'''
shit fucking happends
有时候页面未加载完 会造成xpath取节点时崩溃
'''
def avoid_being_fuck_by_selenium_xpath(browser_driver, xpath_code):
    max_retry_times = 0
    res = list()

    # 预防页面未完成加载 最多重试30次 即1分钟
    # 并且预防被网页限制访问 
    while max_retry_times < 30:
        try:
            res = browser_driver.find_elements_by_xpath(xpath_code)
            if len(res) > 0:
                break
            else:                               # 没有找到对应字段
                try:                            # 被ban了
                    browser_driver.find_element_by_xpath('//div[@class="payValidate"]')
                    exit_all(browser_driver, -1, "be baned: xpath is " + xpath_code)
                except:                         # 只是纯粹网络慢 网页未完成加载 刷新一下等十秒
                    browser_driver.refresh()
                    time.sleep(10)
                    max_retry_times += 1
        except NoSuchElementException:          # 网络出现问题导致无法访问网站 或者 网页改版了
            try:                                # 希望只是被ban 不然问题更大
                browser_driver.find_element_by_xpath('//div[@class="payValidate"]')
                exit_all(browser_driver, -1, "be baned with NoSuchElementException: xpath is " + xpath_code)
            except:                             # 同样只是因为网速过于狗屎 刷新一下
                browser_driver.refresh()
                time.sleep(10)
                max_retry_times += 1

    if len(res) <= 0:                           # 理论上只有 网速持续保持1.14514kb/s 才会跑进这里
        exit_all(browser_driver, -1, "fuck by fucking network, xpath is " + xpath_code)

    return res

'''
清理进程
'''
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
从每个专利的专属链接中提取数据
'''
def get_data_from_url(browser_driver, url):
    browser_driver.get(url)
    browser_driver.refresh()
    time.sleep(2)

    # 打表 字段对应数据
    main_matter_label2data = dict()
    main_matter_label2data["申请号"] = str()
    main_matter_label2data["申请日"] = str()
    main_matter_label2data["公开号"] = str()
    main_matter_label2data["授权公告日"] = str()
    main_matter_label2data["申请（专利权）人"] = str()
    main_matter_label2data["发明人"] = str()    

    # 主要事项的 描述字段 及 对应数据
    main_matters_labels_xpath = avoid_being_fuck_by_selenium_xpath(browser_driver, '//ul[@class="abst-info fn-clear"]/li')
    for i in range(len(main_matters_labels_xpath)):
        key_value = main_matters_labels_xpath[i].text.split('\n')
        label_key = key_value[0]
        if main_matter_label2data.get(label_key) == None:
            continue
        
        main_matter_label2data[label_key] = key_value[1]
    
    patentType_pantentName_xpath = avoid_being_fuck_by_selenium_xpath(browser_driver, '//span[@class="title Js_hl"]')[0]
    patentType_pantentName = patentType_pantentName_xpath.text.strip().split(" ")

    main_matter_label2data["专利类型"] = patentType_pantentName[0].replace('[', '').replace(']', '')
    main_matter_label2data["专利名"] = patentType_pantentName[-1]
    main_matter_label2data["法律状态"]  = avoid_being_fuck_by_selenium_xpath(browser_driver, '//div[@class="law-status law-status2"]/p')[0].text

    # debug txt
    with open("debug.txt", "wb") as debug_file:
        debug_file.write((str(main_matter_label2data) + "\n").encode("utf-8"))

    # 单独写入一个数据
    baidten_db.insert_one(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), main_matter_label2data)

'''
获取每个专利的专属链接
'''
def get_child_urls(browser_driver, go_url):
    logging.info("processing url %s", go_url)
    
    browser_driver.get(go_url)
    browser_driver.refresh()
    time.sleep(2)

    child_urls = []
    public_id_list = avoid_being_fuck_by_selenium_xpath(browser_driver, '//div[@class="fn-left g-right newList-item"]/a')
    for idx in range(0, len(public_id_list), 2):
        child_urls.append(public_id_list[idx].get_attribute("href"))
    
    return child_urls

'''
返回专利链接集合
'''
def get_child_url_set(browser_driver):
    # 搜索关键字
    key_word = str("广州医软智能科技有限公司")
    key_word_urlencode_1 = parse.quote(key_word.encode("utf-8"))
    key_word_urlencode_2 = parse.quote(key_word_urlencode_1.encode("utf-8"))    # 两次转码

    # 单页搜索数据量 10个
    default_single_page_obj_num = 10
    origin_url = "https://www.baiten.cn/results/s/" + key_word_urlencode_2 + "/.html?type=s#/"  

    # 所有专利的单独链接
    child_url_set = []

    # go to collect from page 1
    child_urls = get_child_urls(browser_driver, origin_url + str(default_single_page_obj_num) + "/" + str(1))
    child_url_set.extend(child_urls)

    # 总共含有的页数
    all_page_num_xpath = avoid_being_fuck_by_selenium_xpath(browser_driver, '//span[@class="btui-paging-totalPage"]/em')[0]
    all_page_num = int(all_page_num_xpath.text.strip())
    logging.info("totally contains %d pages", all_page_num)

    # go to collect from page 2 until end
    for page in range(2, all_page_num + 1):
        child_urls = get_child_urls(browser_driver, origin_url + str(default_single_page_obj_num) + "/" + str(page))
        child_url_set.extend(child_urls)

    # 总共有 xx 个专利
    logging.info("totally contains %d objects", len(child_url_set))

    return child_url_set

'''
启动函数
获取浏览器应用
'''
def get_driver(driver_path):
    # 尝试启动firefox浏览器
    browser_driver = webdriver.Firefox(executable_path= driver_path)

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
    
    # 获取浏览器驱动
    browser_driver = get_driver(driver_path)
    if browser_driver is None:
        return False

    # 返回专利链接集合
    child_url_set = get_child_url_set(browser_driver)

    # 从这些链接里提取数据
    for url in child_url_set:
        assert(type(url) is str)
        get_data_from_url(browser_driver, url)

    # 正常退出
    exit_all(browser_driver, 0, "finished..")

if __name__ == "__main__":
    kill_process("firefox")
    main()