# GLAS: A Global Landslide Analytics System
## Ishaan Javali & Shrey Joshi

[**dataset_weatherstack.csv**](https://github.com/Landslide-Analytics-System/Landslide-Prediction/blob/main/dataset_weatherstack.csv) contains the compiled data of 20,000+ landslide and non-landslide incidences, each with over 100 features.

The `type` column specifies the type of the instance. 
- `1`: (10,101 instances) means it is a landslide instance. 
- `2`: (5,007 instances) means it is a non-landslide instance from a random location and time
- `3`: (5,000 instances) means it is a non-landslie instance from the same location where a landslide has/will occur, but at a different time when no landslides occured within a 90 day time span.

