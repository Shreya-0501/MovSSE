# import the necessary packages
#from skimage.measure import compare_ssim
from skimage.metrics import structural_similarity
#import argparse
import imutils
import cv2
# construct the argument parse and parse the arguments

# load the two input images
imageA = cv2.imread("image5.png")
imageB = cv2.imread("image6.png")
# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# compute the Structural Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned
(score, diff) = structural_similarity(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))
