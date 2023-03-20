#A program to merge two images In order to create a hybrid image
#Author - cryptographer3
#Please note - low pass and high pass filters must be in the same directory as this program

import cv2
import matplotlib.pyplot as plt
import numpy as np
import highpassfilter as hpf
import lowpassfilter as lpf

#General info about the Butterworth pass filters - 
#The butterworth pass filters take the original image, a cutoff frequency and order as input
#and return coefficients for images that are either filtered for low frequencies or high frequencies

#Take various inputs from the user -
image1 = input("Please enter the address/name for the first image : ")
print(image1)
image2 = input("Please enter the address/name for the second image : ")
print(image2)
cutoff_low = int(input("Please enter the cutoff frequency for image to be smoothed : "))
order_low = int(input("Please enter an order for the butterworth low pass filter (Smoothening) (Recommended - 1) : "))
cutoff_high = int(input("Please enter the cutoff frequency for image to be Sharpened : "))
order_high = int(input("Please enter an order for the butterworth high pass filter (Sharpening) (Recommended - 1) : "))

#Plotting a figure for image display
fig = plt.figure(figsize=(30,30))
rows = 6
columns = 6

#Reading the image to be smoothened by passing through low pass filter -------------------------------------------------
readimage1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)

#Resize the image
w1 = 400
h1 = 400
lowpassimage = cv2.resize(readimage1, (w1, h1), interpolation = cv2.INTER_AREA)

fig.add_subplot(rows, columns, 1)
plt.imshow(lowpassimage, cmap="gray")
plt.title("Original Image 1")

#Fourier transform the image 1 into frquency domain 
lp = np.fft.fft2(lowpassimage)
lpshift = np.fft.fftshift(lp)

#Pass it through butterworth low pass filter 
coeff_low = lpf.lowpassfilter(lowpassimage, cutoff_low, order_low)
lowpassres = lpshift*coeff_low

#Inverse fourier transform to get Smoothed Image as output
smooth = np.fft.ifftshift(lowpassres)
fig.add_subplot(rows, columns, 2)
plt.imshow(np.log1p(np.abs(smooth)), cmap="gray")
plt.title("Frequency domain of smoothed Image")

smooth_back = np.abs(np.fft.ifft2(smooth))

fig.add_subplot(rows, columns, 3)
plt.imshow(smooth_back, cmap="gray")
plt.title("Smoothed Image")


#Reading the image to be Sharpened by passing through high pass filter -------------------------------------------------
readimage2 = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)

#Resize the image
w2 = 400
h2 = 400
highpassimage = cv2.resize(readimage2, (w2, h2), interpolation = cv2.INTER_AREA)

fig.add_subplot(rows, columns, 4)
plt.imshow(highpassimage, cmap="gray")
plt.title("Original Image 2")

#Fourier transform the image 2 into frquency domain 
hp = np.fft.fft2(highpassimage)
hpshift = np.fft.fftshift(hp)

#Pass it through butterworth high pass filter 
coeff_high = hpf.highpassfilter(highpassimage, cutoff_high, order_high)
highpassres = hpshift*coeff_high

#Inverse fourier transform to get Sharpened Image as output
sharp = np.fft.ifftshift(highpassres)
fig.add_subplot(rows, columns, 5)
plt.imshow(np.log1p(np.abs(sharp)), cmap="gray")
plt.title("Frequency domain of sharpened Image")

sharp_back = np.abs(np.fft.ifft2(sharp))

fig.add_subplot(rows, columns, 6)
plt.imshow(sharp_back, cmap="gray")
plt.title("Sharpened Image")
plt.show()


#Resulting Image
resimagefourier = lowpassres + highpassres
resimage = np.fft.ifftshift(resimagefourier)
resimage_back = np.abs(np.fft.ifft2(resimage))

plt.imshow(resimage_back, cmap="gray")
plt.title("Hybrid Image")
plt.show()
