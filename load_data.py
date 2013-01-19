import pandas as pd

f = open("data/SMSSpamCollection", "r")

for line in f.readlines():


data = pd.read_table("data/SMSSpamCollection")

