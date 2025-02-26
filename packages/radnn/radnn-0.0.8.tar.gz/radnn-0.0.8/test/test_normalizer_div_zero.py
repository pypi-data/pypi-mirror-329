import numpy as np
from radnn.data.preprocess import Normalizer

# Create a 20x3 array, with all elements initially set to zero
original_data = np.zeros((20, 3))

IS_INTEGER = False
# Optionally, you can modify the other columns with random values or other numbers
if IS_INTEGER:
  original_data[:, 1] = np.random.randint(-100, 100, size=20)  # Column 2 with random integers
  original_data[:, 2] = np.random.randint(-100, 100, size=20)  # Column 3 with random integers
else:
  original_data[:, 1] = np.random.random(size=20) *1000000 # Column 2 with random integers
  original_data[:, 2] = np.random.random(size=20) *1000000  # Column 3 with random integers


print(original_data)

oScaler2 = Normalizer()
normalized_data = oScaler2.fit_transform(original_data)
denormalized_data = oScaler2.inverse_transform(normalized_data)
print(np.sum(normalized_data))
assert np.sum(original_data) == np.sum(denormalized_data), "invalid transformation"
