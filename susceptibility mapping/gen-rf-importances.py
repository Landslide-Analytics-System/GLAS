import pickle
import matplotlib.pyplot as plt

with open("model-saves/RF-Binary-Classification.pkl", "rb") as f:
    model = pickle.load(f)

importances = model.feature_importances_
labels = ['humidity9', 'air9', 'ARI9', 'humidity8', 'air8', 'ARI8', 'humidity7', 'air7', 'ARI7', 'humidity6', 'air6', 'ARI6', 'humidity5', 'air5', 'ARI5', 'slope', 'forest', 'osm', 'lithology']

print(len(labels), len(importances))
print(importances)
print(labels)

plt.barh(labels, importances)
plt.title("RF Feature Importances")
plt.ylabel("Features")
plt.xlabel("Importances (normalized)")
plt.tight_layout()
plt.savefig("figures/rf-importances.png", bbox_inches='tight')