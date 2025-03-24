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
import exiftool
import glob
import shutil
import tkinter as tk
from typing import List
from tqdm import tqdm
from datetime import datetime
from tkinter import filedialog
from pathlib import Path
from point import Point



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

def reset_output_dir(output_dir: str):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.mkdir(output_dir)
    os.mkdir(f'{output_dir}/jpgs')
    os.mkdir(f'{output_dir}/dngs')

def get_config_filepath():
    return _window_management_helper.pick_file()

def fix_file_names(dir_names: List[str]):
    """
    Iterates through files in directories and replaces whitespace with underscores.

    **Args**:
        dir_names (list[str]): List of paths to directories containing files to rename

    **Returns**:
        None
    """
    for dir_name in dir_names:
        dir_path = Path(dir_name)

        if not dir_path.exists():
            bcolors.warning(f"Directory does not exist: {dir_name}")
            continue

        # Get all files in directory
        for file_path in dir_path.glob('*'):
            if file_path.is_file():
                # Get original filename
                old_name = file_path.name
                # Replace whitespace with underscore
                new_name = '_'.join(old_name.split())
                # Replace multiple underscores with single underscore
                while '__' in new_name:
                    new_name = new_name.replace('__', '_')

                # Only rename if name would change
                if old_name != new_name:
                    file_path.rename(dir_path / new_name)

def get_timestamp(file: str):
    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(file)
        modify_date_hms = metadata[0]['EXIF:ModifyDate'].split()[-1]
        return datetime.strptime(modify_date_hms,  '%H:%M:%S')

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

    fix_file_names([jpg_dir, dng_dir])

    dngs        = sorted(glob.glob(dng_dir+"/*.dng"))
    jpgs        = sorted(glob.glob(jpg_dir+"/*.jpg"))

    if len(jpgs) != len(dngs):
        bcolors.failure(f"Mismatch in number of files: {len(jpgs)} JPGs vs {len(dngs)} DNGs")
        return None

    for i, _im_fpath in enumerate(tqdm(jpgs)):
        try:
            ## locate corresponding DNG ##
            tag = Point.get_tag(_im_fpath)
            # _dng_path = next(dng for dng in dngs if dng.name == f"{tag}.dng")
            _dng_path = dng_dir + "/" + tag + ".dng"

            ## get corrupted timestamp ##
            timestamp = get_timestamp(dngs[i])

            ## check for end slate ##
            if 'end' in _im_fpath.lower():
                print(f"Found end slate at {timestamp}.")
                points.append(Point(timestamp, _im_fpath, 'end', None, _dng_path))
                end_index = i
                continue

            ## check for open slate ##
            if 'open' in _im_fpath.lower():
                print(f"Found open slate at {timestamp}.")
                points.append(Point(timestamp, _im_fpath, 'open', None, _dng_path))
                start_index = i
                continue

            points.append(Point(timestamp, _im_fpath, None, None, _dng_path))
        except IndexError:
            bcolors.failure(f"Failed to process file pair {i}: JPG exists but no matching DNG")
            continue

    return {'points': points, 'start': start_index, 'end': end_index}





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