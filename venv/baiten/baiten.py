from selenium import webdriver
from pyvirtualdisplay import Display
import sys, os

def run(driverPath):
    driver = webdriver.Firefox()
    driver.close()

def main():
    binPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin")
    sys.path.append(binPath)
    
    sysPlatform = sys.platform.lower()
    if sysPlatform == "linux":
        driverPath = os.path.join(binPath, "chromedriver")
    elif sysPlatform == "win32":
        driverPath = os.path.join(binPath, "chromedriver.exe")

    if not os.path.exists(driverPath):
        return False
    
    run(driverPath)
    return True

if __name__ == "__main__":
    main()