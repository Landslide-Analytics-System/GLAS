from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

def trainRF(X_train, X_test, X_val, y_train, y_test, y_val):
    best = 0
    highest = 0
    print("Training Random Forest...")
    for i in tqdm(range(85, 150, 2), leave=False):
        model = RandomForestClassifier(n_estimators = i)
        model.fit(X_train, y_train)
        pred = model.predict(X_val)
        score = round(accuracy_score(pred, y_val)*10000)/100
        if score > highest:
            highest = score
            best = i
            # tqdm.write(str(score))

    model = RandomForestClassifier(n_estimators = best)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    score = accuracy_score(pred, y_test)*100
    print(f"RF: {best} trees yields {score}%")
    array = confusion_matrix(y_test, pred)
    print(array)

def trainKNN(X_train, X_test, X_val, y_train, y_test, y_val):
    best = 0
    highest = 0
    print("Training KNN...")
    for i in tqdm(range(1, 130), leave=False):
        model = KNeighborsClassifier(n_neighbors = i)
        model.fit(X_train, y_train)
        pred = model.predict(X_val)
        score = round(accuracy_score(pred, y_val)*10000)/100
        if score > highest:
            highest = score
            best = i
            # tqdm.write(str(score))

    model = KNeighborsClassifier(n_neighbors = best)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    score = accuracy_score(pred, y_test)*100
    print(f"KNN: {best} neighbors yields yields {score}%")
    array = confusion_matrix(y_test, pred)
    print(array)

def trainSVC(X_train, X_test, X_val, y_train, y_test, y_val):
    best_c = 0
    best_gamma = 0
    highest = 0
    print("Training SVC...")
    C_range =[1, 10, 100]
    gamma_range = [0.1, 1, 10, 100]
    for c in C_range:
        for g in gamma_range:
            svc2 = SVC(kernel='rbf', gamma=g, C=c)
            svc2.fit(X_train, y_train)
            score = accuracy_score(y_val, svc2.predict(X_val))
            if score > highest:
                best_c = c
                best_gamma = g
                highest = score

    model = SVC(kernel='rbf', gamma=best_gamma, C=best_c)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    score = accuracy_score(pred, y_test)*100
    print(f"SVC: C: {best_c} and Gamma: {best_gamma} yields {score}%")
    array = confusion_matrix(y_test, pred)
    print(array)