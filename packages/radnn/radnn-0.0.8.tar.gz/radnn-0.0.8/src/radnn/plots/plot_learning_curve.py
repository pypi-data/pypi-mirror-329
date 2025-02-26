# ======================================================================================
#
#     Rapid Deep Neural Networks
#
#     Licensed under the MIT License
# ______________________________________________________________________________________
# ......................................................................................

# Copyright (c) 2020-2025 Pantelis I. Kaplanoglou

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
import matplotlib.pyplot as plt

class PlotLearningCurve(object):
  # --------------------------------------------------------------------------------------
  def __init__(self, metrics_dict, model_name):
    self.metrics_dict = metrics_dict
    self.model_name = model_name
    print("Keys in training process log:", self.metrics_dict.keys())
  # --------------------------------------------------------------------------------------
  def prepare(self, metric_key="accuracy", custom_title=None, is_legend_right=False):
    plt.clf()
    plt.plot(self.metrics_dict[metric_key])
    sValidationMetricName = "val_" + metric_key
    if sValidationMetricName in self.metrics_dict:
      plt.plot(self.metrics_dict[sValidationMetricName])
    if custom_title is None:
      plt.title(self.model_name + ' ' + metric_key)
    else:
      plt.title(self.model_name + ' ' + custom_title)
    plt.ylabel(metric_key)
    plt.xlabel("Epoch")
    if is_legend_right:
      plt.legend(["train", 'validation'], loc="upper right")
    else:
      plt.legend(["train", "validation"], loc="upper left")
    return self
  # --------------------------------------------------------------------------------------
  def prepare_cost(self, cost_function=None):
    if isinstance(cost_function, str):
      sCostFunctionName = cost_function
    else:
      sClassName = str(cost_function.__class__)
      if ("keras" in sClassName) and ("losses" in sClassName):
        sCostFunctionNameParts = cost_function.name.split("_")
        sCostFunctionNameParts = [x.capitalize() + " " for x in sCostFunctionNameParts]
        sCostFunctionName = " ".join(sCostFunctionNameParts)

    return self.prepare("loss", sCostFunctionName, True)
  # --------------------------------------------------------------------------------------
  def save(self, filename):
    plt.savefig(filename, bbox_inches='tight')
    return self
  # --------------------------------------------------------------------------------------
  def show(self):
    plt.show()
  # --------------------------------------------------------------------------------------


