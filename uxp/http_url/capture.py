'''
Created on Sep 13, 2019

@author: 5hu5ky
'''

from selenium import webdriver
import os
import psutil
from selenium.common.exceptions import WebDriverException,\
    UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.common.alert import Alert 
import logging
import time

from .util import HTMLUtil
from uxp.common.tools import Tools
import sys
from selenium.webdriver.common import alert

class getScreenShot(object): 
    '''
    Known problems:
    - Support WebGL in headless mode: https://bugzil.la/1375585
    - Iffy alert pop-up handling or is it...?
    '''
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
    
    def __init__(self, saveDir=".", timeout=45,width=1920,height=1080, overWrite=False, verbose=False,debug=True):
        self.options  = webdriver.FirefoxOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.timeout = timeout
        self.width = width
        self.height = height
        self.overWrite = overWrite
        self.verbose = verbose
        self.debug = debug
        
        if os.path.exists(saveDir):
            self.saveDir = saveDir
        else:
            raise Exception("Save directory does not exist!")
        self.geckodriver = None
        
        if Tools.get_platform()== "Windows":
            ret, tmp = Tools.run_external("where geckodriver")
            if ret == 0:
                self.geckodriver = str(tmp[0]).strip('\r')

        elif Tools.get_platform()== "Linux":
            tmp = Tools.which("geckodriver")
            if tmp:
                self.geckodriver = tmp

        
        if not self.geckodriver:
            raise Exception("NO HEADLESS BROWSER")
            sys.exit(1)
            


    #https://stackoverflow.com/questions/46619679/in-python-how-to-check-if-selenium-webdriver-has-quit-or-not#46620600
    #https://stackoverflow.com/questions/47920639/how-to-fix-webdriverexception-message-connection-refused?noredirect=1
    def fetch(self,URI):
        time.sleep(2)
        if self.geckodriver:
            driver = webdriver.Firefox(options = self.options, executable_path = self.geckodriver, service_log_path='./geckodriver.log')
            
        filename = HTMLUtil.getFileFromURL(url=URI)
        driver_process = psutil.Process(driver.service.process.pid) 
        try:
            writepath = "{}/{}.png".format(self.saveDir, filename)
            if self.overWrite or not os.path.isfile(writepath): 
                driver.set_page_load_timeout(self.timeout)
                driver.set_window_size(self.width, self.height)
                driver.get(URI)
                driver.save_screenshot(writepath)
                driver.quit()
            else:
                print("Not writing")
        except UnexpectedAlertPresentException as ueae:
            #Funky javascript alert handling...
            alert = Alert(driver)  
            try:
                alert.accept()
                #Alert(driver).accept()
                driver.save_screenshot(writepath)
                driver.quit()
            except NoAlertPresentException as nape:
                if self.debug:
                    logging.debug(nape)
                driver.save_screenshot(writepath)
                driver.quit()
                pass
            #if self.verbose:
            #    print ("Screen Capture Error! - Page displayed a Javascript alert box")
            if self.debug:
                print (ueae)
            
        except WebDriverException as wde:
            if self.debug:
                logging.debug(wde)
            if driver_process.is_running():
                if self.verbose:
                    print ("Driver is running")
            
                firefox_process = driver_process.children()
                if firefox_process:
                    firefox_process = firefox_process[0]
            
                    if firefox_process.is_running():
                        if self.verbose:
                            print("Firefox is still running - killing the driver..")
                        driver.quit()
                    else:
                        if self.verbose:
                            print("Firefox is unresponsive, can't quit - killing the process...")
                        firefox_process.kill()
                else:
                    if self.verbose:
                        print("Driver error...")
        except Exception as ex:
            if self.verbose:
                print ("Screen Capture Error!")
            if self.debug:
                print (ex)

    def fetchMultiple(self,URIList):
        for host in URIList:
            self.fetch(host)


if __name__ == '__main__':
    c = getScreenShot()
    print(c.geckodriver)