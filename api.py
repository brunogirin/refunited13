'''
Created on 19 Jan 2013

@author: bruno
'''
import requests
from requests.auth import HTTPDigestAuth
import json

API_USER_NAME = 'hackathon'
API_PASSWORD = file.readline(open("password")).rstrip()
API_CORE_URL = 'http://api.ru.istykker.dk/'

class ApiServer:
    def __init__(self):
        self.auth = HTTPDigestAuth(API_USER_NAME, API_PASSWORD)
    
    def create_headers(self, params=''):
        headers = {
                   'Content-Type': 'application/json',
                   'Content-Length': str(len(params))
                   }
        return headers
        
    def get(self, url, params={}, raw = False):
        #headers=self.create_headers('')
        #print 'Headers: {0}'.format(headers)
        return requests.get(API_CORE_URL + url,
                            auth=self.auth,
                            headers=self.create_headers('')#,
                            #params=params
                            )
    
    def post(self, url, params={}, raw=False):
        params_str = json.dumps(params)
        return requests.post(API_CORE_URL + url,
                            auth=self.auth,
                            headers=self.create_headers(params_str),
                            data=params_str
                            )
    
    def put(self, url, params={}, raw=False):
        pass
    
    def delete(self, url, params=[], raw=False):
        pass
