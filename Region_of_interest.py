import numpy as np
import cv2

def display(image):   # ****************************************** will be removed ************************************************************
    cv2.imshow("tmp" , image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return

def ROI(image):
    """
    - X is a column.
    - Y is a row.
    - our ROI is a polygon.
    - we need to make the ROI more dynamic.
    - we need to read more about the assumations and limations of the ROI.
    :param image:  binary image that only have edges.
    :return: image with edges only from the region of interest (ROI).
    """
    # image info
    height , width = image.shape

    # peresentage
    V_pres = 3/5 # I take ( 1 - V_pres ) of the image height
    H_pres = 1/8  # I leave ( H_pres ) from both sides

    # *********** I need to specify the presentage of pixels that I leave form the upper boundary  ************

    # upper right boundary
    upper_right_x = int(width - width*(3/8))  # leave 3/8 from the right of the image.
    upper_right_y = int(height*V_pres)

    # upper left  boundary
    upper_left_x = int(width*(3/8))   # leave 3/8 from the left of the image.
    upper_left_y = int(height*V_pres)

    # lower right boundary
    lower_right_x = width-1 #int(width-width*H_pres)
    lower_right_y = height-1

    # lower left boundary
    lower_left_x = 0 #int(width*H_pres)
    lower_left_y = height-1

    # points are (col , row)
    # order of points matters as cv2 just connect the points in order
    polygon = [ [upper_left_x , upper_left_y] ,
                [lower_left_x, lower_left_y],
                [lower_right_x, lower_right_y] ,
                [upper_right_x , upper_right_y] ]

    return extract_ROI(polygon , image)

def extract_ROI(polygon , image):
    '''
    fillpoly do it's work in place
    fillpoly take points as (col , row)
    fillpoly take a very stupid parameter dimension : np array of array of arrays
    fillpoly care about the order of the points as cv2 just connect the points in order

    :param polygon:  that descripe the polygon
    :param image: gray scale image
    :return:  gray scale image with that contain only the ROI
    '''

    # create the  mask
    mask = np.zeros(image.shape , dtype=np.uint8)

    # specify the color
    color = 255
    if len(image.shape) == 3:
        color = [255, 255, 255]

    print(polygon)
    cv2.fillPoly(mask, np.array([polygon], dtype=np.int32), color)
    cv2.bitwise_and(image , mask , dst=mask)
    #display(mask)
    return mask  # has the ROI
