class Data:
    def __init__(self):
        self.all_msg = []
        self.good_msg = []
        self.bad_msg = []
        self.neutral_msg = []
        f = open("data/SMSSpamCollection", "r")
        for line in f.readlines():
            if line.startswith('ham'):
                tag = line[:3]
                msg = line[4:]
                self.good_msg.append(msg)
            elif line.startswith('spam'):
                tag = line[:4]
                msg = line[5:]
                self.bad_msg.append(msg)
            else:
                tag = ''
                msg = line
                self.neutral_msg.append(msg)
            self.all_msg.append((msg, tag))

        self.idx = 0

    def getNext(self):
        if self.idx >= len(self.all_msg):
            return None
        else:
            m = self.all_msg[self.idx][0]
            self.idx = self.idx + 1
            return m