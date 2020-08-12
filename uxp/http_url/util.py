'''
Created on Sep 13, 2019

@author: 5hu5ky
'''

from bs4 import BeautifulSoup
from urllib import parse as urlparse
from builtins import staticmethod
import re

class HTMLUtil:

    @staticmethod
    def getFileFromURL(url):
        parsedURL = urlparse.urlparse(url)
        domain ='{uri.netloc}'.format(uri=parsedURL)
        result = url[url.rfind("/")+1:].strip().replace('?','_').replace('&','-')
        if result == "":
            result = "{}_index".format(domain)
        return result 
    
    @staticmethod
    def getLink(html_doc):
        searchMagic= {"id": "clickthrough"}
        soup = BeautifulSoup(html_doc, 'html.parser')
        result = soup.find('a', searchMagic)
        if result:
            return result.text
        return result 
    
    
    @staticmethod
    def isBitlyWarningPage(html_doc):
        result = False
        try:
            #print(html_doc)
            soup = BeautifulSoup(html_doc, 'html.parser')
            title = soup.find('title')

            if title:
                if title.string.lower() == "Warning! | There might be a problem with the requested link".lower():
                    result = True
        except Exception as ex:
            print (ex)
        return result
    
    
    @staticmethod
    def pageContainsString(html_doc, search_string=[]):
        '''
        Simple search method that searches html content
        
        :returns number of keywords matched...
        '''
        result = 0
        try:
            for s in search_string:
                soup = BeautifulSoup(html_doc, 'html.parser')
                if soup.body:
                    results = soup.body.findAll(text=re.compile(r'{}'.format(s), re.IGNORECASE))
                    if results:
                        result += 1    
        except Exception as ex:
            print (ex)
            
        return result