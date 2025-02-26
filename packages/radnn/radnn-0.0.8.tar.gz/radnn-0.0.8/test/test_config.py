from radnn import FileSystem
from radnn.experiment import MLExperimentConfig


oSys = FileSystem("MLConfig", "MLModels", "MLData")

oConfig = MLExperimentConfig(number=3).assign(
        {
            "ModelName": "QPEDS_MLP"
           ,"DNN.InputFeatures": 72
           ,"DNN.LayerNeurons": [288, 4]
           ,"DNN.Classes": 4
           ,"Training.MaxEpoch": 200
           ,"Training.BatchSize": 160
           ,"Training.LearningRate": 0.2
           ,"Experiment.RandomSeed": 2022
         }
).save_config(oSys)
print(oConfig)

print("."*40, "Loading", "."*40)
oConfig = MLExperimentConfig().load_config(oSys, "QPEDS_MLP_03")

print(oConfig)
print(oConfig.get_experiment_code)