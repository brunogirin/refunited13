'''
Created on 19 Jan 2013

@author: bruno
'''
from api import ApiServer
import json

class MessageHandler:
    def __init__(self):
        self.api = ApiServer()
        
    def read_messages(self, profile_id):
        r = self.api.get('profile/{0}/messages'.format(profile_id))
        return json.loads(r.text)
    
    def read_message_thread(self, profile_id, profile_id2):
        r = self.api.get('profile/{0}/messages/{1}.'.format(profile_id, profile_id2))
        return json.loads(r.text)
    
    def send_message(self, profile_id, profile_id2, message):
        p = {
             'messageBody': message
             }
        r = self.api.post(
                          'profile/{0}/messages/{1}.'.format(profile_id, profile_id2),
                          params=p
                          )
        return json.loads(r.text)
    