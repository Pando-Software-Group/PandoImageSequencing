"""
====================================
Filename:         pipeline.py 
Author:              Joseph Farah 
Description:       Main pipeline aggregate.
====================================
Notes
    - Offers options to user, saves input and settings, and calls
    on external modules. 
"""

#------------- IMPORTS -------------#
import os
import sys
import glob 
import copy
import subprocess
import numpy as np
import typing_filter
from tqdm import tqdm 
import datetime as dt
from datetime import datetime
import matplotlib.pyplot as plt

import file_io
from orientation import Point


#------------- GLOBAL SETTINGS -------------#
RedirectorObject = None


#------------- CLASSES -------------#
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def warning(message):
        print (bcolors.WARNING + "[" + message + "]" + bcolors.ENDC)

    @staticmethod
    def success(message):
        print (bcolors.OKGREEN + "[" + message + "]" + bcolors.ENDC)

    @staticmethod
    def failure(message):
        print (bcolors.FAIL + "[" + message + "]" + bcolors.ENDC)


class Redirector(object):

    def __init__(self):
        self.options = [
            'Quit', 
            'View configuration',
            'Input JPG',
            'Input DNG',
            'Load images',
        ]
        self.descriptions = [
            'Exit the pipeline and return to the command line.', 
            'View configuration settings.', 
            'Choose folder location of input JPGs.',
            'Choose folder location of input DNGs.',
            'Load all JPGs, link to corresponding DNG.',
        ]
        self.options_dict = {
            'Quit':self.__quit, 
            'View configuration':self.__print_settings, 
            'Input JPG':self.__choose_input_fpath_jpg,
            'Input DNG':self.__choose_input_fpath_dng,
            'Load images':self.__load_images,
        }

        self.settings = {
            'Pando':True,
            'im_fpath_JPG':None,
            'im_fpath_DNG':None,
            'output_dir':None,
            'start_index':None,
            'end_index':None,
            'points':None
        }


    def save_config(self):
        with open("config.pando", "w") as f:
            f.write(str(self.settings))

    def __load_config(self):
        input_fpath = file_io.get_image_dir_fpath()
        with open(input_fpath, "r") as f:
            self.settings = eval(f.read())

    def get_options(self):
        return self.options

    def get_descriptions(self):
        return self.descriptions

    def get_switch(self, choice):
        return self.options_dict[choice]

    def __quit(self):
        sys.exit(0)

    def __print_settings(self):
        for key in list(self.settings.keys()):
            print(f"{key}: {self.settings[key]}")
        input("\n\n\nPress any key to return to the menu.")

    def __choose_input_fpath_jpg(self):
        input_fpath = file_io.get_image_dir_fpath()
        self.settings['im_fpath_JPG'] = input_fpath
        input(f"Loaded {input_fpath}. Press any key to continue.")
        return input_fpath

    def __choose_input_fpath_dng(self):
        input_fpath = file_io.get_image_dir_fpath()
        self.settings['im_fpath_DNG'] = input_fpath
        input(f"Loaded {input_fpath}. Press any key to continue.")
        return input_fpath

    def __load_images(self):
        loaded_object = file_io.load_points(self.settings['im_fpath_JPG'], self.settings['im_fpath_DNG'])
        self.settings['start_index'] = loaded_object['start_index']
        self.settings['end_index'] = loaded_object['end_index']
        self.settings['points'] = loaded_object['points']
        input("Loaded images. Press any key to continue.")




#------------- FUNCTIONS -------------#
def main(intro=False):
    """
        Main function execution.
    
        Args:
            intro (bool): flag to run intro
    
        Returns:
            none (none): none
    
    """

    global RedirectorObject

    ## initialize ##
    if intro:
        file_io._window_management_helper.clear()
        bcolors.success("Welcome to the Pando Image Sequencing pipeline. Press [ENTER] to continue.")
        input("\n>>>")

        ## create RedirectorObject for settings and choices ##
        RedirectorObject = Redirector()


    choice = typing_filter.launch(RedirectorObject.get_options(), RedirectorObject.get_descriptions())

    RedirectorObject.get_switch(choice)()
    RedirectorObject.save_config()

    main()



    


#------------- SWITCHBOARD -------------#
if __name__ == '__main__':
    main(intro=True)