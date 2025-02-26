from radnn import mlsys, FileSystem
from radnn.experiment import MLExperimentConfig

mlsys.filesys = FileSystem()



CONFIG_BASE_CNN = MLExperimentConfig(number=1).assign({
                 "ModelName": "CIFAR10_BASECNN"
                ,"CNN.InputShape": [32,32,3]
                ,"CNN.Classes": 10
                ,"CNN.ModuleCount": 6
                ,"CNN.ConvOutputFeatures": [32,32,64,64,128,128]
                ,"CNN.ConvWindows": [ [3,2,True], [3,1,True] ,  [3,1,True], [3,2,True], [3,1,True], [3,1,True] ]
                ,"CNN.PoolWindows": [  None      , None       ,  None      , None      , [3,2]     , None      ]
                ,"CNN.HasBatchNormalization": True
                ,"Training.MaxEpoch": 3
                ,"Training.BatchSize": 128
                ,"Training.LearningRate": 0.1
                ,"Training.StepsPerEpoch": 391
                ,"Experiment.RandomSeed": 2023
            }).save()

print(CONFIG_BASE_CNN)
print(CONFIG_BASE_CNN.filename)