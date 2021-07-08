import matplotlib.pyplot as plt
import seaborn as sns

matrix = [[0.75, 0.04910714, 0.078125, 0.07366071, 0.04910714],
 [0.11034483, 0.36781609, 0.22298851, 0.16781609, 0.13103448],
 [0.14874142, 0.20366133, 0.31350114, 0.20823799, 0.12585812],
 [0.13987474, 0.19624217, 0.27139875, 0.25469729, 0.13778706],
 [0.12585812, 0.201373,   0.21052632, 0.27459954, 0.18764302]]

plt.clf()
sns.set(font_scale=1.5)
sns.heatmap(matrix, annot=True, cmap="magma_r", cbar=False, xticklabels=["no", 6, 7, 8, 9], yticklabels=["no", 6, 7, 8, 9])

plt.xlabel('Predicted Date')
plt.ylabel('True Date')
plt.tight_layout()
plt.title("RF Landslide Date Prediction")
# plt.show()
plt.savefig("RF-Landslide-Date-Prediction.png", bbox_inches = 'tight')