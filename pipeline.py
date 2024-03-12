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
import file_io
import subprocess
import numpy as np
import typing_filter
from tqdm import tqdm 
import datetime as dt
from datetime import datetime
import matplotlib.pyplot as plt


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
        self.options = ['Quit', 'Input']
        self.descriptions = ['Exit the pipeline and return to the command line.', 'Choose folder location of input images.']
        self.options_dict = {'Quit':self.__quit, 'Input':self.__choose_input_fpath}

        self.settings = {
            'Pando':True,
            'im_fpath':None,
            'output_dir':None,
        }


    def get_options(self):
        return self.options

    def get_descriptions(self):
        return self.descriptions

    def get_switch(self, choice):
        return self.options_dict[choice]

    def __quit(self):
        sys.exit(0)

    def __choose_input_fpath(self):
        return file_io.get_image_dir_fpath()




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

    main()



    


#------------- SWITCHBOARD -------------#
if __name__ == '__main__':
    main(intro=True)