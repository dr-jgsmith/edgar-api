# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 22:26:32 2017

@author: justi

SEC Search
"""
import requests
import lxml
from bs4 import BeautifulSoup



class Edgar:
    
    def __init__(self, name=None, tid=None):
        self.name = name
        self.tid = tid
        self.payload = {"company": self.name}
        self.edgar_url = "https://www.sec.gov/cgi-bin/browse-edgar"
        
        self.s = requests.Session()
        self.s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
   
        
    def lookup(self):
        r = self.s.post(self.edgar_url, data=self.payload)
        self.response = r.content
                
        return self.response
    
    
    def parse_lookup(self):
        soup = BeautifulSoup(self.response, "lxml")
        for tag in soup.find_all("a"):
            x = tag.get('id')
            
            if x == 'documentsbutton':
                self.data = tag.get("href")
                
                break
            else:
                pass
        
        return self.data
    
    
    def get_taxid(self):
        sec = "https://www.sec.gov"
        doc = self.data
        url = sec + doc
        self.id_page = self.s.get(url).content
        
        soup = BeautifulSoup(self.id_page, "lxml")
        
        for tag in soup.find_all('p', 'identInfo'):
            self.taxid = tag.find('strong')
            print(self.taxid.contents[0])
               
        
        return self.taxid.contents[0]
        

       
x = Edgar('chipotle')
x.lookup()
x.parse_lookup()
x.get_taxid()
