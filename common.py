# coding=utf-8
import os
import platform
import shutil


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


def copyFilesTo(paths, dstPath):
    """
    A function for copying files to certain dir.

    :param paths: A list of file paths.
    :param dstPath: A string,the destination dir for files.
    :return: Nothing.
    """
    for i in range(len(paths)):
        shutil.copy(paths[i], dstPath)
        print (i * 1.0 / len(paths)) * 100, "% finished."


def gatherDifferentTypeFiles(root_dir, file_types):
    """
    A function for gather different types of files at one time.
    
    :param root_dir: String,directory you want to search,e.g."E:/images/"
    :param file_types: A list contains different file types.Each item is a string.
    :return: A list of file paths.
    """
    paths = []
    for parent, dirname, filenames in os.walk(root_dir):
        for filename in filenames:
            for item in file_types:
                if filename.endswith(item):
                    paths.append(parent + getSeparator() + filename)
                    continue
    print paths.__len__(), " files loaded."
    return paths


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
                paths.append(parent + getSeparator() + filename)
    return paths
