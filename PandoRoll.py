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





def locate_sun(image, radius=701, show=False):

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
        

## roll single image button ##
def roll_folder_manual(directory=None):

    ## select image
    os.system(f"mkdir {directory}/rolled/")
    for _im_fpath in tqdm(glob.glob(directory + "/*.jpg")):
    # _im_fpath = filedialog.askopenfilename()
        print(_im_fpath)

        # ## draw image ##
        im = plt.imread(_im_fpath)
        # plt.clf()
        # plt.imshow(im)
        # plt.setp(plt.gca(), autoscale_on=False)

        # _window_management_helper.tellme("Click twice on feature you would like to roll to middle.\nPress [ENTER] to continue.")

        # circle1 = plt.Circle([0, 0], 700, color='r', fill=False)
        # plt.gca().add_patch(circle1)

        # while True:

        #     if plt.waitforbuttonpress():
        #         break

        #     pts = np.asarray(plt.ginput(1, timeout=-1, show_clicks=True))
        #     _window_management_helper.tellme('Click twice on feature you would like to roll to middle.\nPress [ENTER] to continue.')

        #     circle1.remove()

        #     if len(pts) > 0:
        #         sun_coord = pts[0]

        #     circle1 = plt.Circle(sun_coord, 700, color='r', fill=False)
        #     plt.gca().add_patch(circle1)

        #     print(sun_coord)

        # plt.clf()
        # plt.cla()
        # plt.close('all')

        sun_coord, _ = locate_sun(im)

        rolled_im = np.roll(im, (0, -int(sun_coord[0])+int(7680/2), 0), axis=(0, 1, 2))
        print(rolled_im.shape)
        tag = _im_fpath.split('/')[-1]
        Image.fromarray(rolled_im).save(f"{directory}/rolled/{tag}")
        # plt.imshow(rolled_im)
        # plt.title("Rolled im, saved")
        # plt.show()
        print("Images aligned.")
        del im


