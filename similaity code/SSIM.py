# Imports
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity
from skimage.transform import resize
import numpy as np
import cv2
import os
from PIL import Image 
# import imutils


#  to generate video from frames 
def generate_video():
    image_folder = "D:\sem 6\sem project\onetest\images" # make sure to use your folder
    video_name = 'struct_sim_generatedvideo.avi'
    os.chdir("D:\sem 6\sem project\onetest")
      
    # images = [img for img in image_files_sorted]
     
    # Array images should only consider the image files ignoring others if any print(images) 
  
    frame = cv2.imread(os.path.join(image_folder, image_files_sorted[0]))
  
    # setting the frame width, height width
    # the width, height of first image
    height, width, layers = frame.shape  
  
    video = cv2.VideoWriter(video_name, 0, 24, (width, height)) 
  
    # Appending the images to the video one by one
    for image in image_files_sorted: 
        video.write(cv2.imread(os.path.join(image_folder, image))) 
        # print("writing image into the video")
      
    # Deallocating memories taken for window creation
    cv2.destroyAllWindows() 
    video.release()  # releasing the video generated
  


# function for plotting the values of similarity algos
def similarityPlot(similarity_array):
  y = similarity_array
  n = len(y)
  # print(y)
  x = []
  for i in range(n):
    x.append(i)
  # print(len(x))
#   plt.plot(y, linestyle ="solid")
#   plt.show()
  plt.plot(y, linestyle ="solid")
  plt.show()


# ---Function to check SSIM similarity---
def SSIM_similarity(imageA, imageB):

  # compute the Structural Similarity Index (SSIM) between the two images, ensuring that the difference image is returned
  (score, diff) = structural_similarity(imageA, imageB, full=True)
  diff = (diff * 255).astype("uint8")
#   print("SSIM: {}".format(score))
  return score


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
# frameExtract()

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

# to break the movie into frames
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
    SSIM = SSIM_similarity(img1_bw, img2_bw)
    # print(SSIM)

    # print("Orb similarity: ")
    # print(orb)
    struct_sim.append(SSIM)
with open("D:\sem 6\sem project\onetest\struct_similarityVals.txt", "w") as output:
  output.write(str(struct_sim))

mean_height = 0
mean_width = 0
# To combine frames into shots
for image in range(len(image_files_sorted)):
  im = Image.open(os.path.join("D:\sem 6\sem project\onetest\images", image_files_sorted[image]))
  width, height = im.size
  # print(width, height)
  mean_width += width
  mean_height += height

mean_width = int(mean_width / len(image_files_sorted))
mean_height = int(mean_height /len(image_files_sorted))
# print(mean_height, mean_width)


  
# Calling the generate_video function
generate_video()
print("done generating video")


similarityPlot(struct_sim)
