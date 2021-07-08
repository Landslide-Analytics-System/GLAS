from modeling.figures import plotROCAllModels
from modeling.data_processing import Dataset
from modeling.models import trainRF, trainKNN, trainSVC
import json

# open 3 terminals and change this to GLIF_dataset.csv, 5000random.csv, and 5000same.csv and run them one on each terminal
glif = Dataset("GLIF_dataset.csv")
results = dict()
funcs = [trainRF, trainKNN, trainSVC]
names = ["rf", "knn", "svc"]

print("----------Binary Classification----------")
X_train, X_test, X_val, y_train, y_test, y_val = glif.prepareBinaryData()
temp = {}
for idx, func in enumerate(funcs):
    temp[names[idx]] = func(X_train, X_test, X_val, y_train, y_test, y_val, "Binary Classification")
results["binary"] = temp

with open('final_results.json', 'w+') as fp:
    json.dump(results, fp)


print("----------Severity Classification----------")
X_train, X_test, X_val, y_train, y_test, y_val = glif.prepareSeverityData()
temp = {}
for idx, func in enumerate(funcs):
    temp[names[idx]] = func(X_train, X_test, X_val, y_train, y_test, y_val ,"Severity Classification")
results["severity"] = temp
with open('final_results.json', 'w+') as fp:
    json.dump(results, fp)

print("----------Landslide Date Prediction----------")
X_train, X_test, X_val, y_train, y_test, y_val = glif.prepareTimeData()
temp = {}
for idx, func in enumerate(funcs):
    temp[names[idx]] = func(X_train, X_test, X_val, y_train, y_test, y_val, "Landslide Date Prediction")
results["date"] = temp

with open('final_results.json', 'w+') as fp:
    json.dump(results, fp)


plotROCAllModels(results["binary"])