#Implementation of an ideal passing filter on fourier transformed images
#Author - cryptographer3 (GitHub) (Self)

#Importing required libraries
import numpy as np

#Function for ideal pass filter
def idealpassfilter(transform, cutoff):
    X,Y = transform.shape
    res = np.zeros((X,Y), dtype=np.float32)
    for i in range(X):
        for j in range(Y):
            freq = np.sqrt((i-X/2)**2 + (j-Y/2)**2)
            if freq <= cutoff:
                res[i,j] = 1
            else:
                res[i,j] = 0
    return res