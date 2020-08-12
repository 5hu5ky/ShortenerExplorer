'''
Created on May 10, 2018

@author: 5hu5ky

'''
import concurrent.futures
import random, string
import requests
import logging
from datetime import datetime


import urllib3
from urllib3.exceptions import NewConnectionError
from uxp.http_url.util import HTMLUtil
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




from uxp.http_url.capture import getScreenShot
from uxp.common.tools import Tools

class Explorer(object):
    '''
     A class for exploring URL shorteners safely.
     
    #TODO: 
    1. Check if there is a list of checked hashes exists  hash:service if yes, load them up in to __CHECKED_HASH
    -- Keep the hashes per mission if the evidence path has the hash list use it
    -- Or do we use the log file
    2. Write the hashes to a file before exiting...
    3. Detect keyboard Ctrl+C for long loop cycles
    4. User-Agent randomization
    5. Word Freq analysis on web pages
    6. Filters - for notifications for areas of interest (keywords)
    7. Create an option that tries combinations instead of permutations...
    8. Create an argument for downloading hashes via file
    
    #DONE:
    1. Auto platform geckodrive detection - DONE
    2. Implement a limit in case you do not want to run this infinitely. - DONE
    3. Implement command line args - DONE
    4. PhantomJS does not work on Windows - REMOVE - DONE
    5. Implement a Queue so that there is a limit to threads - DONE
    6. Create an output folder for the mission and logs - DONE
    
 
    '''
    service = "https://bit.ly"
    __HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}
    __VERIFYSSL=False,
    __CHECKED_HASH = set()

    def __init__(self, shortnerService="https://bit.ly", url=None, hashLength=6, userAgent=None,
                 evidenceCollect=False, evidenceSavePath=".", search=[], debug=False, verbose=False, log=False):
        '''
        Constructor
        '''
        if userAgent is not None:
            self.__HEADERS = userAgent
        self.hashLength = hashLength
        if shortnerService is not None:
            self.service = shortnerService
        self.debug = debug
        self.verbose = verbose
        self.missionTime = datetime.now().strftime('%H%M%S%m%d%Y')
        self.evidenceCollect = evidenceCollect
        self.evidenceSavePath = evidenceSavePath
        self.log =log
        self.logpath = os.path.join(self.evidenceSavePath,self.missionTime+".log")
        self.screenCap = getScreenShot(saveDir=evidenceSavePath,overWrite=False,verbose=verbose,debug=debug)
        self.max_workers = 5
        self.url = url
        self.search = search        
        
        if self.debug:
            #logging.basicConfig(level=logging.DEBUG)
            pass
        
    def setClickThrough(self,status):
        self.clickthrough = status
    
    def getCheckedHashes(self):
        return self.__CHECKED_HASH
    
    def setLogPath(self,logpath):
        self.logpath = logpath
    
    def setCampaign(self,campaignName):
        self.campaign_name = campaignName
        self.hashpath = os.path.join(self.evidenceSavePath,"hashlist")

    
    def linkFetcherWorker(self, urlhashx=None):
        result = 000
        try:           
            if urlhashx.find("http_url://")!=-1 or urlhashx.find("https://")!=-1:
                url = urlhashx
            elif urlhashx not in self.__CHECKED_HASH:
                url = self.service + "/" + urlhashx
            else:
                if self.verbose:
                    print ("Already checked!")
                return result
            
            if self.verbose:
                logging.info("fetching {}".format(url))
            
            response = requests.get(url=url,headers=self.__HEADERS,verify=False)
            html_doc = response.text
            result = response.status_code
            '''
            TODO:
            - Do something with the content
            '''
            if self.verbose:
                logging.info(response.status_code)
            
            if response.status_code != 404:
                if self.verbose:
                    print ("%s,%s" %(urlhashx, response.url))

                if self.service.find('bit.ly') != -1:
                    if HTMLUtil.isBitlyWarningPage(html_doc) and self.clickthrough:
                        url = HTMLUtil.getLink(html_doc)
                if self.evidenceCollect:
                    if self.search == [] or HTMLUtil.pageContainsString(html_doc, self.search)>0:
                        self.screenCap.fetch(url)
                if self.log:                  
                    Tools.resultWrite(filepath=self.logpath,content="{},{},{}".format(urlhashx, url, response.url))
            else:
                if self.verbose:
                    print ("{},{},{}".format(urlhashx, response.url, str(response.status_code)))
                #return url, response.url
            
        
        except NewConnectionError as nce:
            return 000
            if self.debug:
                logging.debug(nce, exc_info=True)
        except Exception as ex:
            if self.debug:
                logging.debug(ex, exc_info=True)
            return -1
        
        self.__CHECKED_HASH.add(urlhashx)
        
        if self.campaign_name != None:
            Tools.resultWrite(self.hashpath, urlhashx)
        
        return result
        
    
    def __generateHash(self, count=1):
        result = set()
        counter=0
        if count == 0:
            count = Tools.permutation(self.hashLength)
        #Read the previously touched hashes so that we do not repeat them...
        if self.campaign_name:
            self.__CHECKED_HASH = Tools.readHashList(self.hashpath)
        while (counter<=count):
            hashx = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(self.hashLength))
            if hashx not in self.__CHECKED_HASH:
                try:
                    result.add(hashx)
                    counter += 1
                except:
                    #Repeat hash created in the same batch move on...
                    pass
        return result
     
    def linkFetcher(self, count):
        results = []
        hashlist =  self.__generateHash(count=int(count))
        logging.info(hashlist)
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            threads=[]
            
            for urlhash in hashlist:
                threads.append(executor.submit(self.linkFetcherWorker,urlhash))
            
            for response in concurrent.futures.as_completed(threads):
                results.append(response.result())
                        
            threads = []
       
        return results

    
