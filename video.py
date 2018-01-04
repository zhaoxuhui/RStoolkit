# coding=utf-8
import cv2

import common


def makeVideo(image_path, image_type, fps, out_path, scale_factor=1, showInfo=True):
    """
    A fuction for compose a video from a set of images.
    
    :param image_path: String,the parent dictionary of images.e.g."E:/test/"
    :param image_type: String,the file type of images.e.g."jpg"
    :param fps: Int,the "frame per second" of output video.e.g.24
    :param out_path: String,the output path of video.e.g."E:/out.avi"
    :param scale_factor: Float,the zoom factor of images to compose the video."1"  as default,means use the original size.e.g.0.5
    :param showInfo: Boolean,True as default.Whether to show information during processing.
    :return: Nothing.But the output video will be saved in the dictionary you choose.
    
    Usage:
     makeVideo("E:/test/", "jpg", 25, "E:/out.avi")
    """

    rootdir = image_path + common.getSeparator()
    output = out_path + common.getSeparator() + "video.avi"
    type = image_type
    if scale_factor is not 1:
        scale = scale_factor
    fps = fps

    paths = common.findAllFiles(rootdir, type)

    if showInfo:
        print "Processing...\n"
        print paths.__len__(), "frames were found."

    tem = cv2.imread(paths[0])
    width = int(scale * tem.shape[1])
    height = int(scale * tem.shape[0])

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output, fourcc, fps, (width, height))

    count = 0

    for item in paths:
        frame = cv2.imread(item)
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
        out.write(frame)
        count += 1
        if showInfo:
            print "Making...", round((count * 1.0 / paths.__len__()) * 100, 2), " % finished."
    out.release()

    if showInfo:
        print "--------------------------------"
        print "Output Video Information:"
        print "Output path:" + output
        print "Width:" + width.__str__()
        print "Height:" + height.__str__()
        print "FPS:" + fps.__str__()
        print "Frames:" + paths.__len__().__str__()
        print "Time:" + (paths.__len__() * 1.0 / fps * 1.0).__str__() + " s"
        print "--------------------------------"


def extractROI(input_path, output_path, left_top_x, left_top_y, right_bottom_x, right_bottom_y, showInfo=True):
    """
    A function for extract ROI(Region Of Interest) from a video.
    
    :param input_path: String,the file path of input video.e.g."E:/test.avi"
    :param output_path: String,the file path of output video.e.g."E:/roi.avi"
    :param left_top_x: Float,the x pixel coordinate of top-left point.e.g.10
    :param left_top_y: Float,the y pixel coordinate of top-left point.e.g.10
    :param right_bottom_x: Float,the x pixel coordinate of right-bottom point.e.g.100
    :param right_bottom_y: Float,the y pixel coordinate of right-bottom point.e.g.100
    :param showInfo: Boolean,True as default.Whether to show information during processing.
    :return: Nothing.But the output video will be saved in the dictionary you choose.
    
    Usage:
     extractROI("E:/test/test.avi", "E:/roi.avi", 10, 10, 100, 100)
    """

    cap = cv2.VideoCapture(input_path)

    width = int(cap.get(3))
    height = int(cap.get(4))
    total = int(cap.get(7))

    fps = 20
    waitTime = 1
    count = 0

    if cap.get(5) != 0:
        waitTime = int(1000.0 / cap.get(5))
        fps = cap.get(5)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (right_bottom_x - left_top_x, right_bottom_y - left_top_y))

    while cap.isOpened():
        ret, frame = cap.read()
        if frame is None:
            break
        else:
            res = frame[left_top_y:right_bottom_y, left_top_x:right_bottom_x, :]

            out.write(res)
            count += 1
            if showInfo:
                print 'Extracting...', round((count * 1.0 / total) * 100, 2), ' % finished.'
            k = cv2.waitKey(waitTime) & 0xFF
            if k == 27:
                break
    cap.release()
    out.release()


