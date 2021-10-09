import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


matrix = [[1656, 21, 110, 0], [185, 136, 189, 1], [220, 83, 786, 2], [36, 7, 122, 5]]
matrix=np.array(matrix)
matrix = matrix / matrix.astype(np.float).sum(axis=1)
plt.clf()
plt.yticks(rotation=90, fontsize=15)
plt.xticks(fontsize=15)
sns.set(font_scale=2)
sns.heatmap(matrix, annot=True, cmap="Greens", cbar=False, xticklabels=["No", "Small", "Medium", "Large"], yticklabels=["No", "Small", "Medium", "Large"],)

plt.xlabel('Predicted Date', fontsize=20)
plt.ylabel('True Date', fontsize=20)
plt.tight_layout()
plt.title("RF Binary Prediction")
plt.savefig("RF-Binary-Slides.png", bbox_inches = 'tight')