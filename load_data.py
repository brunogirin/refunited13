class Data:
    def __init__(self):
        self.all_msg = []
#        self.good_msg = []
#        self.bad_msg = []
        f = open("data/SMSSpamCollection", "r")
        for line in f.readlines():
#            if line.startswith('ham '):
#                msg = line[4:]
#                self.good_msg.append(msg)
#                self.all_msg.append(msg)
#                print msg
#            elif line.startswith('spam '):
#                msg = line[5:]
#                self.bad_msg.append(msg)
#                self.all_msg.append(msg)
#                print msg
#            else:
#                print "shouldn't be here: [{0}]".format(line)
            self.all_msg.append(line[5:])

        self.idx = 0

    def getNext(self):
        #print len(self.all_msg), self.idx
        if self.idx >= len(self.all_msg):
            return None
        else:
            m = self.all_msg[self.idx]
            self.idx = self.idx + 1
            return m