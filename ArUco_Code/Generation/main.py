import numpy as np
import cv2

# generation

# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

aruco_type = "DICT_4X4_100"
id = 16

arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])

tag_size = 100
# aruco code --> image black and white --> array of bit
tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")

# draw the ArUco tag
# arucoDict: The ArUco dictionary loaded by cv2.aruco.getPredefinedDictionary.
# This function tells OpenCV which ArUco dictionary we are using, how to draw the tags, etc.
# id: The ID of the ArUco tag we are drawing. This ID must be a valid tag ID in arucoDict.
# tag_size: The size of the ArUco tag that will be drawn. This value should match the width/height of the
# NumPy array we initialized.
# tag: The NumPy array that we are drawing the ArUco tag on.
# 1: The number of “border bits” to pad the tag with. If we generate a 5×5 tag,
# then setting borderBits=1will output a 6×6 image with a 1 bit border surrounding the 5×5 region,
# making the tag easier to detect and read. Typically you should set borderBits=1
cv2.aruco.generateImageMarker(arucoDict, id, tag_size, tag, 1)

# save the tag
tag_name = "{}_{}.png".format(aruco_type, id)
cv2.imwrite(tag_name, tag)