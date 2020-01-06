from selenium import webdriver
from pyvirtualdisplay import Display
import sys, os

sysPlatform = sys.platform.lower()    # 系统类型
assert(sysPlatform == "linux")

try:
    display = Display(visible=0, size=(800, 800))
except Exception as e:
    ErrorStr = str(e)
    if "No such file or directory: 'Xvfb'" in ErrorStr:
        import subprocess
        subprocess.getoutput("sudo apt-get install xvfb")
        subprocess.getoutput("pip install xvfbwrapper")
display = Display(visible=0, size=(800, 800))
display.start()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
lastdir = os.path.dirname(os.path.dirname(__file__))
sysPlatform = sys.platform.lower()
if sysPlatform == "linux":
    chrome_options.binary_location = lastdir + r"/bin/chromedriver"
elif sysPlatform == "win32":
    chrome_options.binary_location = lastdir + r"/bin/chromedriver.exe"

driver = webdriver.Chrome(options=chrome_options)