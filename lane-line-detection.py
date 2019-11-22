import math
import copy
import time
import numpy as np
import cv2

# my packages
from Lines import *
from Region_of_interest import *


"""
    Notes:
    1 - opencv store images in BGR.
    2 - we did get the gray scale and ROI early to make the computations faster.
    3 - every function that produce a new image will call display function for debuging reasons
    4 - in pipe line 3 and 4 have to go in this order as if the reverse we will have extra edges
        on the boundary between ROI and the rest of the image and they are supposed to be plain area, 
        however this will be faster in edge detection but will produce wrong results.
    5 - currently my hard coded hyper parameters give me perfect result 
    6 - I have to keep the whole Image size matrix even after getting the ROI 
        such that we get the right coordinates of voted points from houghline transform, 
        and being able to draw them in the original image.
        
    7 - we can detect at which part of the road we are 
        by the number of detected lines in each side as the more lines 
        mean the thick line and less lines mean the dashed one
        is this right , and applicable  !?
        
    8 - ( very important )line shape don't infer it's slope here as the image cordinate system is reflected 
        so we look at them in terms changes in x and y and look at the relation between them 
        which make +ve slope looking be in the image as -ve slope 
        and vice versus
    9 - if we did averge lines with slopes and intercept this will save the step of extrapolate.
    
    10 -
          
"""

"""
    TO-DO:
    1 - search for the best way to specify the hyper parameters parameters
    2 - search for how to make the hyper parameters dynamic.
    3 - in avergining the lines we can take into account the the length of the lines as weighted average 
        also we can take lines with some specific length into account 
        also we can look at standard diviation of slopes which I don't get it's idea here !!?
    4 - try to average slopes and intercepts instead of avergining coordinates points and see the difference 
    5 - I need to make the lines more table across frames 
    6 - I need to make the line more thicker 
    7 - I need to cut of from the vanching points of the two line or low down the intersection.
    8 - investigate every pipeline step and see which part tham make the lines unstable 
      
"""

"""
    Questions:
    1 - does it differ to apply gaussian filter before or after converting the image into gray ??
    2 - what fuck is apertureSize in canny edge detector ??
    3 - does the points in lines list are always ordered as the higher coordinate first ?? 
"""

"""
    my pipe line is :
    1 - load the image and get gray scale copy
    2 - filter the image with gaussian filter
    3 - get edges using cany edge detector 
    4 - get region of interest
    5 - detect hough lines 
    6 - split the lines detected into right lane and left lane , ignore horizontal and vertical 
    7 - average the lines to get only 1 line for each lane 
    8 - draw the lines on a copy of the original image 
    [9] - if we will work on video it we just will read the vidoe frame by frame then we will go throw the same pipeline  
"""

"""
    To - Learn :
    1 - coordinate geometry
    2 - parametric equation of line in 3d and 2d space 
    3 - line exterpolation , interpolation  
"""

# we will use moving average as it make transaction between different detected lines
# more smooth
# check the performance with them and without
# lower point then upper point  (col ,row)
Avg_left_lane = (0 , 0 , 0 , 0)
Avg_right_lane = (0  , 0 , 0 ,0)


def display(image):
    cv2.imshow("tmp" , image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return

def gauss_blur(image):
    """
    :param image:  gray  image
    :return:  blurred image with gaussian filter to remove the noise from it
    """
    blured_image = cv2.GaussianBlur(image , (7 , 7) , 0)
    #display(blured_image)
    return blured_image



def canny_edges(image):
    '''
    :param iamge:  gray  image
    :return: binary image with it's edges detected
    '''
    T1 = 80     # week edge
    T2 = 150     # was 220 strong edge , ***************** could be extreme in some bad roads *****************
    ap_size = 3 # ***********************  what is this !???   **************************
    edges_image = cv2.Canny(image , T1 , T2 , apertureSize=ap_size , L2gradient=True)
    #display(edges_image)

    return edges_image
def processes_video():
    """
    - how to locate the waiting time in ms that is proper to the frame per second we egt from the video ?
    :return:
    """
    video_name ='test_videos/solidYellowLeft.mp4'
    cap = cv2.VideoCapture(video_name)
    while True:
        print("here")
        ret, frame = cap.read()
        print(ret)
        if ret == False:
            break

        # processes the frame
        processed_image = processes_image(frame , True)
        cv2.imshow("prcessed image " , processed_image)
        cv2.waitKey(15)

    cap.release() # what does this do !?
    cv2.destroyAllWindows()

    return

def processes_image(image , video):
    global Avg_left_lane , Avg_right_lane
    original_image = image
    if video==False:
        img_name = "test_images/solidWhiteCurve.jpg"
        # load the image
        original_image = cv2.imread(img_name , -1)

    # cvt to gray
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # gaussian filter
    blurred_image = gauss_blur(gray_image)

    # canny edge detector
    edges_image = canny_edges(blurred_image)

    # get region of interest
    ROI_image = ROI(edges_image)

    # detect the hough lines
    lines = Hough_lines(ROI_image)
    lines = np.squeeze(lines)

    # split the lines
    left_lines , right_lines = split_lines(lines)

    # Average the lines
    # left lane
    Avg_left_lane = average_lines(left_lines , Avg_left_lane[0] , Avg_left_lane[1], Avg_left_lane[2] , Avg_left_lane[3])
    # right lane
    Avg_right_lane = average_lines(right_lines , Avg_right_lane[0] , Avg_right_lane[1], Avg_right_lane[2] , Avg_right_lane[3])

    # extrapolate lines
    ex_left_lane = exterpolate_line(Avg_left_lane , original_image)
    ex_right_lane = exterpolate_line(Avg_right_lane , original_image)
    # draw lines
    lines_image = draw_lines([ex_left_lane] , original_image)
    lines_image = draw_lines([ex_right_lane] , lines_image)

    #display(lines_image)
    return lines_image


#processes_image(None , False)
processes_video()
