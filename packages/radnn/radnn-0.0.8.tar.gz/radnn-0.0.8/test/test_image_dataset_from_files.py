import numpy as np

from radnn import mlsys, FileSystem
from radnn.data import ImageDataSetFiles

mlsys.filesys = FileSystem(dataset_folder=r"M:\MLData", is_custom_setup=True)

oSourceFS = mlsys.filesys.datasets.subfs("FlagExplanations").subfs("dataset")

oImageFiles = ImageDataSetFiles(oSourceFS, "FlagX")
oImageFiles.load()
print("-"*35 +  "Folders" + "-"*35)
print(oImageFiles.class_folders)
print("-"*35 +  "Class Names" + "-"*35)
print(oImageFiles.class_names)
print("-"*80)


nSampleCount = np.zeros((len(oImageFiles.class_names.keys()), 3), dtype=np.int32)
for nClassIndex, (nClassKey, sClassName) in enumerate(oImageFiles.class_names.items()):
  nSampleCount[nClassIndex, 0] = len(oImageFiles.files[nClassIndex])
  nSampleCount[nClassIndex, 1] = len(oImageFiles.files_ts[nClassIndex])
  nSampleCount[nClassIndex, 2] = len(oImageFiles.files_vs[nClassIndex])

  print(f"{sClassName} {nSampleCount[nClassIndex, 0]} ts:{nSampleCount[nClassIndex, 1]} vs:{nSampleCount[nClassIndex, 2]}")
  #for oFile in oImageFiles.files[nClassIndex]:
    #print(oFile)

print(oImageFiles.total_file_count)
print("-"*80)
nSortedBySampleCountClassIndices = np.argsort(nSampleCount[:, 0])
for nClassIndex in nSortedBySampleCountClassIndices:
  nSamples = nSampleCount[nClassIndex, 0]
  if nSamples < 70:
    sClassName = oImageFiles.class_names[nClassIndex]
    print(f"{nClassIndex}-{sClassName}: {nSamples}" )
#nIndexMinFiles, nIndexMinFilesTS, nIndexMinFilesVS = nSampleCount.argmin(axis=0)
#print(oImageFiles.class_names[nIndexMinFiles], nSampleCount[nIndexMinFiles, ...])
#print(oImageFiles.class_names[nIndexMinFilesTS], nSampleCount[nIndexMinFilesTS, ...])
#print(oImageFiles.class_names[nIndexMinFilesVS], nSampleCount[nIndexMinFilesVS, ...])

import cv2
import random

sImageFile = oImageFiles.files[0][0]

print(sImageFile)
import cv2
import numpy as np
import cv2
import numpy as np

from PIL import Image
import numpy as np
import cv2
import numpy as np
import random


def roll_image(image_path, shift_x=0, shift_y=0):
    img = Image.open(image_path)
    arr = np.array(img)

    # Apply roll effect
    arr = np.roll(arr, shift_x, axis=1)  # Shift horizontally
    arr = np.roll(arr, shift_y, axis=0)  # Shift vertically

    img_out = Image.fromarray(arr)
    img_out.show()
    return img_out



def pan_zoom(image_path, scale=1.2, tx=30, ty=20):
  img = cv2.imread(image_path)
  h, w = img.shape[:2]

  # Transformation matrix for scaling and translation
  M = np.array([[scale, 0, tx],
                [0, scale, ty]], dtype=np.float32)

  # Apply affine warp
  result = cv2.warpAffine(img, M, (w, h))

  cv2.imshow("Pan & Zoom Effect", result)
  cv2.waitKey(0)
  cv2.destroyAllWindows()





def wave_effect(image_path, amplitude=30, frequency=0.05):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]

    # Create mapping arrays
    map_x = np.zeros((h, w), dtype=np.float32)
    map_y = np.zeros((h, w), dtype=np.float32)

    for i in range(h):
        for j in range(w):
            offset_x = int(amplitude * np.sin(2 * np.pi * frequency * i))
            map_x[i, j] = j + offset_x
            map_y[i, j] = i

    # Apply remapping
    result = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)

    cv2.imshow("Wavy Flag Effect", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




def random_light_saturation_cv(image_path, brightness_range=(0.8, 1.2), saturation_range=(0.8, 1.2)):
    img = cv2.imread(image_path)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)

    # Random brightness (Value channel)
    brightness_factor = random.uniform(*brightness_range)
    img_hsv[..., 2] = np.clip(img_hsv[..., 2] * brightness_factor, 0, 255)

    # Random saturation (Saturation channel)
    saturation_factor = random.uniform(*saturation_range)
    img_hsv[..., 1] = np.clip(img_hsv[..., 1] * saturation_factor, 0, 255)

    # Convert back to BGR
    img_hsv = img_hsv.astype(np.uint8)
    result = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    cv2.imshow("Random Light & Saturation", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def horizontal_wave_effect(image_path, amplitude=20, frequency=0.05):
  img = cv2.imread(image_path)
  h, w = img.shape[:2]

  # Create mapping arrays
  map_x = np.zeros((h, w), dtype=np.float32)
  map_y = np.zeros((h, w), dtype=np.float32)

  for i in range(h):
    for j in range(w):
      offset_y = int(amplitude * np.sin(2 * np.pi * frequency * j))  # Horizontal wave
      map_x[i, j] = j
      map_y[i, j] = i + offset_y  # Apply wave effect in Y direction

  # Apply remapping
  result = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)

  cv2.imshow("Horizontal Wavy Effect", result)
  cv2.waitKey(0)
  cv2.destroyAllWindows()


#random_light_saturation_cv(sImageFile)
horizontal_wave_effect(sImageFile, amplitude=10, frequency=0.01)
pan_zoom(sImageFile, scale=0.8, tx=0.1*300, ty=0.1*300)
roll_image(sImageFile, shift_x=50, shift_y=20)



