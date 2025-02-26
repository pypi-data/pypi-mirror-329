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
import sys
import socket
import platform
import subprocess
from datetime import datetime

# ----------------------------------------------------------------------------------------------------------------------
def system_name() -> str:
  return MLInfrastructure.host_name(False)
# ----------------------------------------------------------------------------------------------------------------------
def now_iso():
  return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
# ----------------------------------------------------------------------------------------------------------------------
def shell_command_output(command_string):
  oOutput = subprocess.check_output(command_string, shell=True)
  oOutputLines = oOutput.decode().splitlines()

  oResult = []
  for sLine in oOutputLines:
      oResult.append(sLine)

  return oResult
# ----------------------------------------------------------------------------------------------------------------------





# ======================================================================================================================
class MLInfrastructure(object):
  # --------------------------------------------------------------------------------------------------------------------
  @classmethod
  def is_linux(cls):
    return not (cls.is_windows or cls.is_colab or cls.is_macos())
  # --------------------------------------------------------------------------------------------------------------------
  @classmethod
  def is_windows(cls):
    sPlatform = platform.system()
    return (sPlatform == "Windows")
  # --------------------------------------------------------------------------------------------------------------------
  @classmethod
  def is_colab(cls):
    return "google.colab" in sys.modules
  # --------------------------------------------------------------------------------------------------------------------
  @classmethod
  def is_macos(cls):
    sPlatform = platform.system()
    return (sPlatform == "Darwin")
  # --------------------------------------------------------------------------------------------------------------------
  @classmethod
  def host_name(cls, is_using_ip_address=True) -> str:
    sPlatform = platform.system()
    sHostName = socket.gethostname()
    sIPAddress = socket.gethostbyname(sHostName)

    bIsColab = "google.colab" in sys.modules
    if bIsColab:
      sResult = "(colab)"
      if is_using_ip_address:
        sResult += "-" + sIPAddress
    else:
      if sPlatform == "Windows":
        sResult = "(windows)-" + sHostName
      elif sPlatform == "Darwin":
        sResult = "(macos)-" + sHostName
      else:
        sResult = "(linux)-" + sHostName
    return sResult
  # --------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================