#Implementation for Butterworth Low Pass filter
#Author - cryptographer3 (GitHub) (Self)

#Usage -
#The lowpassfilter(transform, cutoff, order) function takes the aforementioned values as input
#and return low pass coefficient for low frequency values.

#Importing required libraries
import numpy as np

#Function for low pass filter
def lowpassfilter(transform, cutoff, order):
    X,Y = transform.shape #Number of rows and columns in the image
    res = np.zeros((X,Y), dtype=np.float32)
    for i in range(X):
        for j in range(Y):
            freq = np.sqrt((i-X/2)**2 + (j-Y/2)**2)
            res[i,j] = 1 / (1 + (freq/cutoff)**(2*order))
    return res