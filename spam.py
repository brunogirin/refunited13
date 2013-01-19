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
        c = Corpus()
        for k, v in message.iteritems():
            if k == 'body':
                self.tokenize_message_body(c, v)
            else:
                c.add_word('{0}*{1}'.format(k, v))
        return c
    
    def tokenize_message_body(self, c, body):
        s = 0
        i = 0
        while i < len(body):
            if body[i] in SEPARATORS:
                if i > s:
                    c.add_word(body[s:i])
                s = i + 1
            i = i + 1
        return c

class Corpus:
    def __init__(self):
        self.data = {}
        
    def add_word(self, word):
        self.add_word_count(word, 1)
    
    def add_word_count(self, word, count):
        if word in self.data:
            n = self.data[word]+count
        else:
            n = count
        self.data[word] = n
    
        