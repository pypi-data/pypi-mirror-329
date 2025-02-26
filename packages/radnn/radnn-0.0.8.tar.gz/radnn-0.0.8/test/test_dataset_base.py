import numpy as np
from radnn.data import DataSetBase
from radnn import mlsys
import os
from radnn import FileStore, FileSystem

mlsys.random_seed_all(2023)

oFileSys = FileSystem("MLConfig", model_folder="MLModels", dataset_folder="MLData")

#os.chdir("..\..")
oDatasetsMainFS = FileStore("MLData")
oFS = oDatasetsMainFS.subfs("DUMMY")

# nData = np.random.rand(100).astype(np.float32)
nData = np.arange(0, 100)
nData = nData / (nData + 1)
print(nData.shape)
nLabels = np.concatenate([np.zeros(50), np.ones(50)], axis=0).astype(np.int32)
print(nLabels.shape)

oDataset = DataSetBase("dummy", fs=oFileSys)
oDataset.for_classification(3, {"negative", "neutral", "positive"}).assign((nData, nLabels)).split(0.8).save_cache()
oDataset.print_info()

nTSChecksum = np.sum(oDataset.ts_samples)
nVSChecksum = np.sum(oDataset.vs_samples)
print(nTSChecksum, nVSChecksum)

# // Unit Testing \\
assert nTSChecksum == 75.59110064555725
assert nVSChecksum == 19.22152183680314

# Seed None:                 75.45033306926038 19.362289413100005
# Seed None: Parameter 2023: 75.59110064555725 19.22152183680314
# Seed 2023: Parameter 2023: 75.59110064555725 19.22152183680314  # First call with the same seed
# Seed 2023: Parameter None: 75.59110064555725 19.22152183680314  # First call with the same seed
# Seed 2025:                 75.55118094349115 19.261441538869224


print("- " *40, "Loading", "- " *40)
oDatasetClone = DataSetBase("dummy", fs=oFileSys)
oDatasetClone.load_cache()
oDatasetClone.print_info()

nTSChecksum = np.sum(oDataset.ts_samples)
nVSChecksum = np.sum(oDataset.vs_samples)
print(nTSChecksum, nVSChecksum)


# // Unit Testing \\
assert nTSChecksum == 75.59110064555725
assert nVSChecksum == 19.22152183680314



