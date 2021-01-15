from TifHandler import TifHandler
import pandas as pd
import os
import gc

for filename in os.listdir("TIF Files"):
    if not filename.endswith(".tif"): 
        continue
    print("\x1b[1;37;40m", filename)
    
    tif_name = filename
    th = TifHandler(tif_name)
    # th.thumbnail()
    df = pd.read_csv("full_combined.csv")
    finished = open("finished.txt", "r")
    have = finished.read()
    print("\x1b[1;33;40m")

    for idx, row in df.iterrows():
        tag = str(row.id) + "..."
        if tag in have or not th.inBounds(row.lat, row.lon):
            continue
        print(idx, ": ", row.id, " | ", row.lat, row.lon, "in", row.date)
        
        year = 2000 + int(row.date[-2:])
        lat, lon = row.lat, row.lon
        results = th.forestLoss(year, lat, lon)
        print(results[0], results[1])
        
        writer = open("forest.txt", "a")
        writer.write(str(row.id) + "," + str(results[0]) + "," + str(results[1]) + ","+ str(row.id) + ";;;\n")
        writer.close()

        f2 = open("finished.txt", "a")
        f2.write(tag + "\n")
        f2.close()

    del th
    gc.collect()
    print("\x1b[7;37;41m -------------------------------------------------")

