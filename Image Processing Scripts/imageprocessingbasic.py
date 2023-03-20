#A script for analysing various aspects of image modifications
#Author - cryptographer3

#Importing the OpenCV library
import cv2

#Importing the matplotlib library
from matplotlib import pyplot as plt

#importing the numpy library 
import numpy as np

#Take input from the user for the target image
targetimage = input("Please enter the address/name for the image : ")

#Reading the target image file and storing it in a variable ---------------------------------------------- section a
image1 = cv2.imread(targetimage)
cv2.imshow(str(target image), image1)


#Converting the target image to grayscale ---------------------------------------------------------------- section b
image1_grayscale = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
cv2.imshow((str(target image) + ' in grayscale'), image1_grayscale)

#Plotting the histogram for the grayscale version of the target image and displaying it ------------------ section c
image1hist = cv2.calcHist([image1_grayscale], [0], None, [256], [0, 256])
plt.hist(image1_grayscale.ravel(),256,[0,256])
plt.title('Histogram for grayscale ' + str(targetimage))


#Thresholding the image ---------------------------------------------------------------------------------- section d
thresh1, blacknwhite = cv2.threshold(image1_grayscale, 175, 255, cv2.THRESH_BINARY)
cv2.imshow(('black and white rendition of ' + str(targetimage) +'with a threshold value of 175' ),blacknwhite)

#Performing morphological process of erosion on the black and white image -------------------------------- section e
mask = np.ones((3, 3), np.uint8)
image1_erosion = cv2.erode(blacknwhite, mask, iterations = 1)
cv2.imshow(('Erosion of the b/w rendition of ' + str(targetimage)), image1_erosion)

#Performing morphological process of dilation on the black and white image ------------------------------- section f
mask = np.ones((3, 3), np.uint8)
image1_dilation = cv2.dilate(blacknwhite, mask, iterations = 1)
cv2.imshow(('Dilation of the b/w rendition of ' + str(targetimage)), image1_dilation)

#Counting the number of objects in the image ------------------------------------------------------------- section g

#Inverting the binary image in order to make the background as black and objects as white (for border distinction)
whitenblack = cv2.bitwise_not(blacknwhite)
#Morphologically dilating the image in order to remove distortion and noise
mask = np.ones((3, 3), np.uint8)
image1_dilated = cv2.dilate(whitenblack, mask, iterations = 7)

#Test for printing this inverted binary image
#cv2.imshow('Inverted Binary image after certain cycles of dilation', image1_dilated)

#Finding the contour shapes(peaks that will mark the boundary with the black background)
contours, order = cv2.findContours(image1_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#Storing and printing the number of objects
num_objects = len(contours)
print()
print("The total number of objects in the image is : " + str(num_objects))
print()

plt.show()