def zoomVideo(input_path, output_path, scale_factor=1, showInfo=True):
    """
    A function for zooming video.
    
    :param input_path: String,the file path of input video.e.g."E:/test.avi"
    :param output_path: String,the file path of output video.e.g."E:/zoom.avi"
    :param scale_factor: Float,the zoom factor of images to compose the video."1"  as default,means use the original size.e.g.0.5
    :param showInfo: Boolean,True as default.Whether to show information during processing.
    :return: Nothing.But the output video will be saved in the dictionary you choose.
    
    Usage:
     zoomVideo("E:/test/test.avi", "E:/zoom.avi", 0.5)
    """

    cap = cv2.VideoCapture(input_path)

    total = int(cap.get(7))
    width = int(scale_factor * int(cap.get(3)))
    height = int(scale_factor * int(cap.get(4)))

    fps = 20
    waitTime = 1
    count = 0

    if cap.get(5) != 0:
        waitTime = int(1000.0 / cap.get(5))
        fps = cap.get(5)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if frame is None:
            break
        else:
            res = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

            out.write(res)
            count += 1
            if showInfo:
                print 'Zooming...', round((count * 1.0 / total) * 100, 2), ' % finished.'
            k = cv2.waitKey(waitTime) & 0xFF
            if k == 27:
                break
    cap.release()
    out.release()


def resizeVideo(input_path, output_path, width, height, showInfo=True):
    """
    A function for resizing video.
    
    :param input_path: String,the file path of input video.e.g."E:/test.avi"
    :param output_path: String,the file path of output video.e.g."E:/zoom.avi"
    :param width: Int,the new width of output video.e.g.640
    :param height: Int,the new height of output video.e.g.480
    :param showInfo: Boolean,True as default.Whether to show information during processing.
    :return: Nothing.But the output video will be saved in the dictionary you choose.
    
    Usage:
     resizeVideo("E:/test/test.avi", "E:/resize.avi", 640, 480)
    """

    cap = cv2.VideoCapture(input_path)

    total = int(cap.get(7))

    fps = 20
    waitTime = 1
    count = 0

    if cap.get(5) != 0:
        waitTime = int(1000.0 / cap.get(5))
        fps = cap.get(5)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if frame is None:
            break
        else:
            res = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

            out.write(res)
            count += 1
            if showInfo:
                print 'Resizing...', round((count * 1.0 / total) * 100, 2), ' % finished.'
            k = cv2.waitKey(waitTime) & 0xFF
            if k == 27:
                break
    cap.release()
    out.release()


def clipVideo(input_path, output_path, start_time, end_time, showInfo=True):
    """
    A function for clipping video.
    
    :param input_path: String,the file path of input video.e.g."E:/test.avi"
    :param output_path: String,the file path of output video.e.g."E:/clip.avi"
    :param start_time: Float,the start time in second.e.g. 1.5
    :param end_time: Float,the end time in second.e.g. 20
    :param showInfo: Boolean,True as default.Whether to show information during processing.
    :return: Nothing.But the output video will be saved in the dictionary you choose.
    
    Usage:
     clipVideo("E:/test/test.avi", "E:/clip.avi", 1.5, 20)
    """

    video_path = input_path
    out_path = output_path
    start = start_time
    end = end_time
    cap = cv2.VideoCapture(video_path)

    frames = int(cap.get(7))
    fps = int(cap.get(5))

    if showInfo:
        print (round(frames / fps, 2)).__str__(), 'seconds(', frames, 'frames', ') in total.'

    startIndex = int(start * fps)
    endIndex = int(end * fps)
    rangeFrames = endIndex - startIndex
    count = 0

    video_h = int(cap.get(4))
    video_w = int(cap.get(3))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(out_path, fourcc, fps, (video_w, video_h))

    if rangeFrames < 0:
        if showInfo:
            print 'Error.'
        exit()

    if showInfo:
        print rangeFrames, 'frames are going to be outputted.'

    for i in range(startIndex):
        ret, frame = cap.read()

    for i in range(startIndex, endIndex):
        ret, frame = cap.read()
        if frame is None:
            break
        else:
            out.write(frame)
            count += 1
            if showInfo:
                print 'Cutting...', round((count * 1.0 / rangeFrames) * 100, 2), "% finished."
    cap.release()


