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
import shutil
import glob
import sys
if (sys.version_info.major == 3) and (sys.version_info.minor <= 7):
  import pickle5 as pickle
else:
  import pickle
from radnn.system.files import FileList
from radnn.system.files import JSONFile
from radnn.system.files import PickleFile
from radnn.system.files import TextFile
from radnn.system.files import CSVFile
from radnn.ml_system import mlsys
if mlsys.is_opencv_installed:
  from radnn.system.files.imgfile import PNGFile




# =======================================================================================================================
class FileStore(object):
  # --------------------------------------------------------------------------------------------------------
  def __init__(self, base_folder, is_verbose=False, must_exist=False):
    #.......................... |  Instance Attributes | ............................
    self.base_folder = base_folder
    self.absolute_path = os.path.abspath(base_folder)
    if not os.path.exists(self.base_folder):
      if must_exist:
        raise Exception(f"File store folder {self.base_folder} does not exist.")
      else:
        os.makedirs(self.base_folder)

    self.is_verbose  = is_verbose
    self.json = JSONFile(None, parent_folder=self.base_folder)
    self.obj = PickleFile(None, parent_folder=self.base_folder)
    self.text = TextFile(None, parent_folder=self.base_folder)
    self.csv = CSVFile(None, parent_folder=self.base_folder)
    if mlsys.is_opencv_installed:
      self.img = PNGFile(None, parent_folder=base_folder)
    self.donefs = None
    #................................................................................
  # --------------------------------------------------------------------------------------------------------
  @property
  def has_files(self):
    return not self.is_empty
  # --------------------------------------------------------------------------------------------------------
  @property
  def is_empty(self):
    bExists = not os.path.exists(self.base_folder)
    if not bExists:
      bExists = len(os.listdir(self.base_folder)) > 0
    return not bExists
  # --------------------------------------------------------------------------------------------------------
  def exists_folder(self, filename):
    sFullPath = os.path.join(self.base_folder, filename)
    return os.path.exists(sFullPath)
  # --------------------------------------------------------------------------------------------------------
  def exists(self, filename):
    sFullFilePath = os.path.join(self.base_folder, filename)
    return os.path.isfile(sFullFilePath)
  # --------------------------------------------------------------------------------------------------------
  def subfs(self, subfolder_name, must_exist=False):
    return FileStore(self.subpath(subfolder_name), must_exist=must_exist)
  # --------------------------------------------------------------------------------------------------------
  def subpath(self, subfolder_name):
    if os.path.sep == "\\":
      if subfolder_name.find(os.path.sep) < 0:
        subfolder_name = subfolder_name.replace("/", "\\")
    return self.folder(subfolder_name)
  # --------------------------------------------------------------------------------------------------------
  def folder(self, folder_name):
    sFolder = os.path.join(self.absolute_path, folder_name)
    if not os.path.exists(sFolder):
      os.makedirs(sFolder)

    return sFolder
  # --------------------------------------------------------------------------------------------------------
  def file(self, file_name, file_ext=None):
    if file_ext is not None:
      if file_ext.find(".") < 0:
        file_name += "." + file_ext
      else:
        file_name += file_ext
    return os.path.join(self.absolute_path, file_name)
  # --------------------------------------------------------------------------------------------------------
  def entries(self):
    return os.listdir(self.base_folder)
  # --------------------------------------------------------------------------------------------------------
  def _ls(self, file_matching_pattern, is_removing_extension, sort_filename_key):
    if ";" in file_matching_pattern:
      sEntries = []
      for sExt in file_matching_pattern.split(";"):
        sEntries += glob.glob1(self.base_folder, sExt.strip())
    else:
      sEntries = glob.glob1(self.base_folder, file_matching_pattern)

    if is_removing_extension:
      oFileNamesOnly = []
      for sEntry in sEntries:
        sFileNameOnly, _ = os.path.splitext(sEntry)
        oFileNamesOnly.append(sFileNameOnly)
      sEntries = sorted(oFileNamesOnly, key=sort_filename_key)

    return sEntries
  # --------------------------------------------------------------------------------------------------------
  def list_files(self, file_matching_pattern, is_full_path=True, is_removing_extension=False, sort_filename_key=None):
    sEntries = self._ls(file_matching_pattern, is_removing_extension, sort_filename_key)
    if is_full_path:
      oResult = [os.path.join(self.base_folder, x) for x in sEntries]
    else:
      oResult = [x for x in sEntries]
    return oResult
  # --------------------------------------------------------------------------------------------------------
  def filelist(self, file_matching_pattern, is_removing_extension=False, sort_filename_key=None):
    sEntries = self._ls(file_matching_pattern, is_removing_extension, sort_filename_key)
    oFileList = FileList(self.base_folder)
    for x in sEntries:
      oFileList.append(x)
    return oFileList
  # --------------------------------------------------------------------------------------------------------
  def list_folders(self, is_full_path=True):
    sResult = []
    for sFolder in os.listdir(self.base_folder):
      sFullPath = os.path.join(self.base_folder, sFolder)
      if os.path.isdir(sFullPath):
        if is_full_path:
          sResult.append(sFullPath)
        else:
          sResult.append(sFolder)
    return sResult
  # --------------------------------------------------------------------------------------------------------
  def dequeue_file(self, file_matching_pattern, is_full_path=True, archive_folder_name=".done"):
    if self.donefs is None:
      self.donefs = self.subfs(archive_folder_name)
    oQueue = self.files(file_matching_pattern, is_full_path=False)

    if len(oQueue) == 0:
      sFileName = None
    else:
      sFileName = oQueue[0]
      shutil.move(os.path.join(self.base_folder, sFileName), os.path.join(self.donefs.base_folder, sFileName))

    if is_full_path and (sFileName is not None):
      sFileName = os.path.join(self.donefs.base_folder, sFileName)
    return sFileName
  # --------------------------------------------------------------------------------------------------------
  def purge_done(self):
    #//TODO: Remove from the current filestore all files that are moved into the .done filestore
    pass
  # ----------------------------------------------------------------------------------
  def __repr__(self)->str:
    return self.absolute_path
  # --------------------------------------------------------------------------------------------------------
  def __str__(self)->str:
    return self.absolute_path
  # --------------------------------------------------------------------------------------------------------
# ======================================================================================================================


# .................... Tests ....................
if __name__ == "__main__":
  VISUALIZE = False
  import numpy as np

  # Lazy initialize a file store folder
  oFS = FileStore("C:\MLData\SomeDataSet")

  # Serialize data into a sub folder
  oData = np.asarray([1, 2, 3]).astype(np.float32)
  print(oFS.subfs("test"))
  oFS.subfs("test").obj.save(oData, "sample1.pkl")

  # Get paths
  print("==== Paths ====")
  print(oFS.subfs("test").file("sample1.png"))
  print(oFS.folder("test"))

  # Deserialize data from a sub folder
  oLoadedData = oFS.subfs("test").obj.load("sample1.pkl")
  print(oLoadedData)

  # List files
  print("==== Files ====")
  sFiles = oFS.subfs("test").list_files("*.pkl", True)
  print("\n".join(sFiles))

  # Load a PNG file
  if (is_opencv_installed()):
    oPng = FileStore("C:\\UX").subfs("PNG").img.load("Ideas.png")
    print(oPng.shape)

    if VISUALIZE:
      import matplotlib.pyplot as plt
      plt.imshow(oPng)
      plt.show()



