from selenium import webdriver
from pyvirtualdisplay import Display
import sys, os

def run(driverPath):
    driver = webdriver.Chrome(driverPath)
    driver.close()

def main():
    binPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin")
    driverPath = os.path.join(binPath, "chromedriver")

    sysPlatform = sys.platform.lower()
    if sysPlatform == "linux":
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
    elif sysPlatform == "win32":
        driverPath += ".exe"

    if os.path.exists(driverPath):
        return False

    sys.path.append(binPath)
    run(driverPath)
    return True

if __name__ == "__main__":
    main()