"""
turns off prints
"""
import os
import sys


class HiddenPrints:
    """
    turns off prints
    """

    def __init__(self):
        """
        turns off prints
        """
        self._original_stdout = sys.stdout

    def __enter__(self):
        """
        turns off prints
        """
        sys.stdout = open(os.devnull, "w", encoding="utf8")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        turns off prints
        """
        sys.stdout.close()
        sys.stdout = self._original_stdout
