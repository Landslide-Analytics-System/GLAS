import pandas as pd

df = pd.read_csv("./data/landslide_catalog/with_weather_no_slope.csv")
slopes = pd.read_csv("./data/landslide_catalog/landslides_with_slope.csv")
slopes.rename(columns={"FID": "OBJECTID"}, inplace=True)
slopes = slopes[['OBJECTID', 'slope']]

merged = df.merge(slopes)

# this dataset has weather data up to 35 days before landslides in southeast asia after 2008
# geographical area: (-10 S --> 40 N and 60 E to 150 E)
merged.to_csv("./data/landslide_catalog/full_dataset_v1.csv")