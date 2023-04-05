# A GUI program aimed at performing edge detection in images. Also supports circle detection.
# Author - cryptographer3

# Three edge detection techniques have been used in this program - Canny, Sobel and Laplacian

# The role of the edge detection thresholds is to aid the Canny algorithm in hysteresis procedure
# Minimum threshold - resolving Weak edges connected to strong edges
# Maximum threshold - resolving Strong edges

# The circle is detected by using Hough Transform algorithm. It depends on Max_threshold and radius as input

# After using the circle detection using detect circles button, please press load image button
# again to refresh the loaded as well as result image and clear of the circles from previous iteration

#Importing the required libraries

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np 
import cv2
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Defining a class, ImageGUI, to facilitate the GUI program with required functionalities

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

        # Create frame 2 for displaying algorithms for Edge detection
        self.button_frame2 = tk.Frame(self.master)

        # Create frame 3 for displaying scale widgets for changing certain parameters
        self.button_frame3 = tk.Frame(self.master)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------       
        # Section to handle load image button and loaded image label display
        
        # Create a "Load Image" button
        self.load_button = tk.Button(self.button_frame1, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.TOP, padx=10, pady=10)
        # Create a label to display the chosen image
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(side=tk.LEFT)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------     
        # Section to handle operation buttons
        
        # Create a drop down menu to display the algorithms for edge detection
        self.options = ["Canny", "Sobel", "Laplacian"]
        self.options_var = tk.StringVar()
        self.options_var.set(self.options[0])
        self.options_menu = tk.OptionMenu(self.button_frame2, self.options_var, *self.options)
        self.options_menu.pack(side=tk.TOP, padx=10, pady=10)

        # Create a "Detect Edges" button
        self.detect_button = tk.Button(self.button_frame2, text="Detect Edges", command=self.detect_edges)
        self.detect_button.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create a "Detect Circles" button
        self.detect_circles_button = tk.Button(self.button_frame2, text="Detect Circles", command=self.detect_circles)
        self.detect_circles_button.pack(side=tk.TOP, padx=10, pady=10)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
        # Section for input parameters handling
        
        # ->Create a Scale widget for the Minimum Threshold
        self.min_threshold = tk.IntVar()
        self.min_threshold.set(50)
        self.min_threshold_scale = tk.Scale(self.button_frame3, from_=1, to=1000, orient=tk.HORIZONTAL, label="Minimum Threshold Value", length = 150, variable=self.min_threshold)
        self.min_threshold_scale.bind("<ButtonRelease-1>", self.re_perform_min)
        self.min_threshold_scale.pack(side=tk.TOP, padx=10, pady=10)

        # ->Create a Scale widget for the Maximum Threshold
        self.max_threshold = tk.IntVar()
        self.max_threshold.set(100)
        self.max_threshold_scale = tk.Scale(self.button_frame3, from_=1, to=1000, orient=tk.HORIZONTAL, label="Maximum Threshold Value", length = 150, variable=self.max_threshold)
        self.max_threshold_scale.bind("<ButtonRelease-1>", self.re_perform_max)
        self.max_threshold_scale.pack(side=tk.TOP, padx=10, pady=10)

        # ->Create a Scale widget for the Approximate Radius
        self.app_radius = tk.DoubleVar()
        self.app_radius.set(10)
        self.app_radius_scale = tk.Scale(self.button_frame3, from_=1, to=1000, resolution=0.1, orient=tk.HORIZONTAL, label="Approximate radius", length = 150, variable=self.app_radius)
        self.app_radius_scale.pack(side=tk.TOP, padx=10, pady=10)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------       
        # Create a label to display the edge-detected image
        self.result_image = tk.Label(self.image_frame)
        self.result_image.pack(side=tk.RIGHT)
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------      
        # Section to pack all the tkinter frames
        
        # Pack all the frames
        self.image_frame.pack(side = tk.TOP, expand = True, fill = tk.BOTH)
        self.button_frame1.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
        self.button_frame2.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
        self.button_frame3.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)

     
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
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
    # Function to detect edges in the image
    def detect_edges(self):
        option = self.options_var.get()
        
        # Convert the original image to grayscale
        grayscale_image = self.original_image.convert('L')
    
        # Convert the grayscale image to a numpy array
        np_image = np.array(grayscale_image)
        
        if option == "Canny":
            edges = cv2.Canny(np_image, self.min_threshold.get(), self.max_threshold.get())
        elif option == "Sobel":
            sobelx = cv2.Sobel(np_image, cv2.CV_64F, 1, 0, ksize=5)
            sobely = cv2.Sobel(np_image, cv2.CV_64F, 0, 1, ksize=5)
            edges = cv2.bitwise_or(sobelx, sobely)
        elif option == "Laplacian":
            edges = cv2.Laplacian(np_image, cv2.CV_64F)

        # Convert the equalized image back to PIL format
        self.pil_image = Image.fromarray(edges)
        
        # Resize the image to fit in the label
        width, height = self.pil_image.size
        max_size = 300
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        self.pil_image = self.pil_image.resize((new_width, new_height))
        
        # Convert the image to Tkinter format and display it on the right side
        photo = ImageTk.PhotoImage(self.pil_image)
        self.result_image.configure(image=photo)
        self.result_image.image = photo

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Supporter function to track the changes on minimum threshold tkinter scale and dynamically update the result image
    def re_perform_min(self, min_threshold):
        self.detect_edges()
    
    # Supporter function to track the changes on maximum threshold tkinter scale and dynamically update the result image    
    def re_perform_max(self, max_threshold):
        self.detect_edges()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Function to detect circles in the loaded image and the output image on the basis of the radius provided     
    def detect_circles(self):
        # Convert the original image to grayscale
        grayscale_image = self.original_image.convert('L')
    
        # Convert the grayscale image to a numpy array
        np_image = np.array(grayscale_image)
        
        # Detect circles using Hough circle transform
        circles = cv2.HoughCircles(np_image, cv2.HOUGH_GRADIENT, dp=1, minDist=int(self.app_radius.get())+1, param1=int(self.max_threshold.get()), minRadius=int(self.app_radius.get()))
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            self.display_circles(circles)
    
    # Function to display circles over the loaded image and the output image
    def display_circles(self, circles):
        # Fetch the original loaded and result images
        img_loaded = np.asarray(self.original_image)
        img_result = np.asarray(self.pil_image)
        
        # Overlay circles on both
        for circle in circles:
            x, y, radius = circle
            img_loaded = cv2.circle(img_loaded, (x, y), radius, (255, 0, 0), 3)
            img_result = cv2.circle(img_result, (x, y), radius, (255, 0, 0), 3)
        
        # Convert the image to Tkinter format and display it on the left side
        img_loaded = Image.fromarray(img_loaded)
        photo1 = ImageTk.PhotoImage(img_loaded)
        self.image_label.configure(image=photo1)
        self.image_label.image = photo1
        
        # Convert the image to Tkinter format and display it on the right side
        img_result = Image.fromarray(img_result)
        photo2 = ImageTk.PhotoImage(img_result)
        self.result_image.configure(image=photo2)
        self.result_image.image = photo2
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Instantiate a window from the class
if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("600x600")
    gui = ImageGUI(window)
    window.mainloop()
