import numpy as np

from sklearn.preprocessing import StandardScaler
from radnn.data.preprocess import Standardizer
from radnn import FileSystem

oFileSys = FileSystem("MLConfig", "MLModels", "MLData")
oDataFS = oFileSys.datasets.subfs("STANDARDIZER")
np.random.seed(2023)

original_data = np.random.rand(100, 5)

print(original_data.shape)

# data = data.astype(np.float64)  # Same with sklearn
original_data = original_data.astype(np.float32)  # sklearn is loosing precision at the 6th digit

oScaler1 = StandardScaler()
data1 = oScaler1.fit_transform(original_data)
data1_inv = oScaler1.inverse_transform(data1)
print(f"scaler mean/std shape:{oScaler1.mean_.shape}")
print(np.sum(original_data), np.sum(data1_inv))


oScaler2 = Standardizer(name="Standardizer", filestore=oDataFS)
data2 = oScaler2.fit_transform(original_data)
data2_inv = oScaler2.inverse_transform(data2)



print(data1.dtype, data2.dtype)
print("Inversing: sklearn  :%.8f" % np.sum(original_data), " inv: %.8f" % np.sum(data1_inv))
print("Inversing: radnn    :%.8f" % np.sum(original_data), " inv: %.8f" % np.sum(data2_inv))
print("Sum      : sklearn  :%.8f" % np.sum(data1), "radnn:%.8f" % np.sum(data2), f" difference: {np.sum(data1) - np.sum(data2):.8f}")
print()



print("Rounding differences in mean")
print(oScaler1.mean_ - oScaler2.mean)
print("Rounding differences in std")
print(oScaler1.scale_ - oScaler2.std)

assert np.sum(oScaler1.mean_ - oScaler2.mean) == 0, "Differences in means"
assert np.sum(oScaler1.scale_ - oScaler2.std) == 0, "Differences in stds"

