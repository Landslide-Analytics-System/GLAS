import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


matrix = [[311, 29, 33, 35, 57], [40, 172, 88, 63, 75], [48, 107, 118, 80, 88], [56, 112, 91, 83, 105], [70, 89, 77, 82, 127]]
matrix=np.array(matrix)
matrix = matrix / matrix.astype(np.float).sum(axis=1)
plt.clf()
sns.set(font_scale=1.5)
sns.heatmap(matrix, annot=True, cmap="magma_r", cbar=False, xticklabels=["no", 6, 7, 8, 9], yticklabels=["no", 6, 7, 8, 9])

plt.xlabel('Predicted Date')
plt.ylabel('True Date')
plt.tight_layout()
plt.title("RF Landslide Date Prediction")
plt.savefig("RF-Landslide-Date-Prediction.png", bbox_inches = 'tight')