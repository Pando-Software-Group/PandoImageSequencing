class Point(object):
    """
    Object for manipulating and sequencing images taken on PPS route.
    """

    def __init__(self, timestamp, fpath: str, slate, im, dng: str):

        self.timestamp = timestamp
        """Timestamp corresponding to image."""
        self.fpath = fpath
        """Folderpath to JPG version of image."""
        self.dng = dng
        """Folderpath to DNG version of image."""
        self.slate = slate
        """Open or end slate or None."""
        self.im = im
        """Image contents."""
        self.tag = self.fpath.split('/')[-1].split('.')[0]
        """Tag containing information assigned by Friends of Pando."""
        self.timestamp_old = timestamp
        """Backup version of timestamp to preserve."""

    def __sub__(self, other):
        """
        Overwrite subtraction method to perform timestamp subtraction
        **Args**:
        * other (Point): additional Point object to perform delta.
        **Returns**:
        * delta (float): time delta between two Point objects in seconds.
        """

        diff = self.timestamp - other.timestamp
        return diff.seconds

    @staticmethod
    def get_tag(path: str):
        """
        Extract tag containing information assigned by Friends of Pando.
        **Args**:
        * path (str): filepath to image.
        **Returns**:
        * tag (str): tag of image.
        """

        return path.split('/')[-1].split('.')[0]