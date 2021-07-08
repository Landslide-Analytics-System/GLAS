import matplotlib.pyplot as plt
import seaborn as sns

def saveConfusionMatrix(filename, title, matrix):
    plt.clf()
    sns.set(font_scale=1.5)
    sns.heatmap(matrix, annot=True, cmap="magma_r")
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.tight_layout()
    plt.title(title)
    plt.savefig("figures/"+filename, bbox_inches = 'tight')

def saveROCAllModels(results):
    plt.clf()
    plt.plot([0,1],[0,1], 'k--')
    plt.plot(results["rf"]["fpr"], results["rf"]["tpr"], label= "Random Forest")
    plt.plot(results["knn"]["fpr"], results["knn"]["tpr"], label= "K-Nearest Neighbors")
    plt.plot(results["svc"]["fpr"], results["svc"]["tpr"], label= "Support Vector Machine (RBF)")
    plt.legend()
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.savefig("figures/ROC_Curve_Binary.png", bbox_inches="tight")
