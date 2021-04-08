import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("file.csv")
X = df.copy()
y = X.landslide
columns = []
for i in range(9, 4, -1):
    columns.append('humidity' + str(i))
    columns.append('ARI' + str(i))
columns.append('slope')
columns.append('forest2')
columns.append('realosm')
X = X[columns]

scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

filename = 'model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X, y)
pred = loaded_model.predict(X)
print("Accuracy: ", result)
print("=============")
print("Actual:  ", y)
print("Predicted:", pred)