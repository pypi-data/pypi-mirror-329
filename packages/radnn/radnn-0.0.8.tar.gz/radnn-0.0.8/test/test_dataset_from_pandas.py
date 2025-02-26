import pandas as pd
import numpy as np
from radnn import mlsys, FileSystem
from radnn.data import DataSetBase

mlsys.random_seed_all(2025)
oFileSys = FileSystem("MLConfig", model_folder="MLModels", dataset_folder="MLData")

# Create first 7 random columns
random_data = np.random.randint(0, 100, size=(6, 7))

# Create last 3 columns with values [1, 2, 3] repeated
fixed_data = np.tile([1, 2, 3], (6, 1))

# Combine into a single DataFrame
IS_START = False
IS_RANGE = True

oDataset = DataSetBase("random_pd", fs=oFileSys)
if IS_START:
  df = pd.DataFrame(np.hstack((fixed_data, random_data)), columns=[f'label{i}' for i in range(1,4)] + [f'feature{i}' for i in range(1, 8)])
  df.info()
  if IS_RANGE:
    oDataset.assign(df, 0, 2)
  else:
    oDataset.assign(df, 0)
else:
  df = pd.DataFrame(np.hstack((random_data, fixed_data)), columns=[f'feature{i}' for i in range(1, 8)] + [f'label{i}' for i in range(1,4)] )
  df.info()
  if IS_RANGE:
    oDataset.assign(df, -3)
  else:
    oDataset.assign(df, -1)

oDataset.assign(df)
print("="*40 +  "Labels" +  "="*40)
print(oDataset.labels)
print("="*40 +  "Features" +  "="*40)
print(oDataset.samples)

oDataset.save_cache()