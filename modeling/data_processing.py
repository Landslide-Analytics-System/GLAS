import random
import pandas as pd
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from collections import Counter

def scale_split(X, y):
    # 70/20/10 train/test/val split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size = 0.125) # 0.125 * 0.8 = 0.1

    # print(X_train.head())

    if type(X_train).__name__=="list":
        num = len(list(X_train)[0])
    else:
        num = len(X_train.columns)

    categorical = [num-1]
    numerical = [i for i in range(num-1)]

    scaler = ColumnTransformer([
        ('num', StandardScaler(), numerical),
        ('cat', OrdinalEncoder(), categorical)
    ])

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    X_val = scaler.transform(X_val)

    return X_train, X_test, X_val, y_train, y_test, y_val

class Dataset:
    def __init__(self, filename):
        self.df = pd.read_csv(filename, low_memory=False)
        self.df = self.df.query("(landslide == 0) | (landslide == 1 & (severity == 'small' | severity == 'medium' | severity == 'large'))")
        self.num_landslides = self.df.landslide.value_counts()[1]

        print("Loading data...")
        count = 0
        to_drop = []
        for idx, row in tqdm(self.df.iterrows(), total=len(self.df), leave=False):
            if row.landslide==0 and count <= self.num_landslides:
                count+=1

            if row.landslide==0 and count > self.num_landslides:
                to_drop.append(idx)
        self.df.drop(to_drop, inplace=True)

        self.df = shuffle(self.df)
        self.df.reset_index(inplace=True, drop=True)
        

    def prepareBinaryData(self):
        X = self.df.copy()
        y = X.landslide
        columns = []
        for i in range(9, 4, -1):
            columns.append('humidity' + str(i))
            columns.append('air' + str(i))
            columns.append('ARI' + str(i))
        columns.append('slope')
        columns.append('forest')
        columns.append('osm')
        columns.append('lithology')
        X = X[columns]

        return scale_split(X, y)
    
    def prepareSeverityData(self):
        X = self.df.copy()
        y = []
        types = set()
        for idx, row in X.iterrows():
            if row.landslide == 0:
                y.append(0)
            elif row.severity == 'small':
                y.append(1)
            elif row.severity == 'medium':
                y.append(2)
            else:
                y.append(3)
            types.add(y[-1])
        # print(types)
        columns=[]
        for i in range(9, 4, -1):
            columns.append('humidity' + str(i))
            columns.append('ARI' + str(i))
            columns.append('air' + str(i))
        columns.append('slope')
        columns.append('forest')
        columns.append('osm')
        columns.append('lithology')
        X = X[columns]

        return scale_split(X, y)
    
    def prepareTimeData(self):
        X = []
        y = []
        days = dict()
        for idx, row in self.df.iterrows():
            lastday = random.randint(6, 9)
            if row.landslide == 1:
                y.append(lastday-4)
            else:
                if Counter(y)[-1] < 2284:
                    y.append(-1)
                else:
                    continue
            temp=[]
            if lastday in days:
                days[lastday] +=1
            else:
                days[lastday] = 0
            for i in range(6):
                temp.append(row['humidity' + str(lastday-i)])
                temp.append(row['ARI' + str(lastday-i)])
                temp.append(row['wind' + str(lastday-i)])
            temp.append(row['slope'])
            year = int(str(row.date)[-2:])
            temp.append(row['forest'])
        #     temp.append(1 if year - row.forest_year <= 4 else 0)
            temp.append(row['osm'])
            temp.append(row['lithology'])

            X.append(temp)
            # if idx == 0:
            #     print(year, row.forest_year)

        print(Counter(y)[-1])
        return scale_split(X, y)

if __name__ == '__main__':
    glif = Dataset("GLIF_Dataset.csv")
    # glif.prepareBinaryData()
    # glif.prepareSeverityData()
    glif.prepareTimeData()