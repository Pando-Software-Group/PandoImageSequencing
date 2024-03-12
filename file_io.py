"""
====================================
Filename:         file_io.py 
Author:              Joseph Farah 
Description:       Handles file input and output for pipeline.
====================================
Notes
     
"""
 
#------------- IMPORTS -------------#
from tkinter import filedialog



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
    def tellme(s):
        # print(s)
        plt.title(s, fontsize=10)
        plt.draw()



def get_image_dir_fpath():
    """
        Gets directory containing unsequenced images.       
    
        Args:
            none (none): none
    
        Returns:
            _fpath (str): folderpath  containing unsequenced images
    
    """


    return _window_management_helper.pick_folder()
    



#------------- FUNCTIONS -------------#
def main():
    """
    Main function execution.

    Args:
        none (none): none

    Returns:
        none (none): none
    
    """

    pass


if __name__ == '__main__':
    main()