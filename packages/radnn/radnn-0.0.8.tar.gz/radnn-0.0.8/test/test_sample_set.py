import numpy as np
from radnn import mlsys, FileSystem
from datasets.mnist import MNISTDataSet
from radnn.data import SampleSet
from radnn.data import TFDataPipeline

mlsys.filesys = FileSystem(is_custom_setup=True)

oMnist = MNISTDataSet()
oMnist.load()

SampleSet("ts").subset_of(oMnist)
SampleSet("vs").subset_of(oMnist)


for nIndex, (nId, nSample, nLabel) in enumerate(oMnist.vs):
  print(nId, np.sum(nSample), nLabel)
  if nIndex == 10:
    break

oMnist.vs.labels = None

print("."*80)
for nIndex, (nId, nSample) in enumerate(oMnist.vs):
  print(nId, np.sum(nSample))
  if nIndex == 10:
    break
print("-"*80)
for nIndex, (nId, nSample, nLabel) in enumerate(oMnist.ts):
  print(nId, np.sum(nSample), nLabel)
  if nIndex == 10:
    break


oMnist.ts.feed = TFDataPipeline(oMnist.ts).standardize().augment().shuffle().batch(128).feed
oMnist.vs.feed = TFDataPipeline(oMnist.vs).standardize().batch(oMnist.vs.sample_count).feed

print(oMnist.ts.feed)
print(oMnist.vs.feed)



