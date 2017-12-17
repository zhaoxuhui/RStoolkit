# coding=utf-8
import math

import cv2
from gdalconst import *
from osgeo import gdal

import common


def convertBit(image_path, out_bit_depth, out_band_sequence, isVisuable=True, showInfo=True):
    """
    A function for convert different image bit depth.
    
    :param image_path: String,image path,e.g. "E:/images/test.tif"
    :param out_bit_depth: Int,bit depth for output image.e.g. 8
    :param out_band_sequence: String,format "a,b,c",separated by ",".abc means band index,start from 0.e.g."2,1,0"
    :param isVisuable: Boolean,True as default.
    
                        True:The pixel value is not the right value for the bit depth you choose.It is calculated in 8-bit or 16-bit to let you see as it is right.
                        
                        False:The pixel value is the right value for the bit depth.But you may see the iamge as a black one or a white one.Beacuse OpenCV can only save images in 8-bit or 16-bit.As a 1-bit image,the pixel value will only be 0 or 1.And it will be saved in 8-bit,which has a range [0,255].So the image will looks like a whole black one.
    :param showInfo: Boolean,True as default.Whether to show information during processing.
    :return: Nothing.But the output image will be saved in the same dictionary.
    
    Usage:
     convertBit("E:/test/001.tif", 8, "2,1,0")
    """
    name = image_path.split(common.getSeparator())[-1]
    root = image_path.split(name)[0]
    outputBitNum = out_bit_depth
    output_bands = out_band_sequence

    bands = []
    maxNums = []
    band_data = []

    dataset = gdal.Open(root + name, GA_ReadOnly)

    if showInfo:
        print 'Image Info:'
        print 'Image Type:', dataset.GetDriver().ShortName
        print 'Image Description:', dataset.GetDescription()
        print 'Image Bands:', dataset.RasterCount
        print "\n"

    for i in range(dataset.RasterCount):
        bands.append(dataset.GetRasterBand(i + 1))

    if showInfo:
        for i in range(dataset.RasterCount):
            print "Band", (i + 1).__str__(), ":"
            print "Width:", bands[i].XSize
            print "Height:", bands[i].YSize
            print 'Data type:', bands[i].DataType
            print 'Max&Min:', bands[i].ComputeRasterMinMax()
            print "-------------------------------"

    maxNums.append(bands[i].ComputeRasterMinMax()[1])

    inputBitNum = int(math.ceil(math.log(max(maxNums), 2)))
    if showInfo:
        print "Bit depth of input image：", inputBitNum

    for i in range(dataset.RasterCount):
        band_data.append(bands[i].ReadAsArray(0, 0, bands[i].XSize, bands[i].YSize))

    if isVisuable is True:
        # convert image to visuable bit depth in 8bit or 16bit,not the right real pixel value
        if int(outputBitNum) < int(inputBitNum):
            print "#######"
            if outputBitNum <= 8:
                param = int(pow(2, inputBitNum) / pow(2, int(outputBitNum)))
                for i in range(dataset.RasterCount):
                    band_data[i] = band_data[i] / param
                # convert to visiable 8-bit
                for i in range(dataset.RasterCount):
                    band_data[i] = band_data[i] * int(255 / (pow(2, int(outputBitNum)) - 1))
            elif int(outputBitNum > 8):
                param = int(pow(2, int(inputBitNum)) / pow(2, outputBitNum))
                for i in range(dataset.RasterCount):
                    band_data[i] = band_data[i] / param
                # convert to visiable 16-bit
                for i in range(dataset.RasterCount):
                    band_data[i] = band_data[i] * int(65535 / (pow(2, int(outputBitNum)) - 1))
        elif int(outputBitNum) > int(inputBitNum):
            print "~~~~~~~"
            param = int(pow(2, int(outputBitNum)) / pow(2, inputBitNum))
            for i in range(dataset.RasterCount):
                band_data[i] = band_data[i] * param
            if int(outputBitNum) <= 8:
                print
                # convert to visiable 8-bit
                for i in range(dataset.RasterCount):
                    band_data[i] = band_data[i] * int(255 / (pow(2, int(outputBitNum)) - 1))
            elif int(outputBitNum > 8):
                print
                # convert to visiable 16-bit
                for i in range(dataset.RasterCount):
                    band_data[i] = band_data[i] * int(65535 / (pow(2, int(outputBitNum)) - 1))
        elif int(outputBitNum) == int(inputBitNum):
            print "!!!!!!!"
            if int(outputBitNum) <= 8:
                print
                # convert to visiable 8-bit
                for i in range(dataset.RasterCount):
                    band_data[i] = band_data[i] * int(255 / (pow(2, int(outputBitNum)) - 1))
            elif int(outputBitNum > 8):
                print
                # convert to visiable 16-bit
                for i in range(dataset.RasterCount):
                    band_data[i] = band_data[i] * int(65535 / (pow(2, int(outputBitNum)) - 1))
    else:
        if int(outputBitNum) < int(inputBitNum):
            param = int(pow(2, inputBitNum) / pow(2, int(outputBitNum)))
            for i in range(dataset.RasterCount):
                band_data[i] = band_data[i] / param
        else:
            param = int(pow(2, int(outputBitNum)) / pow(2, inputBitNum))
            for i in range(dataset.RasterCount):
                band_data[i] = band_data[i] * param

    if showInfo:
        print "Band Info:"
        for i in range(dataset.RasterCount):
            print "[", i.__str__(), "]:band", (i + 1).__str__()

    band_num = output_bands.split(",")

    if int(outputBitNum) <= 8:
        if band_num.__len__() < 3:
            for i in range(len(band_num)):
                datagray = band_data[int(band_num[i])]
                cv2.imwrite(root + name.split(".")[0] + "_" + band_num[i] + ".jpg", datagray)
                if showInfo:
                    print "Success! " + root + name.split(".")[0] + "_" + band_num[i] + ".jpg"
        else:
            datagray = cv2.merge(
                [band_data[int(band_num[0])], band_data[int(band_num[1])], band_data[int(band_num[2])]])
            cv2.imwrite(root + name.split(".")[0] + ".jpg", datagray)
            if showInfo:
                print "Success! " + root + name.split(".")[0] + ".jpg"
    else:
        if band_num.__len__() < 3:
            for i in range(len(band_num)):
                datagray = band_data[int(band_num[i])]
                cv2.imwrite(root + name.split(".")[0] + "_" + band_num[i] + ".png", datagray)
                if showInfo:
                    print "Success! " + root + name.split(".")[0] + "_" + band_num[i] + ".png"
        else:
            datagray = cv2.merge(
                [band_data[int(band_num[0])], band_data[int(band_num[1])], band_data[int(band_num[2])]])
            cv2.imwrite(root + name.split(".")[0] + ".png", datagray)
            if showInfo:
                print "Success! " + root + name.split(".")[0] + ".png"



