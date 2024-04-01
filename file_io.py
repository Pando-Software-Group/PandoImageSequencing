"""
====================================
Filename:         file_io.py 
Author:              Joseph Farah 
Description:       Handles file input and output for pipeline.
====================================
Notes
     
"""
 
#------------- IMPORTS -------------#
import os
import glob
import subprocess
import tkinter as tk
from tqdm import tqdm
from datetime import datetime
from tkinter import filedialog

from orientation import Point



#------------- GLOBAL SETTINGS -------------#


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
    def pick_file():
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        return file_path

    @staticmethod
    def tellme(s):
        # print(s)
        plt.title(s, fontsize=10)
        plt.draw()



def get_image_dir_fpath():
    """
        Gets directory containing unsequenced images.       
    
        **Args**:
            None
    
         **Returns**:
            _fpath (str): folderpath  containing unsequenced images
    
    """


    return _window_management_helper.pick_folder()


def get_config_filepath():
    return _window_management_helper.pick_file()


def load_points(jpg_dir, dng_dir):
    """
        Loads JPGs from a directory, converts to points,
        and links to DNGs. 

        **Args**:
            jpg_dir (str): folderpath to directory containing JPGs
            dng_dir (str): folderpath to directory containing DNGs

         **Returns**:
            loaded_obj (dict): dictionary containing start/end 
            index and orientation.Point objects

    """
    if jpg_dir is None or dng_dir is None: 
        bcolors.failure("JPG_DIR or DNG_DIR is none. Please make sure folderpaths have been assigned for both.")
        input("\n\n>>>Press enter to return to the main menu.")
        return

    points      = []
    start_index = 0
    end_index   = 0

    dngs        = sorted(glob.glob(dng_dir+"/*.dng"))

    for i, _im_fpath in enumerate(tqdm(sorted(glob.glob(jpg_dir+"/*.jpg")))):

        ## locate corresponding DNG ##
        tag = Point.get_tag(_im_fpath)
        _dng_path = dng_dir + "/" + tag + ".dng"

        ## get corrupted timestamp ##
        timestamp = subprocess.check_output(f'exiftool -v "{dngs[i]}" | grep ModifyDate', shell=True).decode("utf-8").split('15)')[-1].split('\n')[0].split('=')[-1].split(' ')[-1]

        timestamp = datetime.strptime(timestamp,  '%H:%M:%S')

        ## check for end slate ##
        if 'end slate' in _im_fpath:
            print("Found end slate.")
            print(timestamp)
            points.append(Point(timestamp, _im_fpath, 'end', None, _dng_path))
            end_index = i
            continue

        ## check for open slate ##
        if 'open slate' in _im_fpath:
            print("Found open slate.")
            print(timestamp)
            points.append(Point(timestamp, _im_fpath, 'open', None, _dng_path))
            start_index = i
            continue

        points.append(Point(timestamp, _im_fpath, None, None, _dng_path))

    return {'points':points, 'start':start_index, 'end':end_index}





#------------- FUNCTIONS -------------#
def main():
    """
    Main function execution.

    **Args**:
        None

     **Returns**:
        None
    
    """

    pass


if __name__ == '__main__':
    main()