def resolveVideo(input_path, output_folder, start_time, end_time, interval=1, showInfo=True):
    """
    A function for decomposing a video to a set of images.
    
    :param input_path: String,the file path of input video.e.g."E:/test.avi"
    :param output_folder: String,the parent dictionary of output images.e.g."E:/output/"
    :param start_time: Float,the start time in second.e.g. 1.5
    :param end_time: Float,the end time in second.e.g. 20
    :param interval: Int,the interval for loading frames.1 as default, means read every frame.e.g.1
    :param showInfo: Boolean,True as default.Whether to show information during processing.
    :return: Nothing.But the output video will be saved in the dictionary you choose.
    
    Usage:
     resolveVideo("E:/test/test.avi", "E:/output", 1.5, 20)
    """
    video_path = input_path
    out_path = output_folder
    interval = interval
    start = start_time
    end = end_time
    cap = cv2.VideoCapture(video_path)

    frames = int(cap.get(7))
    fps = int(cap.get(5))

    if showInfo:
        print frames, 'frames in total.'

    startIndex = int(start * fps)
    endIndex = int(end * fps)
    rangeFrames = endIndex - startIndex
    count = 0

    if rangeFrames < 0:
        if showInfo:
            print 'Error.'
        exit()

    if showInfo:
        print rangeFrames / interval, 'frames are going to be outputted.'

    for i in range(startIndex):
        ret, frame = cap.read()

    for i in range(startIndex, endIndex, interval):
        ret, frame = cap.read()
        if frame is None:
            break
        else:
            cv2.imwrite(out_path + common.getSeparator() + "%04d" % (i + 1) + ".jpg", frame)
            count += interval
            if showInfo:
                print 'Resolving...', round((count * 1.0 / rangeFrames) * 100, 2), "% finished."
    cap.release()


def getFrameNo(video_path, time):
    """
    A function for get frame number according to time in seconds.
    
    :param video_path: String,the file path of input video.e.g."E:/test.avi"
    :param time: Float,the time you want to get in frame number.e.g.4.5
    :return: Int,the frame number
    
    Usage:
     getFrameNo("E:/test/test.avi", 1.5)
    """

    cap = cv2.VideoCapture(video_path)
    frames = int(cap.get(7))
    fps = int(cap.get(5))
    cap.release()
    total_time = frames * 1.0 / fps
    return int((time / total_time) * frames)


def getFrameTime(video_path, number):
    """
    A function for get time in seconds according to frame number.
    
    :param video_path: String,the file path of input video.e.g."E:/test.avi"
    :param number: Int,the frame number.e.g.1020
    :return: Float,the time you want to get
    
    Usage:
     getFrameTime("E:/test/test.avi", 1020)
    """
    cap = cv2.VideoCapture(video_path)
    frames = int(cap.get(7))
    fps = int(cap.get(5))
    cap.release()
    total_time = frames * 1.0 / fps
    return (number * 1.0 / frames) * total_time


def getVideoInfo(video_path):
    """
    A function for getting brief info about video.
    :param video_path: String,the file path of input video.e.g."E:/test.avi"
    :return: Dictionary,contains key:frames,fps,width,height,total_time.
    
    Usage:
     info = getVideoInfo("E:/test/test.avi")
     
     print info['frames']
    """

    info = {}
    cap = cv2.VideoCapture(video_path)
    info["frames"] = int(cap.get(7))
    info["fps"] = int(cap.get(5))
    info["width"] = int(cap.get(3))
    info["height"] = int(cap.get(4))
    info["total_time"] = info["frames"] * 1.0 / info["fps"]
    return info
