# ======================================================================================
#
#     Rapid Deep Neural Networks
#
#     Licensed under the MIT License
# ______________________________________________________________________________________
# ......................................................................................

# Copyright (c) 2018-2025 Pantelis I. Kaplanoglou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# .......................................................................................
import os
import random
import numpy as np
import importlib

class MLSystem(object):
  # --------------------------------------------------------------------------------------
  _instance = None
  @classmethod
  def Instance(cls):
    if cls._instance is None:
      cls._instance = cls()
      mlsys = cls._instance
    return cls._instance
  # --------------------------------------------------------------------------------------
  @property
  def is_using_tensorflow(self):
      return self.is_tensorflow_installed and self._is_using_tensorflow
  # --------------------------------------------------------------------------------------
  @is_using_tensorflow.setter
  def is_using_tensorflow(self, value):
    self._is_using_tensorflow = value
    self._is_using_torch = not value
  # --------------------------------------------------------------------------------------
  @property
  def is_using_torch(self):
      return self.is_torch_installed and self.is_using_torch
  # --------------------------------------------------------------------------------------
  @is_using_torch.setter
  def is_using_torch(self, value):
    self._is_using_torch = value
    self._is_using_tensorflow = not value
  # --------------------------------------------------------------------------------------
  def __init__(self):
    self._is_random_seed_initialized = False
    self._filesys = None
    self._seed = None
    self.switches = dict()
    self.switches["IsDebuggable"] = False

    self.is_tensorflow_installed = False
    self.is_torch_installed = False
    self.is_opencv_installed = False

    self._is_using_tensorflow = False
    self.is_using_torch = False
  # --------------------------------------------------------------------------------------
  @property
  def filesys(self):
    return self._filesys
  # ............................
  @filesys.setter
  def filesys(self, value):
    self._filesys = value

  # --------------------------------------------------------------------------------------
  @property
  def seed(self):
    return self._seed
  # --------------------------------------------------------------------------------------
  # We are seeding the number generators to get some amount of determinism for the whole ML training process.
  # For Tensorflow it is not ensuring 100% deterministic reproduction of an experiment on the GPU.
  def random_seed_all(self, seed, is_done_once=False, is_parallel_deterministic=False):
    self._seed = seed

    bContinue = True
    if is_done_once:
      bContinue = (not self._is_random_seed_initialized)

    if bContinue:
      random.seed(seed)
      os.environ['PYTHONHASHSEED'] = str(seed)
      np.random.seed(seed)
      if mlsys.is_tensorflow_installed:
        import tensorflow as tf
        tf.compat.v1.reset_default_graph()
        if is_parallel_deterministic:
          tf.config.experimental.enable_op_determinism()  # Enable determinism for num_parallel_calls
        tf.random.set_seed(seed)
        tf.keras.utils.set_random_seed(seed)
      if mlsys.is_torch_installed:
        import torch
        torch.manual_seed(seed)
        # GPU and multi-GPU
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        # For GPU determinism
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

      self._is_random_seed_initialized = True
      print("(>) Random seed set to %d" % seed)
  # --------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def is_tensorflow_installed():
    bIsInstalled = importlib.util.find_spec("tensorflow") is not None
    if not is_tensorflow_installed:
      bIsInstalled = importlib.util.find_spec("tensorflow-gpu") is not None
    return bIsInstalled
# ----------------------------------------------------------------------------------------------------------------------


mlsys: MLSystem = MLSystem.Instance()
mlsys.is_tensorflow_installed = is_tensorflow_installed()
mlsys.is_torch_installed = importlib.util.find_spec("torch") is not None
mlsys.is_opencv_installed = importlib.util.find_spec("cv2") is not None
