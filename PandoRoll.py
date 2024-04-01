"""
====================================
Filename:         PandoRoll.py 
Author:              Joseph Farah 
Description:       Program to roll image or images to the same orientation
====================================
Notes   
    - Functionality: 
        - Roll single image to chosen orientation
        - Roll group of images to orientation based on changing feature
        - Roll group of images to orientation automatically based on sun position
"""

#------------- IMPORTS -------------#
import os 
import cv2
import glob
import matplotlib
import numpy as np
import tkinter as tk
from tqdm import tqdm
from PIL import Image
from tkinter import filedialog
import matplotlib.pyplot as plt
from PIL import ImageTk, Image


#------------- CLASSES -------------#
class _window_management_helper:
    '''
        Helper class to manage on screen text and operations.
    '''
    @staticmethod
    def clear():
 
        # for windows
        if os.name == 'nt':
            _ = os.system('cls')
     
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = os.system('clear')

    @staticmethod
    def pick_folder():
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askdirectory()

        return file_path

    @staticmethod
    def tellme(s):
        # print(s)
        plt.title(s, fontsize=10)
        plt.draw()


#------------- GLOBALS -------------#




#------------- FUNCTIONS -------------#
def locate_sun(image, radius=701, show=False):
    """
        Locate sun in image by blurring image and finding brightest spot.
        Physical obstructions in image may cause incorrect recovery.
    
        **Args**:
    
        * image (PIL.Image/cv2.Image/numpy.array): image object or pixel array
        * radius (int): size of blurring kernel
        * show (bool): show the extraction location on the image
    
        **Returns**:
    
        * maxLoc (tuple): estimated location of Sun
        * radius (int): size of blurring kernel used (legacy)
    
    """
     
    

    print(f"Locating sun in image.")
    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # perform a naive attempt to find the (x, y) coordinates of
    # the area of the image with the largest intensity value
    # apply a Gaussian blur to the image then find the brightest
    # region
    gray = cv2.GaussianBlur(gray, (radius, radius), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

    if show:
        plt.imshow(orig[:,:,::-1])
        circle1 = plt.Circle(maxLoc, radius, color='r', fill=False)
        plt.gca().add_patch(circle1)
        plt.show()

    return maxLoc, radius
        

def roll_folder_manual(directory: str=None):
    """
        Roll list of images to have brightest spot at center
    
        **Args**:
    
        * directory (str): path to JPGs that need to be centered.   
    
        **Returns**:
    
        * None
    
    """
     
    

    ## select image
    os.system(f"mkdir {directory}/rolled/")
    for _im_fpath in tqdm(glob.glob(directory + "/*.jpg")):
    # _im_fpath = filedialog.askopenfilename()
        print(_im_fpath)

        im = plt.imread(_im_fpath)

        sun_coord, _ = locate_sun(im)

        rolled_im = np.roll(im, (0, -int(sun_coord[0])+int(7680/2), 0), axis=(0, 1, 2))
        print(rolled_im.shape)
        tag = _im_fpath.split('/')[-1]
        Image.fromarray(rolled_im).save(f"{directory}/rolled/{tag}")
        print("Images aligned.")
        del im


