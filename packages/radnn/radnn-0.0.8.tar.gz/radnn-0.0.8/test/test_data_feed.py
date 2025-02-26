import numpy as np
from radnn.plots import AutoMultiImagePlot
from radnn import mlsys, FileSystem, print_tensor
from radnn.utils import data_hash, print_method_execution_time, interactive_matplotlib

from datasets.mnist import MNISTDataSet
from radnn.data import TFClassificationDataFeed

mlsys.filesys = FileSystem(dataset_folder="MLData", is_custom_setup=True)
mlsys.random_seed_all(2025)
mlsys.is_using_tensorflow = True

oDataset = MNISTDataSet(mlsys.filesys)
oDataset.load()
oDataset.print_info()
oDataset.sample_shape = [28, 28, 1]

oTS = TFClassificationDataFeed(oDataset, "train")
oTS.multiclass().standardize(-1).augment_crop(10).augment_flip_left_right().random_shuffle().batch(128)
print(oTS.value_preprocessor)


def epoch():
  for oMB_Samples, oMB_Labels in oTS.feed:
    #print(oMB_Samples.shape, oMB_Labels.shape)
    print(data_hash(oMB_Samples.numpy()))
    print(oMB_Labels.shape)
    break

print_method_execution_time(epoch)

if False:
  oPlot = AutoMultiImagePlot()
  for oMB_Samples, oMB_Labels in oTS.feed:
    for nIndex, nSample in enumerate(oMB_Samples):
      nLabel = np.argmax(oMB_Labels.numpy()[nIndex])
      if nIndex % 12 == 0:
        oPlot.add_row()

      nImage = nSample.numpy()
      oPlot.add_column(nImage, oDataset.class_names[nLabel])
      if nIndex == 71:
        print_tensor(nImage)
        break
    break
  oPlot.prepare("MNIST").show()

