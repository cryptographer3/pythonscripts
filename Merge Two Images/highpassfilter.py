#Implementation for Butterworth High Pass Filter
#Author - cryptographer3 (GitHub) (Self)

#Usage -
#The highpassfilter(transform, cutoff, order) function takes the aforementioned values as input
#and return high pass coefficient for high frequency values.

#Importing required libraries
import numpy as np

#Function for high pass filter
def highpassfilter(transform, cutoff, order):
    X,Y = transform.shape #Number of rows and columns in the image
    res = np.zeros((X,Y), dtype=np.float32)
    for i in range(X):
        for j in range(Y):
            freq = np.sqrt((i-X/2)**2 + (j-Y/2)**2)
            res[i,j] = 1 / (1 + (cutoff/freq)**(2*order))
    return res