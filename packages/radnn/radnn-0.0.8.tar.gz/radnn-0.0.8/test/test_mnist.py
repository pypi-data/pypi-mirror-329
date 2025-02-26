import os
from radnn import FileSystem, mlsys, print_tensor
from datasets.mnist import MNISTDataSet

import matplotlib.pyplot as plt

IS_TESTING_NORMALIZATION = True
IS_TESTING_FEED = True


oFileSys = FileSystem(dataset_folder="MLData")

mlsys.random_seed_all(2024)
oMNIST = MNISTDataSet(oFileSys)
oMNIST.load(is_overwriting=True)
oMNIST.print_info()

'''
print("[MNIST] Total Samples:%d   | Features:%d | Classes: %d" % (
oMNIST.SampleCount, oMNIST.FeatureCount, oMNIST.ClassCount))
print("[MNIST] Training:%d        |" % (oMNIST.TSSampleCount))
print("[MNIST] MemoryTest:%d            |" % (oMNIST.VSSampleCount))
'''


if True:
  from datasets.mnist.mnist_data_feed import CMNISTDataFeed

  config = {"InputShape": [28, 28, 1], "ClassCount": 10, "Training.BatchSize": 128, "Validation.BatchSize": 128,
            "Prediction.BatchSize": 200}
  oFeed = CMNISTDataFeed(oMNIST, config)
  print(f"mean: {oFeed.PixelMean} std:{oFeed.PixelStd}")
  (nSamples, nLabels) = next(iter(oFeed.TSFeed))
  plt.figure(figsize=(10, 10))
  for i in range(25):
    plt.subplot(5, 5, i + 1)
    nImage = nSamples[i].numpy().squeeze()
    plt.imshow(nImage, cmap='gray')
    plt.title(f"Label: {nLabels[i]}")
    plt.axis('off')
  print_tensor(nImage)
  plt.show()

