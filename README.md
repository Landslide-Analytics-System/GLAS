# GLAS: A Global Landslide Analytics System
## Ishaan Javali & Shrey Joshi

Landslides cost billions in damage annually in the U.S. & have affected 4.8 million people over the past 2 decades. 
GLAS is a landslide analytics system that offers a compiled dataset of global landslide incidences and features (GLIF), forecasting models, and a terrain-based susceptibility map.

This repository contains the dataset, forecasting models, and a testing tool along with some code used for collecting & processing the raw data.

Folders:
- **data collection and processing:** Contains code for collecting and processing features from their different sources.
- **dataset creation and testing tool:** Contains program for dataset creation given list of locations and times, and program for forecasting landslides. Setup required
- **forecasting models:** Contains code for training & evaluating forecasting models.
- **susceptibility mapping:** Contains code for generating susceptibility map.

------

# Dataset
[**GLIF_dataset.csv**](https://github.com/Landslide-Analytics-System/GLAS/blob/main/GLIF%20dataset.csv) contains the compiled data of 20,000+ landslide and non-landslide incidences, each with metadata and approximately 97 features.

The `type` column specifies the type of the instance. 
- `1`: (10,101 instances) means it is a landslide instance. 
- `2`: (5,007 instances) means it is a non-landslide instance from a random location and time
- `3`: (5,000 instances) means it is a non-landslide instance from the same location where a landslide has/will occur, but at a different time when no landslides occured within a 180-day time span and 20-mile radius.
A number `x` at the end of a column name implies how many days before the event the feature is for. Ex: The `ARI9` column is the ARI for the day 9 days before the events.

| Feature      | Description |
| ----------- | ----------- |
| ARI0 - ARI9      | <p>ARI for 0 to 9 days before the events. </p>       |
| precip0 - precip15      | <p>Precipitation in millimeters 0 to 15 days before the events. </p>       |
| temp0 - temp15      | <p>Temperature in Celsius 0 to 15 days before the events. </p>       |
| air15 - air15      | <p>Air Pressure in millibar 0 to 15 days before the events. </p>       |
| humidity15 - humidity15      | <p>Air Humidity level in percentage 0 to 15 days before the events. </p>       |
| wind0 - wind15      | <p>Wind Speed in kilometers/hour 0 to 15 days before the events. </p>       |
| forest   | Boolean variable for whether forest loss has occured within a year and 5-mile bounding box of the event.        |
| forest_year   | Number of years after 2000 since forest loss occurred (or 0 if no forest loss).         |
| slope   | Update         |
| osm   | Number of instances of human infrastructure tags within 1-mile bounding box.        |
| lithology   | Update         |
| landslide   | Boolean variable (0 or 1) for landslide or not         |

------
# Testing Tool

[This folder](https://github.com/Landslide-Analytics-System/GLAS/tree/main/dataset%20creation%20and%20testing%20tool) contains the code for the dataset creation and forecasting tools. 

- `collect.py`: Program for dataset creation
- `input.txt`: Input file for specifying latitude, longitude, time, and landslide/non-landslide (0/1) event to collect data for.
- `forecast.py`: Program for forecasting landslide occurences on the generated dataset.

On [this line](https://github.com/Landslide-Analytics-System/GLAS/blob/31c69216ce88262497e9a260616ee5fd7952677b/dataset%20creation%20and%20testing%20tool/collect.py#L16), for each of the events you wish to collect data for, you must specify which TIF files should be used (based on the latitude and longitude). This is for forest loss data collection
*['forest_scraper.py`](https://github.com/Landslide-Analytics-System/GLAS/tree/main/data%20collection%20and%20processing/scrapers) can be used for downloading all the TIF files.*

------

*This repository does not contain all the code used for this research or its evaluation. It contains the streamlined testing tool created by the authors as well as some of the programs the authors created for downloading, processing, extracting, and compiling data; training the models; and creating the susceptibility map.*
