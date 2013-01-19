'''
Created on 19 Jan 2013

@author: bruno
'''
import math

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
    
    def add_corpus(self, corpus):
        for k, v in corpus.data.iteritems():
            self.add_word_count(k, v)
    
    def add_message_corpus(self, mcorpus):
        for k in mcorpus.data.iterkeys():
            self.add_word(k)
    
    def get_word_count(self, word):
        if word in self.data:
            return self.data[word]
        else:
            return 0

class SpamProcessor:
    def __init__(self):
        self.good_corpus = Corpus()
        self.bad_corpus = Corpus()
        self.num_good_msg = 0
        self.num_bad_msg = 0
    
    def add_bad_message_corpus(self, mcorpus):
        self.bad_corpus.add_message_corpus(mcorpus)
        self.num_bad_msg = self.num_bad_msg + 1
    
    def add_good_message_corpus(self, mcorpus):
        self.good_corpus.add_message_corpus(mcorpus)
        self.num_good_msg = self.num_good_msg + 1
    
    def score_word(self, word):
        ngood = self.good_corpus.get_word_count(word)
        nbad = self.bad_corpus.get_word_count(word)
        if (ngood == 0 and nbad == 0) or (self.num_good_msg == 0 and self.num_bad_msg == 0):
            p = 0.5
        elif ngood == 0 or self.num_good_msg == 0:
            p = 0.99
        elif nbad == 0 or self.num_bad_msg == 0:
            p = 0.1
        else:
            p = (nbad/self.num_bad_msg) / (nbad/self.num_bad_msg) + (ngood/self.num_good_msg)
        return p
    
    def score_message_corpus(self, mcorpus):
        pmap = {}
        for k in mcorpus.data.iterkeys():
            pmap[k] = self.score_word(k)
        plist = [(k, v, math.fabs(v - 0.5)) for k, v in pmap.iteritems()]
        plist.sort(key=lambda x: x[2])
        plist.reverse()
        slist = plist[:10]
        pp = reduce(lambda x, y: x*y, slist)
        np = reduce(lambda x, y: x*(1-y), slist)
        s = pp/(pp+np)
        return s
        