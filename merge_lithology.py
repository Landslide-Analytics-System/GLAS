import os
import pandas as pd
from geojsplit import geojsplit
from tqdm import tqdm
import sys
import numpy as np
import matplotlib.path as mpltPath

geojson = geojsplit.GeoJSONBatchStreamer("data/lithology/lithology-json.geojson")

csv_path = os.path.join("data", "dataset.csv")
df = pd.read_csv(csv_path, low_memory=False)

batch_size=1000

latlon_points = np.array(list(zip(list(df['lat']), list(df['lon']))))

min_areas = np.zeros(latlon_points.shape[0])
min_areas.fill(-1)

classnames = ["" for i in range(len(latlon_points))]


continue_iter = 0
# continue_iter = 585


for index, feature_collection in tqdm(enumerate(geojson.stream(batch=batch_size)), total=1235400/batch_size):
    
    if index<continue_iter:
        continue

    for feature_path in tqdm(feature_collection['features'], leave=False):
        properties = feature_path['properties']
        shapearea = int(properties['Shape_Area'])
        classname = properties['xx']

        path = mpltPath.Path(feature_path['geometry']['coordinates'][0][0])

        # pass in a 2d np array of point pairs.
        inside = path.contains_points(latlon_points)

        # from the inside array, if val=true add to classname array
        # if val=true second time and shapearea smaller then update it. else leave it
        for idx, val in enumerate(inside):
            if val:
                if min_areas[idx]==-1 or (min_areas[idx]>0 and shapearea<min_areas[idx]):
                    min_areas[idx] = shapearea
                    classnames[idx] = classname

    df['lithology'] = classnames
    df.to_csv("dataset_with_lithology.csv")