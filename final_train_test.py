from modeling.data_processing import Dataset
from modeling.models import trainRF, trainKNN, trainSVC

# open 3 terminals and change this to GLIF_dataset.csv, 5000random.csv, and 5000same.csv and run them one on each terminal
glif = Dataset("GLIF_dataset.csv")

funcs = [trainRF, trainKNN, trainSVC]

print("----------Binary Classification----------")
X_train, X_test, X_val, y_train, y_test, y_val = glif.prepareBinaryData()

for func in funcs:
    func(X_train, X_test, X_val, y_train, y_test, y_val)

print("----------Severity Classification----------")
X_train, X_test, X_val, y_train, y_test, y_val = glif.prepareSeverityData()

for func in funcs:
    func(X_train, X_test, X_val, y_train, y_test, y_val)

print("----------Landslide Date Prediction----------")

X_train, X_test, X_val, y_train, y_test, y_val = glif.prepareTimeData()

for func in funcs:
    func(X_train, X_test, X_val, y_train, y_test, y_val)
