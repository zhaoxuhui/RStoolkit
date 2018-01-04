# coding=utf-8
import os
import platform


def getSeparator():
    """
    Get the separator for different systems.
    
    :return: String,the separator.e.g. "/" on linux.
    """
    sysstr = platform.system()
    if (sysstr == "Windows"):
        separator = "\\"
    elif (sysstr == "Linux"):
        separator = "/"
    else:
        separator = "/"
    return separator


def findAllFiles(root_dir, file_type):
    """Find the all the files you want in a certain directory.
    
    :param root_dir: String,directory you want to search,e.g."E:/images/"
    :param file_type: String,file type,e.g. "jpg","png","tif"...
    :return: list,returns A list contains files' paths
    
    Usage:
     findAllFiles("E:/images/", "jpg")
    It will return a list of jpg image paths.
    """
    paths = []
    for parent, dirname, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(file_type):
                paths.append(parent + filename)
    return paths
