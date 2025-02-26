from radnn import FileSystem, FileStore
from radnn.experiment import MLExperimentEnv, MLExperimentConfig

# Creating a file system with a group and a sub-group of experiments
oFileSys = FileSystem().group("C-MNIST").group("EXP18-08")
oFileSys.save_setup()

# Using the default configuration file store from the file system with a fixed experiment code
oEnv1 = MLExperimentEnv(oFileSys, experiment_code="LREXPLAINET18_FMNIST_08-02")
oEnv1.save_config()
print(oEnv1)

# Using custom file stores and model code parts
oEnv2 = MLExperimentEnv(FileStore("MLConfig"), FileStore("MLModels"), "CREXPLAINET18_FMNIST", 8, None, 10)
oEnv2.save_config()
print(oEnv2)

# Using a filename that may contain iso date/time
sFileName = oFileSys.models.subfs("LREXPLAINET18_FMNIST_08-03").file("2024-05-15_231244_LREXPLAINET18_FMNIST_08-03.json")
print(sFileName)
oEnv3 = MLExperimentEnv(oFileSys, experiment_filename=sFileName)
oEnv3.save_config()
print(oEnv3)


# Importing a configuration and exporting to other experiment
sImportFileName = FileSystem(setup_filename=None).configs.file("LREXPLAINET18_08_Template.json")
sFileName = oFileSys.configs.file("LREXPLAINET18_FMNIST_08-10.json")
print(f"Importing from {sImportFileName}")
oConfig = MLExperimentConfig(sImportFileName)
oEnv4 = MLExperimentEnv(oFileSys, experiment_filename=sFileName, experiment_config=oConfig)
print(f"Saving to {sFileName}")
oEnv4.save_config()

# Creating multiple folds out of loaded configuration template
for nFoldNumber in range(1, 10):
  oConfig["Experiment.FoldNumber"] = nFoldNumber
  oEnvFold = MLExperimentEnv(oFileSys, None,
                             "NEXPERIMENT_MNIST", 1, None, nFoldNumber, experiment_config=oConfig)
  print(f"Saving to {oEnvFold.experiment_filename}")
  oEnvFold.save_config()

