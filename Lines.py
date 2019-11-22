import numpy as np
import cv2

"""
    here we wil detect and draw lines 
"""

# constant colors
RED = (0 , 0 , 255)
BLUE = (255 , 0 , 0)
GREEN = (0 , 255 , 0)


def display(image):   # ****************************************** will be removed ************************************************************
    cv2.imshow("tmp" , image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return


def Hough_lines(image):
    '''
    - min length allowed line and treshold have some  logical relation , as number of votes
      depends on the number of points on the lines , that depend on the length of the line.
    - early canny detection and min  , max treshold affect here.
    - we have to know min and max length of each landmark in the road in terms of pixels
      and analyse how does this change form resolution to another.

    :param image:  binary image with that only have edges
    :return: points of lines that we detected
    '''
    rho_accu = 1                # mean that we consider the smallest perpendicular distance = 1 pixel
    theta_accu = np.pi/180      # radians == mean that we move with 1 degree at a time
    # are theses measured in pixels , and if why they are doubles  ???!!!!
    T = 10
    min_len = 5
    max_gap = 20
    lines = cv2.HoughLinesP(image , rho_accu , theta_accu , T , minLineLength=min_len , maxLineGap=max_gap)
    return lines

def split_lines(lines):
    """
    - keep in mind the different coordinate system of the image.
    - we need to seprate lines into left lane and right lane.
    - and ignore horizontal or vertical lines.
    :param lines: list of list and the inner list have 4 numbers 2 * ( col , row ) that specify the end points of a line.
    :return:
    """
    right_lanes = []
    left_lanes = []
    for i in range(0 , lines.shape[0] , 1):
        # (col , row)
        start_x , start_y , end_x, end_y = lines[i]

        if start_x > end_x:
            point1 = (start_x , start_y)
            point2 = (end_x , end_y)
        else :
            point2 = (start_x , start_y)
            point1 = (end_x , end_y)

        # we will consider that point 1 is always the farther in col

        # vertical lane line
        if point1[0] == point2[0]:
            continue
        # horizontal lane line
        elif point1[1] == point2[1]:
            continue
        # right lane line
        elif point1[1] > point2[1]:
            right_lanes.append(list(lines[i]))
        # left lane line
        else:
            left_lanes.append(list(lines[i]))

    print("number of right lines : " , len(right_lanes))
    print("number of left lines : ", len(left_lanes))
    return left_lanes, right_lanes


def average_lines(lines , Avg_ux , Avg_uy , Avg_lx , Avg_ly):
    """
    - I will work on averaging the end points
    -  ***************** we need to find better way to average the lines ******************
    :param left_lanes:
    :param right_lanes:
    :return:
    """
    # left lane averging end points
    avg_lx = 0
    avg_ly = 0
    avg_ux = 0
    avg_uy = 0

    for i in range(0 , len(lines), 1):
        # (col , row)
        fx , fy , sx , sy = lines[i]
        point1 = 0
        point2 = 0

        # point1 will have the lower point
        if fy>sy:
            point1 = (fx , fy)
            point2 = (sx , sy)
        else:
            point2 = (sx , sy)
            point1 = (fx , fy)

        # average the points
        avg_lx += point1[0]
        avg_ly += point1[1]
        avg_ux +=point2[0]
        avg_uy +=point2[1]

    # calculate moving average  , more smooth detection
    # the problem here is the bias that we need to correct as
    # we did initialize the averages = 0 in the begining.
    """
    Avg_lx = int(.9*Avg_lx + .1*avg_lx)
    Avg_ly = int(.9*Avg_ly + .1*avg_ly)
    Avg_ux = int(.9*Avg_ux + .1*avg_ux)
    Avg_uy = int(.9*Avg_uy + .1*avg_uy)
    """

    l= len(lines)
    return [avg_lx //l , avg_ly //l , avg_ux //l , avg_uy //l]


def exterpolate_lines(line):
    """

    :param line: is the two end points of left or right alane line
    :return: exterpolated line
    """
    pass
def draw_lines(lines , original_image):
    """
    - we get points in lines as ( col , row ).
    - cv2.lines don't affect the image passed in the parameter.
    :param lines: list of list and the inner list have 4 numbers 2 * ( col , row ) that specify the end points of a line.
    :param original_image: the BGR original image c oming from the camera feed , or video.
    :return:  copy of the original image overlapped with the lines detected.
    """
    line_thickness = 2
    lines_image = np.copy(original_image)
    for i in range(0 , len(lines), 1):
        start_x , start_y  , end_x , end_y = lines[i]
        lines_image = cv2.line(lines_image , (start_x , start_y) , (end_x , end_y) , RED , line_thickness)
    display(lines_image)
    return lines_image