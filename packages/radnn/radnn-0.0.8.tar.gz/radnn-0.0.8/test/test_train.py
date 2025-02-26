from experiment.ml_experiment import MLExperiment
from radnn import mlsys, FileSystem
from radnn.experiment import MLExperimentConfig
from radnn.learn import LearningAlgorithm
from datasets.mnist import MNISTDataSet, CMNISTDataFeed
from models import CNNBasic
from tensorflow import keras

mlsys.use_tensorflow()
mlsys.filesys = FileSystem(config_folder="MLConfig", model_folder="MLModels", dataset_folder="MLData", is_custom_setup=True)
mlsys.random_seed_all(2025)

oDataset = MNISTDataSet()
oDataset.load()
oDataset.print_info()

oConfig = MLExperimentConfig(base_name="CNN_MNIST", number=1, fold_number=1).assign(
  {
    "ClassCount": oDataset.class_count,
    "InputShape": [28,28,1],



    "CNN.InputShape": [28,28,1],
    "CNN.Classes": oDataset.class_count,
    "CNN.ModuleCount": 4,
    "CNN.ConvOutputFeatures": [16, 16, 16, 16],
    "CNN.ConvWindows": [[3,1], [3,2], [3,1], [3,2]],
    "CNN.PoolWindows": [None, None, None, None],

    "Prediction.BatchSize": None,

    "Training.BatchSize": 128,
    "Training.Optimizer": "SGD",
    "Training.LearningRate": 0.01,
    "Training.Momentum": 0.9,
    "Training.LearningRateSchedule": [[3, 0.01], [6, 0.001]],
    "Training.MaxEpoch": 10
  }
).save(mlsys.filesys)

oFeeds = CMNISTDataFeed(oDataset, oConfig)

oCNN = CNNBasic(oConfig)
oAlgorithm = LearningAlgorithm(oConfig)
oCost = keras.losses.CategoricalCrossentropy()
oMetrics = ["accuracy"]
oExperiment = MLExperiment(oConfig, oCNN, oAlgorithm, oCost, oMetrics, is_retraining=False)

# //TODO: Builder pattern for dataset
oExperiment.training_set = oFeeds.TSFeed
oExperiment.validation_set = oFeeds.VSFeed
oExperiment.dataset = oDataset

oExperiment.train()
oExperiment.plot_learning_curve()
oExperiment.evaluate_classifier()
