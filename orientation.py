"""
====================================
Filename:         orientation.py 
Author:              Joseph Farah 
Description:       Contains classes and methods for orientation of 
                    img files.
====================================
Notes
     
"""

class Point(object):

    def __init__(self, timestamp, fpath, slate, im, dng):

        self.timestamp = timestamp
        self.fpath = fpath
        self.dng = dng
        self.slate = slate
        self.im = im
        self.tag = self.fpath.split('/')[-1].split('.')[0]
        self.timestamp_old = timestamp

    def __sub__(self, other):
        diff = self.timestamp - other.timestamp
        return diff.seconds

    @staticmethod
    def get_tag(path):
        return path.split('/')[-1].split('.')[0]