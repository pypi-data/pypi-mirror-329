"""
stuff.py functions and such common to threefive.
"""

from sys import stderr


def print2(stuff=b""):
    """
    print2 prints to 2 aka stderr.
    """
    print(stuff, file=stderr, flush=True)


def dbl_split(data, mark):
    """
    dbl_split split bytes on mark twice
    return mark + split bytes on mark twice.
    """
    return mark + data.split(mark)[-1].split(mark)[-1]
