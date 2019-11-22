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
"""

"""
    TO-DO:
    1 - search for the best way to specify the hyper parameters parameters
    2 - search for how to make the hyper parameters dynamic.
    3 -   
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
    display(blured_image)
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
    display(edges_image)

    return edges_image
def processes_video():
    video_name ='solidWhiteRight.mp4'
    cap = cv2.VideoCapture("solidWhiteRight.mp4")
    while True:
        ret, frame = cap.read()
        #print(ret)
        #if ret == False:
        #    break

        # processes the frame
        #processed_image = main(frame , True)
        cv2.imshow("prcessed image " , frame)
        cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()

    return

def main(image , video):
    global Avg_left_lane , Avg_right_lane
    original_image = image
    if video==False:
        img_name = "solidWhiteCurve.jpg"
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
    print(Avg_left_lane)
    print(Avg_right_lane)

    # draw lines
    lines_image = draw_lines([Avg_left_lane] , original_image)
    lines_image = draw_lines([Avg_right_lane] , lines_image)
    display(original_image)
    return

# C++ lover
#main(None , False)
processes_video()