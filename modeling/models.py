from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score, roc_curve, roc_auc_score, plot_roc_curve
from .figures import saveConfusionMatrix
from sklearn.decomposition import PCA
import pickle
import numpy as np

def getMetrics(model, name, task, y_test, pred, probas, best=None, best_c=None, best_gamma=None):
    accuracy = accuracy_score(y_test, pred)
    precision = precision_score(y_test, pred, average='macro')
    recall = recall_score(y_test, pred, average='macro')
    
    if task=="Binary Classification":
        auc = roc_auc_score(y_test, probas)
        fpr, tpr, thresholds = roc_curve(y_test, probas)
    else:
        auc, fpr, tpr, thresholds = None, np.array([]), np.array([]), np.array([])

    f1 = f1_score(y_test, pred, average="micro" if task !="Binary Classification" else "binary")
    array = confusion_matrix(y_test, pred, normalize='true')

    if name == "RF":
        print(f"RF: {best} trees: accuracy, {accuracy}%, precision: {precision}, recall: {recall}, auc: {auc}")
    elif name == "KNN":
        print(f"KNN: {best} neighbors: accuracy, {accuracy}%, precision: {precision}, recall: {recall}, auc: {auc}")
    else:
        print(f"SVC: c: {best_c}, gamma: {best_gamma}, accuracy: {accuracy}%, precision: {precision}, recall: {recall}, auc: {auc}")


    title = f"{name} {task}"
    filename = f"{name}-{task.replace(' ', '-')}.png"
    saveConfusionMatrix(filename, title, array)

    with open(f"model-saves/{name}-{task.replace(' ', '-')}.pkl", "wb") as f:
        pickle.dump(model, f)


    results = {"fpr": fpr.tolist(), "tpr": tpr.tolist(), "thresholds": thresholds.tolist(), "accuracy": accuracy, "precision": precision, "recall": recall, "auc": auc, "f1": f1}
    return results

def trainRF(X_train, X_test, X_val, y_train, y_test, y_val, task):
    best = 0
    highest = 0
    print("Training Random Forest...")
    for i in tqdm(range(90, 130, 2), leave=False):
        model = RandomForestClassifier(n_estimators = i)
        model.fit(X_train, y_train)
        pred = model.predict(X_val)
        score = round(accuracy_score(pred, y_val)*10000)/100
        if score > highest:
            highest = score
            best = i

    model = RandomForestClassifier(n_estimators = best)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    probas = model.predict_proba(X_test)[:,1]

    return getMetrics(model, "RF", task, y_test, pred, probas, best=best)

def trainKNN(X_train, X_test, X_val, y_train, y_test, y_val, task):
    best = 0
    highest = 0
    print("Training KNN...")
    for i in tqdm(range(1, 30, 2), leave=False):
        model = KNeighborsClassifier(n_neighbors = i)
        model.fit(X_train, y_train)
        pred = model.predict(X_val)
        score = round(accuracy_score(pred, y_val)*10000)/100
        if score > highest:
            highest = score
            best = i

    model = KNeighborsClassifier(n_neighbors = best)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    probas = model.predict_proba(X_test)[:,1]

    return getMetrics(model, "KNN", task, y_test, pred, probas, best=best)

def trainSVC(X_train, X_test, X_val, y_train, y_test, y_val, task):
    pca = PCA(0.9)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)
    X_val = pca.transform(X_val)

    best_c = 0
    best_gamma = 0
    highest = 0
    print("Training SVC...")
    C_range =[1, 10, 100]
    gamma_range = [0.1, 1, 10, 100]
    for c in tqdm(C_range, leave=False):
        for g in gamma_range:
            svc2 = SVC(kernel='rbf', gamma=g, C=c, probability=True)
            svc2.fit(X_train, y_train)
            score = accuracy_score(y_val, svc2.predict(X_val))
            if score > highest:
                best_c = c
                best_gamma = g
                highest = score

    model = SVC(kernel='rbf', gamma=best_gamma, C=best_c , probability=True)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    probas = model.predict_proba(X_test)[:,1]

    return getMetrics(model, "SVC", task, y_test, pred, probas, best_gamma=best_gamma, best_c=best_c)