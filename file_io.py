"""
====================================
Filename:         file_io.py 
Author:           Joseph Farah 
Description:      Handles file input and output for pipeline.
====================================
Notes
     
"""
 
#------------- IMPORTS -------------#
import os
import exiftool
import glob
import shutil
import tkinter as tk
import traceback
import matplotlib.pyplot as plt
import re
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
        # 'nt' for windows, 'posix' for mac and linux
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def pick_folder():
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askdirectory()
        return os.path.normpath(file_path)

    @staticmethod
    def pick_file():
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        return os.path.normpath(file_path)

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


def sanitize_filename(filepath):
    """
    Removes any characters from the new file path that seem to be tripping up Windows in shutil.copy2
    
    """
    # Convert filepath to a Path object
    path = Path(filepath)
    
    # Keep the drive and parent directory intact
    drive = path.drive  # Preserve C: or other drive letters
    parent = path.parent  # Preserve the parent directories
    filename = path.name  # Isolate the filename
    
    # Sanitize only the filename
    sanitized_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Reconstruct the full path
    return Path(drive) / parent / sanitized_filename


def write_points(points: List[Point], output_path: str):
    """
    Writes points to output directory.

    **Args**:
        points (list[Point]): list of Point objects
        output_path (str): path to output directory

    **Returns**:
        None
    """
    
    reset_output_dir(output_path)

    """ for p, point in enumerate(tqdm(points)):
        dst_jpg = sanitize_filename(Path(output_path) / 'jpgs' / f"{p}_{point.tag}_new-time={str(point.timestamp).replace(' ', '_')}.jpg")
        dst_dng = sanitize_filename(Path(output_path) / 'dngs' / f"{p}_{point.tag}_new-time={str(point.timestamp).replace(' ', '_')}.dng")

        try:
            shutil.copy2(point.fpath, dst_jpg)
            shutil.copy2(point.dng, dst_dng)
        except Exception as e:
            print("An error occurred during file copy:")
            print(f"Errory type: {type(e).__name__}")
            print(f"Error message: {e}")
            print("Detailed traceback:")
            print(traceback.format_exc())
 """
    for p, point in enumerate(tqdm(points)):
        dst_jpg = sanitize_filename(Path(output_path) / 'jpgs' / f"{p}_{point.tag}_new-time={str(point.timestamp).replace(' ', '_')}.jpg")
        dst_dng = sanitize_filename(Path(output_path) / 'dngs' / f"{p}_{point.tag}_new-time={str(point.timestamp).replace(' ', '_')}.dng")

        """ print(f"src_jpg is now {point.fpath}")
        print(f"dst_jpg is now {dst_jpg}")
        print(f"src_dng is now {point.dng}")
        print(f"dst_dng is now {dst_dng}")
        print(f"About to try copy operation") """
        try:
            shutil.copy2(point.fpath, str(dst_jpg))  # Ensure dst is a string for shutil
            shutil.copy2(point.dng, str(dst_dng))
            print("Copy appears to have succeeded")
        except Exception as e:
            print("An error occurred during file copy:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {e}")
            print("Detailed traceback:")
            print(traceback.format_exc())

def reset_output_dir(output_dir: str):
    output_path = Path(output_dir)
    if output_path.exists():
        shutil.rmtree(output_path)

    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "jpgs").mkdir(parents=True, exist_ok=True)
    (output_path / "dngs").mkdir(parents=True, exist_ok=True)

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
        try:
            dir_path = Path(dir_name).resolve()  # Get absolute path
            if not dir_path.exists():
                bcolors.warning(f"Directory does not exist: {dir_name}")
                continue

            for file_path in dir_path.glob('*.[dDjJ][nNpP][gG]'):
                if file_path.is_file():
                    try:
                        old_name = file_path.name
                        # Remove invalid characters for all platforms
                        new_name = ''.join(c for c in old_name if c.isalnum() or c in '._- ')
                        new_name = '_'.join(new_name.split())
                        while '__' in new_name:
                            new_name = new_name.replace('__', '_')

                        if old_name != new_name:
                            new_path = dir_path / new_name
                            if len(str(new_path)) < 260:  # Windows MAX_PATH
                                file_path.rename(new_path)
                            else:
                                bcolors.warning(f"Path too long for: {new_path}")
                    except OSError as e:
                        bcolors.failure(f"Failed to rename {file_path}: {e}")
        except Exception as e:
            bcolors.failure(f"Error processing directory {dir_name}: {e}")

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

    points = []
    start_index = end_index = 0

    fix_file_names([jpg_dir, dng_dir])

    dngs = sorted(glob.glob(str(Path(dng_dir)/"*.[dD][nN][gG]")))
    jpgs = sorted(glob.glob(str(Path(jpg_dir)/"*.[jJ][pP][gG]")))

    if len(jpgs) != len(dngs):
        bcolors.failure(f"Mismatch in number of files: {len(jpgs)} JPGs vs {len(dngs)} DNGs")
        input("\n\n>>>Press enter to return to the main menu.")
        return

    # need to pass total to fix rendering bug when using tqdm with zip
    for i, (jpg_path, dng_path) in enumerate(tqdm(zip(jpgs, dngs), total=len(jpgs))):
        path_obj = Path(jpg_path)
        try:
            ## get corrupted timestamp ##
            timestamp = get_timestamp(dngs[i])

            ## check for open slate ##
            if 'open' in path_obj.stem.lower():
                print(f"Found open slate at {timestamp}.")
                points.append(Point(timestamp, jpg_path, dng_path, 'open'))
                start_index = i
            ## check for end slate ##
            elif 'end' in path_obj.stem.lower():
                print(f"Found end slate at {timestamp}.")
                points.append(Point(timestamp, jpg_path, dng_path, 'end'))
                end_index = i
            else:
                points.append(Point(timestamp, jpg_path, dng_path, None))

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