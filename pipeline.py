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
import dill
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
import PandoRoll
from orientation import Point, statistical_sequence, suggest_reordering


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
            'Load configuration',
            'View configuration',
            'Input JPG',
            'Input DNG',
            'Output dir',
            'Load images',
            'Statistical sort',
            'PandoRoll',
            'Mark bad images',
        ]
        self.descriptions = [
            'Exit the pipeline and return to the command line.', 
            'Load previous session configuration file to pick up where you left off.', 
            'View configuration settings.', 
            'Choose folder location of input JPGs.',
            'Choose folder location of input DNGs.',
            'Choose folder location to output ordered images.',
            'Load all JPGs, link to corresponding DNG.',
            'Perform initial sort of images using statistical inference.',
            'Roll JPGS so all images have sun centered.',
            'Mark images in sort as incorrectly sequenced and re-order.'
        ]
        self.options_dict = {
            'Quit':self.__quit, 
            'Load configuration':self.__load_config, 
            'View configuration':self.__print_settings, 
            'Input JPG':self.__choose_input_fpath_jpg,
            'Input DNG':self.__choose_input_fpath_dng,
            'Output dir':self.__choose_output_fpath_dir,
            'Load images':self.__load_images,
            'Statistical sort':self.__stat_sort,
            'PandoRoll':self.__center_sun,
            'Mark bad images':self.__mark_bad,
        }

        self.settings = {
            'Pando':True,
            'im_fpath_JPG':None,
            'im_fpath_DNG':None,
            'output_dir':None,
            'start_index':None,
            'end_index':None,
            'points':None,
            'fh_bin':None,
            'sh_bin':None,
            'bad_images':None,
            'final_list':None,
        }


    def save_config(self):
        with open("config.pando", "wb") as f:
            dill.dump(self.settings, f)

    def __load_config(self):
        input_fpath = file_io.get_config_filepath()
        with open(input_fpath, "rb") as f:
            self.settings = dill.load(f)
        print("\n\nSettings loaded. ")
        self.__print_settings()

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

    def __choose_output_fpath_dir(self):
        output_fpath = file_io.get_image_dir_fpath()
        self.settings['output_dir'] = output_fpath
        os.system(f"rm -rf {output_fpath}")
        os.system(f"mkdir {output_fpath}")
        os.system(f"mkdir {output_fpath}/jpgs/")
        os.system(f"mkdir {output_fpath}/dngs/")
        input(f"Created new directory at {output_fpath}. Press any key to continue.")
        return output_fpath

    def __load_images(self):
        loaded_object = file_io.load_points(self.settings['im_fpath_JPG'], self.settings['im_fpath_DNG'])
        self.settings['start_index'] = loaded_object['start']
        self.settings['end_index'] = loaded_object['end']
        self.settings['points'] = loaded_object['points']
        input("Loaded images. Press any key to continue.")

    def __stat_sort(self):
        first_half_bin, second_half_bin, new_points, diffs_combined_mean = statistical_sequence(self.settings['points'], self.settings['start_index'], self.settings['end_index'], self.settings['output_dir'])

        self.settings['fh_bin'] = first_half_bin
        self.settings['sh_bin'] = second_half_bin
        self.settings['final_list'] = new_points
        self.settings['diffs_combined_mean'] = diffs_combined_mean

    def __center_sun(self):
        PandoRoll.roll_folder_manual(directory=f"{self.settings['output_dir']}/jpgs/")


    def __mark_bad(self):
        first_half_bin, second_half_bin, new_points, bad_images = suggest_reordering(self.settings['points'], self.settings['fh_bin'], self.settings['sh_bin'], self.settings['output_dir'], self.settings['start_index'], self.settings['end_index'], self.settings['diffs_combined_mean'])

        self.settings['fh_bin'] = first_half_bin
        self.settings['sh_bin'] = second_half_bin
        self.settings['final_list'] = new_points
        self.settings['bad_images'] = bad_images




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