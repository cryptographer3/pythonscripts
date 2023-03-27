#A python based GUI Program for various Image processing techniques
#This Program supports histogram equalization, low pass filter, high pass filter and high boosting on images in spatial domain
#Author - cryptographer3

#Importing the required libraries

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import cv2

#Define a class for the GUI

class ImageGUI:
   
    def __init__(self, master):
       self.master = master
       self.master.title("Image GUI")
   
       # Create a frame for displaying the photos and center it
       self.image_frame = tk.Frame(self.master)
       
       # Create frame 1 for displaying image loading button
       self.button_frame1 = tk.Frame(self.master)
       
       # Create frame 2 for displaying image filter buttons
       self.button_frame2 = tk.Frame(self.master)
       
       # Create frame 3 for displaying image high boosting button
       self.button_frame3 = tk.Frame(self.master)
       
       # Create a "Load Image" button
       self.load_button = tk.Button(self.button_frame1, text="Load Image", command=self.load_image)
       self.load_button.pack(side=tk.TOP, padx=10, pady=10)
       # Create a label to display the chosen image
       self.image_label = tk.Label(self.image_frame)
       self.image_label.pack(side=tk.LEFT)
       
   
       # Create a Scale widget for the kernel size
       self.kernel_size_var = tk.IntVar()
       self.kernel_size_var.set(3)
       self.kernel_size_scale = tk.Scale(self.button_frame2, from_=1, to=31, orient=tk.HORIZONTAL, label="Kernel Size", variable=self.kernel_size_var)
       self.kernel_size_scale.pack(side=tk.RIGHT, padx=10, pady=10)
   
       # Create a Scale widget for the standard deviation
       self.sigma_var = tk.DoubleVar()
       self.sigma_var.set(2)
       self.sigma_scale = tk.Scale(self.button_frame2, from_=0.1, to=10.0, resolution=0.1, orient=tk.HORIZONTAL, label="Sigma", variable=self.sigma_var)
       self.sigma_scale.pack(side=tk.RIGHT, padx=10, pady=10)
   
       # Create a "Histogram Equalize" button
       self.histogram_button = tk.Button(self.button_frame2, text="Histogram Equalize", command=self.histogram_equalize)
       self.histogram_button.pack(side=tk.TOP, padx=10, pady=10)
   
       # Create a "Low Pass" button
       self.low_pass_button = tk.Button(self.button_frame2, text="Low Pass", command=self.low_pass_filter)
       self.low_pass_button.pack(side=tk.TOP, padx=10, pady=10)
    
       # Create a "High Pass" button
       self.high_pass_button = tk.Button(self.button_frame2, text="High Pass", command=self.high_pass_filter)
       self.high_pass_button.pack(side=tk.TOP, padx=10, pady=10)
       
       # Create a "High Boost" button
       self.high_pass_button = tk.Button(self.button_frame3, text="High Boost", command=self.high_boost_filter)
       self.high_pass_button.pack(side=tk.LEFT, padx=10, pady=10)
       
       # Create a Scale widget for the high boost factor
       self.boost_factor = tk.DoubleVar()
       self.boost_factor.set(1)
       self.sigma_scale = tk.Scale(self.button_frame3, from_=0.1, to=10.0, resolution=0.1, orient=tk.HORIZONTAL, label="Boost Factor", variable=self.boost_factor)
       self.sigma_scale.pack(side=tk.LEFT, padx=10, pady=10)
       
       # Create a label to display the filtered image
       self.result_image = tk.Label(self.image_frame)
       self.result_image.pack(side=tk.RIGHT)
       
       #Pack all the frames
       self.image_frame.pack(side = tk.TOP, expand = True, fill = tk.BOTH)
       self.button_frame1.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
       self.button_frame2.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
       self.button_frame3.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)

     

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
    
    
    #Function to histogram equalize the loaded image
    def histogram_equalize(self):
        # Convert the original image to grayscale
        grayscale_image = self.original_image.convert('L')
        
        # Perform histogram equalization using OpenCV
        np_image = np.array(grayscale_image)
        equalized_image = cv2.equalizeHist(np_image)
        
        # Convert the equalized image back to PIL format
        pil_image = Image.fromarray(equalized_image)
        
        # Resize the image to fit in the label
        width, height = pil_image.size
        max_size = 300
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        pil_image = pil_image.resize((new_width, new_height))
        
        # Convert the image to Tkinter format and display it on the right side
        photo = ImageTk.PhotoImage(pil_image)
        self.result_image.configure(image=photo)
        self.result_image.image = photo
        
        
    #Function to implement high pass filter on the loaded image in spatial domain
    def high_pass_filter(self):
        # Get the kernel size and sigma from the scale widgets
        ksize = 5
    
    
        # Convert the original image to grayscale
        grayscale_image = self.original_image.convert('L')
    
        # Convert the grayscale image to a numpy array
        np_image = np.array(grayscale_image)
    
        # Apply a Laplacian filter to the image
        filtered_image = cv2.Laplacian(np_image, cv2.CV_64F, ksize=ksize)
    
        # Normalize the filtered image to 0-255 range
        filtered_image = cv2.normalize(filtered_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
        # Convert the filtered image back to PIL format
        pil_image = Image.fromarray(filtered_image)
    
        # Resize the image to fit in the label
        width, height = pil_image.size
        max_size = 300
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        pil_image = pil_image.resize((new_width, new_height))
    
        # Convert the image to Tkinter format and display it on the right side
        photo = ImageTk.PhotoImage(pil_image)
        self.result_image.configure(image=photo)
        self.result_image.image = photo
        
    #Function to implement low pass filter on the loaded image in spatial domain    
    def low_pass_filter(self):
        # Get the kernel size and sigma from the scale widgets
        ksize = self.kernel_size_var.get()
        sigma = self.sigma_var.get()
    
        # Convert the original image to grayscale
        grayscale_image = self.original_image.convert('L')
    
        # Convert the grayscale image to a numpy array
        np_image = np.array(grayscale_image)
    
        # Apply a Gaussian filter to the image
        filtered_image = cv2.GaussianBlur(np_image, (ksize, ksize), sigma)
    
        # Convert the filtered image back to PIL format
        pil_image = Image.fromarray(filtered_image)
    
        # Resize the image to fit in the label
        width, height = pil_image.size
        max_size = 300
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        pil_image = pil_image.resize((new_width, new_height))
    
        # Convert the image to Tkinter format and display it on the right side
        photo = ImageTk.PhotoImage(pil_image)
        self.result_image.configure(image=photo)
        self.result_image.image = photo
  
    #Function to implement high boost filter on the loaded image 
    def high_boost_filter(self):
        
        #Temporary boost_factor
        boost_factor = self.boost_factor.get()
        
        # Convert the original image to grayscale
        grayscale_image = self.original_image.convert('L')
        
        # Convert the grayscale image to a numpy array
        np_image = np.array(grayscale_image)
        
        result_image = np_image.copy()
        #Apply High boost to the image
        for i in range(1,np_image.shape[0]-1):
            for j in range(1,np_image.shape[1]-1):
                blur_factor = (np_image[i-1, j-1] + np_image[i-1, j] - np_image[i-1, j+1] + np_image[i, j-1] + np_image[i, j] + np_image[i, j+1] + np_image[i+1, j+1] + np_image[i+1, j] + np_image[i+1, j+1])/9
                mask = boost_factor*np_image[i, j] - blur_factor
                result_image[i, j] = mask
                
        
        # Convert the filtered image back to PIL format
        pil_image = Image.fromarray(result_image)
        
        # Resize the image to fit in the label
        width, height = pil_image.size
        max_size = 300
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        pil_image = pil_image.resize((new_width, new_height))
        
        # Convert the image to Tkinter format and display it on the right side
        photo = ImageTk.PhotoImage(pil_image)
        self.result_image.configure(image=photo)
        self.result_image.image = photo
            
            
#Instantiate a window from the class
if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("600x600")
    gui = ImageGUI(window)
    window.mainloop()
