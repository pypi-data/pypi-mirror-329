import numpy as np

from sklearn.preprocessing import MinMaxScaler
from radnn.data.preprocess import Normalizer
from radnn import FileSystem

oFileSys = FileSystem("MLConfig", "MLModels", "MLData")
oDataFS = oFileSys.datasets.subfs("NORMALIZER")
np.random.seed(2023)

original_data = np.random.rand(100, 5)

print(original_data.shape)

# data = data.astype(np.float64)  # Same with sklearn
original_data = original_data.astype(np.float32)  # sklearn is loosing precision at the 6th digit

oScaler1 = MinMaxScaler()
data1 = oScaler1.fit_transform(original_data)
data1_inv = oScaler1.inverse_transform(data1)
print(f"scaler min/max shape:{oScaler1.data_min_.shape}")
print(np.sum(original_data), np.sum(data1_inv))


oScaler2 = Normalizer(name="Normalizer", filestore=oDataFS)
data2 = oScaler2.fit_transform(original_data)
data2_inv = oScaler2.inverse_transform(data2)



print(data1.dtype, data2.dtype)
print("Inversing: sklearn  :%.8f" % np.sum(original_data), " inv: %.8f" % np.sum(data1_inv))
print("Inversing: radnn    :%.8f" % np.sum(original_data), " inv: %.8f" % np.sum(data2_inv))
print("Sum      : sklearn  :%.8f" % np.sum(data1), "radnn:%.8f" % np.sum(data2))
print("Rounding differences in min")
print(oScaler1.data_min_ - oScaler2.min)
print("Rounding differences in std")
print(oScaler1.data_max_ - oScaler2.max)

assert np.sum(oScaler1.data_min_ - oScaler2.min) == 0, "Differences in min"
assert np.sum(oScaler1.data_max_ - oScaler2.max) == 0, "Differences in max"




