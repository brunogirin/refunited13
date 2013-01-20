'''
Created on 19 Jan 2013

@author: bruno
'''
import math

SEPARATORS=" \n\t\r.,;:'\"()!?"

class MessageTokenizer:
    def __init__(self):
        pass
    
    def tokenize_message(self, message):
        '''
        The message is a dict with item 'body' as the body of the message,
        any other item being meta-data
        '''
        for k, v in message.iteritems():
            if k == 'body':
                for t in self.tokenize_message_body(v):
                    yield t
            else:
                yield '{0}*{1}'.format(k, v)
    
    def tokenize_message_body(self, body):
        s = 0
        i = 0
        while i < len(body):
            if body[i] in SEPARATORS:
                if i > s:
                    yield body[s:i]
                s = i + 1
            i = i + 1

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
    
    def add_message_tokens(self, tokens):
        for t in tokens:
            self.add_word(t)
    
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
        self.tok = MessageTokenizer()
    
    def add_bad_message_tokens(self, tokens):
        self.bad_corpus.add_message_tokens(tokens)
        self.num_bad_msg = self.num_bad_msg + 1
    
    def add_good_message_tokens(self, tokens):
        self.good_corpus.add_message_tokens(tokens)
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
            p = (float(nbad)/float(self.num_bad_msg)) / ((float(nbad)/float(self.num_bad_msg)) + (float(ngood)/float(self.num_good_msg)))
        return p
    
    def score_message_tokens(self, tokens):
        pmap = {}
        for t in tokens:
            pmap[t] = self.score_word(t)
        plist = [(k, v, math.fabs(v - 0.5)) for k, v in pmap.iteritems()]
        plist.sort(key=lambda x: x[2])
        plist.reverse()
        slist = plist[:10]
        pp = reduce(lambda x, y: x*y, [v[1] for v in slist])
        np = reduce(lambda x, y: x*(1-y), [v[1] for v in slist])
        if (pp+np == 0):
            s = 0.5
        else:
            s = pp/(pp+np)
        return (s, plist)
    
    def tokenize_message(self, msg):
        return self.tok.tokenize_message({ 'body': msg })
    
    def flag_as_good(self, msg):
        self.add_good_message_tokens([t for t in self.tokenize_message(msg)])
        
    def flag_as_bad(self, msg):
        self.add_bad_message_tokens([t for t in self.tokenize_message(msg)])
        
    def score(self, msg):
        s = self.score_message_tokens(self.tokenize_message(msg))
        if (s[0] > 0.9):
            m = 'Bad'
        elif (s[0] < 0.1):
            m = 'Good'
        else:
            m = 'Neutral'
        return (s[0], m, s[1])
        