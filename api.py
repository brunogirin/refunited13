'''
Created on 19 Jan 2013

@author: bruno
'''
import requests
from requests.auth import HTTPDigestAuth

API_USER_NAME = 'hackathon'
API_PASSWORD = file.readlines(open("password"))
API_CORE_URL = 'http://api.ru.istykker.dk/'

class ApiServer:
    def __init__(self):
        self.auth = HTTPDigestAuth(API_USER_NAME, API_PASSWORD)
    
    def create_headers(self, params={}):
        param_string = self.create_param_string(params)
        headers = {
                   'Content-Type': 'application/json',
                   'Content-Length': str(len(param_string))
                   }
        return headers
        
    def create_param_string(self, params={}):
        return '&'.join(
                       [k + '=' + v for k, v in params.iteritems()]
                       )
        
    def get(self, url, params={}, raw = False):
        return requests.get(API_CORE_URL + url,
                            auth=self.auth,
                            headers=self.create_headers({}),
                            params=params
                            )
    
    def post(self, url, params={}, raw=False):
        pass
    
    def put(self, url, params={}, raw=False):
        pass
    
    def delete(self, url, params=[], raw=False):
        pass