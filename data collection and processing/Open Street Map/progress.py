import pandas as pd
import datetime
df = pd.read_csv("dataset.csv")

l = len(df)
f1 = open("finished.txt", "r")
f2 = open("rfinished.txt", "r")
print(datetime.datetime.now().time())

s = int(f1.read())
s2 = int(f2.read())
print(s, l - s2)
percent = float(s + (l-s2))
percent /= float(l)
percent = round(percent * 10000)/100
print(percent, "%")
