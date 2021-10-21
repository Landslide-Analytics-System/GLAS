import matplotlib.pyplot as plt
import json
from sklearn.metrics import auc

text = open("final_results.json", "r").read()

results = json.loads(text)

lstmtpr = eval(open("tpr.txt", "r").read())
lstmfpr = eval(open("fpr.txt", "r").read())

print(auc(lstmtpr, lstmtpr))

print(results['binary']['rf']['auc'])
print(results['binary']['knn']['auc'])
print(results['binary']['svc']['auc'])

def saveROCAllModels(results):
    plt.clf()
    plt.plot([0,1],[0,1], 'k--')
    plt.plot(results["rf"]["fpr"], results["rf"]["tpr"], label= "Random Forest (AUC: 0.938)")
    plt.plot(results["knn"]["fpr"], results["knn"]["tpr"], label= "K-Nearest Neighbors (AUC: 0.806)")
    plt.plot(results["svc"]["fpr"], results["svc"]["tpr"], label= "Support Vector Machine with RBF (AUC: 0.826)")
    plt.plot(lstmfpr, lstmtpr, label= "LSTM Neural Network (AUC: 0.747)")
    
    plt.legend()
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.show()
    # plt.savefig("figures/ROC_Curve_Binary.png", bbox_inches="tight")

saveROCAllModels(results['binary'])