from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from urllib import parse
import sys, os, logging, time, datetime
import database

# 日志输出
logging.basicConfig(filename='baiten.log', 
                    filemode="w", 
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%d-%m-%Y %H:%M:%S", 
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
    import_success = False
    try:
        from pyvirtualdisplay import Display
        import_success = True
    except:
        # 安装 pyvirtualdisplay
        logging.info("install pyvirtualdisplay begin")
        logging.info(os.popen("pip3 install pyvirtualdisplay").read())
        logging.info("install pyvirtualdisplay finish")

    if import_success == False:
        from pyvirtualdisplay import Display

    display = None
    try:
        display = Display(visible=False, size=(900, 800))
    except:
        # 安装 xvfb
        logging.info("install xvfb begin")
        logging.info(os.popen("sudo apt-get install xvfb").read())
        logging.info("install xvfb finish")

    if None == display:
        display = Display(visible=False, size=(900, 800))
    display.start()

company_name = "广州医软智能科技有限公司"

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
退出进程
'''
def exit_all(browser_driver, exit_code = 0, log_data = ""):
    if log_data != "":
        logging.debug("be baned: xpath is " + log_data)
    if None != browser_driver:
        browser_driver.close()
    if None != display:
        display.stop()
    
    os._exit(exit_code)
    kill_process("firefox")

'''
从每个专利的专属链接中提取数据
'''
def get_data_from_xpath_set(total_obj_num, xpath_set):
    obj_labels = int(len(xpath_set) / total_obj_num) # 一个专利包括的字段
    for i in range(0, len(xpath_set), obj_labels):
        apply_number = xpath_set[i + 2].text
        patent_type = xpath_set[i + 3].text
        patent_name = xpath_set[i + 4].text
        public_number = xpath_set[i + 5].text
        public_date = xpath_set[i + 6].text
        apply_date = xpath_set[i + 7].text
        apply_member = company_name # 8

        try:
            moreNum_span_list = xpath_set[i + 9].find_elements_by_tag_name('span')
            for moreNum_span in moreNum_span_list:
                if '+' in moreNum_span.text:
                    moreNum_span.click()
                    break
        except:
            pass
        invent_member = ";".join([xpath.text.replace('·', '') for xpath in xpath_set[i + 9].find_elements_by_tag_name('a')])

        law_status = xpath_set[i + 10].text
        
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = [date_time, apply_number, apply_date, public_number, public_date, apply_member, invent_member, patent_type, patent_name, law_status]

        # debug txt
        with open("debug.txt", "ab+") as debug_file:
            debug_file.write((str(data) + "\n").encode("utf-8"))
            
        # 单独写入一个数据
        baidten_db.insert_one_by_list(data)

'''
避免网络太差造成异常退出
'''
def visit_url(browser_driver, go_url, xpath_code):
    max_retry_times = 30
    xpath_set_per_page = list()

    while max_retry_times > 0:
        try:
            browser_driver.get(go_url)
            browser_driver.refresh()
            time.sleep(3)
            xpath_set_per_page = browser_driver.find_elements_by_xpath(xpath_code)
            break
        except:
            time.sleep(3)
            max_retry_times -= 1

    return xpath_set_per_page

'''
所有的页面信息
'''
def get_xpath_set(browser_driver):
    xpath_set = list()

    # 搜索关键字
    key_word = "pa:(" + company_name + ")"
    key_word_urlencode_1 = parse.quote(key_word.encode("utf-8"))
    key_word_urlencode_2 = parse.quote(key_word_urlencode_1.encode("utf-8"))    # 两次转码

    # 单页搜索数据量 100个
    default_single_page_obj_num = 100
    origin_url = "https://www.baiten.cn/results/l/" + key_word_urlencode_2 + "/.html?type=l#/"
    xpath_code = '//tr[@class="Js_showTr Js_tip"]/td'

    # conllect from page 1
    go_url = origin_url + str(default_single_page_obj_num) + "/" + str(1)
    xpath_set_per_page = visit_url(browser_driver, go_url, xpath_code)
    xpath_set.extend(xpath_set_per_page)

    total_obj_num = int(browser_driver.find_element_by_xpath('//span[@class="Js_total"]').text) # 总数量
    other_go_times = int(total_obj_num / default_single_page_obj_num)    # 还剩余页数 例：共有123个 第一页100个 第二页23个

    # conllect from page 2 ~ end
    for i in range(1, other_go_times):
        go_url = origin_url + str(default_single_page_obj_num) + "/" + str(1 + i)
        xpath_set_per_page = visit_url(browser_driver, go_url, xpath_code)
        xpath_set.extend(xpath_set_per_page)

    # 数量对不上 继续处理会出问题 干脆直接退出
    if len(xpath_set) % total_obj_num != 0:
        exit_all(browser_driver, -1, "wired xpath numer...")

    return total_obj_num, xpath_set

'''
启动函数
获取浏览器应用
'''
def get_driver(driver_path):
    browser_driver = None

    # 尝试启动firefox浏览器
    try:
        browser_driver = webdriver.Firefox(executable_path=driver_path)
    except WebDriverException as webdriver_exception:
        msg = str(webdriver_exception)
        if "can't kill an exited process" in msg:
            if sys_platform == "linux":     # 重装firefox
                os.popen("sudo apt-get remove firefox").read()
                os.popen("sudo apt-get install firefox").read()

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
    if os.path.exists(driver_path) == False:
        exit_all(None, -1, "did not find firefox-Driver geckodriver")

    # 浏览器不存在
    if os.path.exists(firefox_path) == False:
        logging.error("did not find firefox-Browser")

        # 林努克丝  环境可以自动安装
        # 温斗士    环境下只能手动安装
        if sys_platform == "linux":
            print("prepare to install firefox")
            logging.info("install firefox begin")
            logging.info((os.popen("sudo apt-get install firefox").read()))
            logging.info("install firefox finish")
        else:
            exit_all(None, -1, "download firefox manully")
    else:
        logging.info("firefox_path : " + firefox_path)
        
    
    # 获取浏览器驱动
    browser_driver = get_driver(driver_path)
    if browser_driver is None:
        exit_all(browser_driver, -1, "no browser_driver")

    total_obj_num, xpath_set = get_xpath_set(browser_driver)
    get_data_from_xpath_set(total_obj_num, xpath_set)

    # 正常退出
    exit_all(browser_driver, 0, "finished..")

if __name__ == "__main__":
    kill_process("firefox")
    main()
