import matplotlib.pyplot as plt
import json
from sklearn.metrics import auc

text = open("final_results.json", "r").read()

results = json.loads(text)

lstmtpr = eval(open("tpr.txt", "r").read())
lstmfpr = eval(open("fpr.txt", "r").read())

lstm_score = str(auc(lstmfpr, lstmtpr))[:5]

rf_score = str(results['binary']['rf']['auc'])[:5]
knn_score = str(results['binary']['knn']['auc'])[:5]
svc_score = str(results['binary']['svc']['auc'])[:5]

def saveROCAllModels(results):
    plt.clf()
    plt.plot([0,1],[0,1], 'k--')
    plt.plot(results["rf"]["fpr"], results["rf"]["tpr"], label= "Random Forest (AUC: "+rf_score+")")
    plt.plot(results["knn"]["fpr"], results["knn"]["tpr"], label= "K-Nearest Neighbors (AUC: "+knn_score+")")
    plt.plot(results["svc"]["fpr"], results["svc"]["tpr"], label= "Support Vector Machine with RBF (AUC: "+svc_score+")")
    plt.plot(lstmfpr, lstmtpr, label= "LSTM Neural Network (AUC: "+lstm_score+")")
    
    plt.legend()
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.show()
    # plt.savefig("figures/ROC_Curve_Binary.png", bbox_inches="tight")

saveROCAllModels(results['binary'])