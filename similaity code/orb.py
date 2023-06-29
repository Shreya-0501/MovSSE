# Imports
import matplotlib.pyplot as plt
# plt.style.use('seaborn-whitegrid')
from skimage.metrics import structural_similarity
from skimage.transform import resize
import numpy as np
import cv2
import os
# import imutils


# function for plotting the values of similarity algos
def similarityPlot(similarity_array):
  y = similarity_array
  n = len(y)
  # print(y)
  x = []
  for i in range(n):
    x.append(i)
  # print(len(x))
  plt.plot(y, linestyle ="solid")
  plt.show()
  # plt.scatter(x,y)
  # plt.show()



# ---Function to check orb similarity---
def orbSimilarity(img1, img2):
  orb = cv2.ORB_create()
  if img1.shape != img2.shape:
    img2 = resize(img2, (img1.shape[0], img1.shape[1]), anti_aliasing=True, preserve_range=True)
  # detect keypoints and descriptors
  kp_a, desc_a = orb.detectAndCompute(img1, None)
  kp_b, desc_b = orb.detectAndCompute(img2, None)
  

  # print(desc_a, desc_b)
  if(desc_a is None or desc_b is None):
    # print("one none val")
    return 0
  # define the bruteforce matcher object
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
  #perform matches. 
  matches = bf.match(desc_a, desc_b)
  #Look for similar regions with distance < 50. Goes from 0 to 100 so pick a number between.
  similar_regions = [i for i in matches if i.distance < 40]  
  if len(matches) == 0:
    return 0
  return len(similar_regions) / len(matches)


def frameExtract():

  # path to video
  vid = cv2.VideoCapture("D:\sem 6\sem project\onetest/slaps.mp4")
  
  try:

    # creating a folder to store frames
    if not os.path.exists('images'):
        os.makedirs('images')

  except OSError:
      print('Error: Creating directory of data')


  currentframe = 0
  while (True):

      # reading from frame
      success, frame = vid.read()

      if success:
          # continue creating images until video remains
          name = './images/' + str(currentframe) + '.jpg'
          # print('Creating...' + name)

          # writing the extracted images
          cv2.imwrite(name, frame)

          # increasing counter so that it will
          # show how many frames are created
          currentframe += 1
      else:
          break

  # Release all space and windows once done
  vid.release()
  cv2.destroyAllWindows()
  
  
  
#driver code begins here

# 1) Divide the video into frames and store 
frameExtract()

# 2) Convert images to matrix form
img1_path = os.getcwd()
path = img1_path + '/' + 'images'
os.chdir(path)  #getting the path of the images in folder "images"
print("path: " + os.getcwd())  # printing the path of the current working directory

image_files = os.listdir()  #  reading the contents of the folder
read_images = [] 
orb_sim = []
struct_sim = []
sift_sim = []

# 3) Convert pairs of images to matrix form, greyscale and compare orb similarities
iterator = 0
# print(image_files)

# SORTING LIST OF IMAGES 
image_files_sorted = sorted(image_files, key=lambda x: int(os.path.splitext(x)[0]))

for image in range(len(image_files_sorted)-1):
    # print(image)

    #  convert both images in imread form 
    img1 = cv2.imread(image_files_sorted[image])
    img2 = cv2.imread(image_files_sorted[image+1])

    # read_images.append(cv2.imread(image, 0))

    # Convert it to grayscale
    img1_bw = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    img2_bw = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Initialize the ORB detector algorithm
    # print("Going to orb sim")
    orb = orbSimilarity(img1_bw, img2_bw)

    # print("Orb similarity: ")
    # print(orb)
    orb_sim.append(orb)

print(orb_sim)
with open("D:\sem 6\sem project\onetest\orb_similarityVals.txt", "w") as output:
    output.write(str(orb_sim))


# for idx in enumerate(orb_sim):
#   print(idx, idx+1 , orb_sim[idx])

# plotting for orb similarity
similarityPlot(orb_sim)
