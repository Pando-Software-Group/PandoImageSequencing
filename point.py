from pathlib import Path
from datetime import datetime

class Point:
    """
    Object for manipulating and sequencing images taken on PPS route.
    """

    def __init__(self, timestamp: datetime, fpath: str, dng: str, slate: str | None, im = None):
        self.timestamp = timestamp
        """Timestamp corresponding to image."""
        self.timestamp_old = timestamp
        """Backup version of timestamp to preserve."""
        self.fpath = fpath
        """Folderpath to JPG version of image."""
        self.dng = dng
        """Folderpath to DNG version of image."""
        self.slate = slate
        """'open' or 'end' slate or None."""
        self.im = im
        """Image contents."""

    @property
    def tag(self):
        """
        Tag containing information assigned by Friends of Pando.
        """
        return Path(self.fpath).stem

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
