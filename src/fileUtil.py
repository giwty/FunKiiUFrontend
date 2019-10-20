"""Helper utility for managing files"""

import shutil
import os
from logger import *


def delete_folder(path):
    """Delete folder and all contents inside."""
    shutil.rmtree(path, ignore_errors=True)

def list_files(directory):
    """Get a list of filename in a directory."""
    try:
        return os.listdir(directory)
    except Exception as e:
        log('Error listing files for directory "{}": '.format(directory) + repr(e))
        temp = []
        return temp

def copy_file(fsrc, ftgt, callback=None, length=16*1024):
    """Copy a file by chunks.Default is 16*1024."""
    with open(fsrc) as source:
        target = open(ftgt, "w")
        copied = 0
        while True:
            buf = source.read(length)
            if not buf:
                break
            target.write(buf)
            copied += len(buf)
            if callback:
                callback(copied)
           # print str((int((float(copied)) / (float(os.path.getsize(fsrc)))) * 100)) + "%"
        target.close()

def move_file(fsrc, fdst, callback=None, length=16*1024):
    with open(fsrc) as source:
        target = open(fdst, "w")
        copied = 0
        while True:
            buf = source.read(length)
            if not buf:
                break
            target.write(buf)
            copied += len(buf)
            if callback:
                callback(copied)
          #  print str((int((float(copied)) / (float(os.path.getsize(fsrc)))) * 100)) + "%"
        target.close()
        os.remove(fsrc)