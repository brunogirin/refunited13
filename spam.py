'''
Created on 19 Jan 2013

@author: bruno
'''

SEPARATORS=" \n\t\r.,;:'\"()"

class MessageTokenizer:
    def __init__(self):
        pass
    
    def tokenize_message(self, message):
        '''
        The message is a dict with item 'body' as the body of the message,
        any other item being meta-data
        '''
        m = {}
        for k, v in message:
            if v == 'body':
                self.tokenize_message_body(m, v)
            else:
                self.add_word(m, '{0}*{1}'.format(k, v))
        return m
    
    def add_word(self, m, word):
        self.add_word_count(m, word, 1)
    
    def add_word_count(self, m, word, count):
        if word in m:
            n = m[word]+count
        else:
            n = count
        m[word] = n
    
    def tokenize_message_body(self, m, body):
        s = 0
        i = 0
        while i < len(body):
            if body[i] in SEPARATORS:
                if i > s:
                    self.add_word(m, body[s:i])
                s = i + 1
            i = i + 1
        return m