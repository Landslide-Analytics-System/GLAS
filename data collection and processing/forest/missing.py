import pandas as pd

df = pd.read_csv("full_combined.csv")
finished = open("finished.txt", "r")
have = finished.read()
missing = ""

for idx, row in df.iterrows():
    tag = str(row.id) + ","+ str(row.lat) + "," + str(row.lon) + "..."
    if tag not in have:
        missing += tag[:-3] + "\n"

file = open("missing.txt", "w")
file.write(missing)
file.close()
print("Missing:", missing)