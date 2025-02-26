from radnn import mlsys


if mlsys.is_tensorflow_installed:
  from .keras_optimization_algorithm import KOptimizationAlgorithm

class LearningAlgorithm(object):
  # -----------------------------------------------------------------------------------
  def __init__(self, config, is_verbose=True):
    self.config = config
    self.is_verbose = is_verbose
    self._implementation = None

    self.prepare()
  # -----------------------------------------------------------------------------------
  @property
  def optimizer(self):
    oResult = None
    if self._implementation is not None:
      if isinstance(self._implementation, KOptimizationAlgorithm):
        oResult = self._implementation.optimizer
    return oResult
  # -----------------------------------------------------------------------------------
  @property
  def callbacks(self):
    oResult = None
    if self._implementation is not None:
      if isinstance(self._implementation, KOptimizationAlgorithm):
        oResult = self._implementation.callbacks
    return oResult
  # -----------------------------------------------------------------------------------
  def prepare(self):
    if mlsys.is_tensorflow_installed:
      self._implementation = KOptimizationAlgorithm(self.config, self.is_verbose)
    return self
  # -----------------------------------------------------------------------------------
