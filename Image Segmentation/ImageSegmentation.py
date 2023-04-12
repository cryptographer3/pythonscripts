# A GUI Based Program for Image Segmentation
# Author - cryptographer3

# Procedure overview -
# After you load the image, please move the respective scales for lower and upper thresholds 
# and the result image will be updated automatically. After the image is loaded, and the parameters are provided, the image
# is passed through a function whose purpose is to filter out H component values from the HSV color space of the image,
# Then the H component and the provided parameters are used to create a mask for segmentation and applied onto the original image
# in order to output the desired segmented image.

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Importing the required libraries

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np 
import cv2
import matplotlib as plt

class ImageGUI:
   
    def __init__(self, master):
        self.master = master
        self.master.title("Image GUI")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------   
        # Section to handle all the frames in the entire Tkinter window
        
        # Create a frame for displaying the photos and center it
        self.image_frame = tk.Frame(self.master)

        # Create frame 1 for displaying image loading button
        self.button_frame1 = tk.Frame(self.master)

        # Create frame 2 for displaying parameter scales
        self.button_frame2 = tk.Frame(self.master)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------       
        # Section to handle load image button and loaded image label display
        
        # Create a "Load Image" button
        self.load_button = tk.Button(self.button_frame1, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.TOP, padx=10, pady=10)
        # Create a label to display the chosen image
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(side=tk.LEFT)
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
        # Section for input parameters handling
        
        # ->Create a Scale widget for the Minimum Threshold
        self.lower_threshold = tk.IntVar()
        self.lower_threshold_scale = tk.Scale(self.button_frame2, from_=0, to=255, orient=tk.HORIZONTAL, label="Lower Threshold Value", length = 150, variable=self.lower_threshold)
        self.lower_threshold_scale.bind("<ButtonRelease-1>", self.re_perform_low)
        self.lower_threshold_scale.pack(side=tk.TOP, padx=10, pady=10)

        # ->Create a Scale widget for the Maximum Threshold
        self.upper_threshold = tk.IntVar()
        self.upper_threshold_scale = tk.Scale(self.button_frame2, from_=0, to=255, orient=tk.HORIZONTAL, label="Upper Threshold Value", length = 150, variable=self.upper_threshold)
        self.upper_threshold_scale.bind("<ButtonRelease-1>", self.re_perform_high)
        self.upper_threshold_scale.pack(side=tk.TOP, padx=10, pady=10)     
        
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------       
        # Create a label to display the segmented image mask
        self.result_image_label1 = tk.Label(self.image_frame)
        self.result_image_label1.pack(side=tk.RIGHT)
        
        # Create a label to display the segmented image 
        self.result_image_label2 = tk.Label(self.image_frame)
        self.result_image_label2.pack(side=tk.RIGHT)
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------      
        # Section to pack all the tkinter frames
        
        # Pack all the frames
        self.image_frame.pack(side = tk.TOP, expand = True, fill = tk.BOTH)
        self.button_frame1.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
        self.button_frame2.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # Function to load images 
    def load_image(self):
        # Open a file selection dialog box to choose an image file
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        
        # Load the chosen image using PIL
        self.original_image = Image.open(file_path)
        
        # Resize the image to fit in the label
        width, height = self.original_image.size
        max_size = 300
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        self.original_image = self.original_image.resize((new_width, new_height))
        
        # Convert the image to Tkinter format and display it on the left side
        photo = ImageTk.PhotoImage(self.original_image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # Function to detect circles in the loaded image and the output image on the basis of the radius provided     
    def segmentation(self):
        
        # Copy the original loaded image
        image_copy = self.original_image.copy()
        
        # Convert the image to a numpy array 
        np_image = np.array(image_copy)
        
        # Convert the image from BGR to HSV color space
        hsv = cv2.cvtColor(np_image, cv2.COLOR_BGR2HSV)
        
        # Extract the H channel
        h_channel = hsv[:,:,0]
        
        # Define the range of colors to be segmented (in HSV color space)
        lower_range = int(self.lower_threshold.get())
        upper_range = int(self.upper_threshold.get())
        
        # Threshold the image to get only the specified range of colors
        mask = cv2.inRange(h_channel, lower_range, upper_range)
        
        # For displaying the output image ----------------->
        
        # Apply the mask to the original image to extract the segmented region
        result_image = cv2.bitwise_and(np_image, np_image, mask=mask)
        
        # Convert the image back to PIL format
        pil_image1 = Image.fromarray(result_image)
        
        # Resize the image to fit in the label
        width, height = self.original_image.size
        max_size = 300
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        pil_image1 = pil_image1.resize((new_width, new_height))
        
        # Convert the image to Tkinter format and display it on the right side
        photo1 = ImageTk.PhotoImage(pil_image1)
        self.result_image_label1.configure(image=photo1)
        self.result_image_label1.image = photo1
        
        # For displaying the mask -------------------------->
        
        # Convert the image back to PIL format
        pil_image2 = Image.fromarray(mask)
        
        # Resize the image to fit in the label
        width, height = self.original_image.size
        max_size = 300
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        pil_image2 = pil_image2.resize((new_width, new_height))
        
        # Convert the image to Tkinter format and display it on the right side
        photo2 = ImageTk.PhotoImage(pil_image2)
        self.result_image_label2.configure(image=photo2)
        self.result_image_label2.image = photo2
        
        
        
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # Supporter function to track the changes on minimum threshold tkinter scale and dynamically update the result image
    def re_perform_low(self, lower_threshold):
        self.segmentation()
    
    # Supporter function to track the changes on maximum threshold tkinter scale and dynamically update the result image    
    def re_perform_high(self, upper_threshold):
        self.segmentation()
        
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Instantiate a window from the class

if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("900x900")
    gui = ImageGUI(window)
    window.mainloop()