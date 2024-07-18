import sys
from urllib.request import urlopen
import cv2 as cv
import numpy as np


# this function retrieve frame from url stream
def capture_from_web_camera(url):
    # retrieve frame
    cam = urlopen(url)
    img = cam.read()
    # convert to numpy array
    img = np.asarray(bytearray(img), dtype='uint8')
    # from numpay array to rgb image
    img = cv.imdecode(img, cv.IMREAD_UNCHANGED)
    cv.waitKey(1)
    return img


# this function retrieves frame from virtual camera and applies computer vision algorithm
def localize_car():
    # open device virtual camera
    cap = cv.VideoCapture(1)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    while cap.isOpened():
        # retrieve frame
        ret, img = cap.read()
        h, w, _ = img.shape
        width = 1000
        height = int(width * (h / w))
        img = cv.resize(img, (width, height), interpolation=cv.INTER_CUBIC)
        # find aruco code inside the image
        corners, ids, rejected = detect_aruco(img)
        # display border code and text upon the image
        detected_markers = aruco_display(corners, ids, rejected, img)
        # return image as request response
        ret, buffer = cv.imencode(".jpg", detected_markers)
        detected_markers = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + detected_markers + b'\r\n')

# list of all aruco code dict given by opencv
ARUCO_DICT = {
    "DICT_4X4_50": cv.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv.aruco.DICT_APRILTAG_36h11
}

# aruco code type used in this section
aruco_type = "DICT_4X4_100"
arucoDict = cv.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])
arucoParams = cv.aruco.DetectorParameters()


# computer vision algorithm
def detect_aruco(img):
    parameters = cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(arucoDict, parameters)
    # [[(xtl, ytl), (xtr, ytr), (xbr, ybr), (xbl, ybl)] for each code detected]
    corners, ids, rejected = detector.detectMarkers(img)
    return corners, ids, rejected


# this function applies computer vision algorithm to url stream
def read_aruco_code(url):
    img = capture_from_web_camera(url)
    h, w, _ = img.shape
    width = 500
    height = int(width * (h / w))
    img = cv.resize(img, (width, height), interpolation=cv.INTER_CUBIC)
    corners, ids, rejected = detect_aruco(img)
    return ids


# overlay text upon image
def aruco_display(corners, ids, rejected, image):
    if len(corners) > 0:
        ids = ids.flatten()

        # attach id to corners and iterate
        for (markerCorner, markerId) in zip(corners, ids):
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            # draw square encapsulating code
            cv.line(image, topLeft, topRight, (0, 255, 0), 2)
            cv.line(image, topRight, bottomRight, (0, 255, 0), 2)
            cv.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

            cx = int((topLeft[0] + bottomRight[0]) / 2.0)
            cy = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv.circle(image, (cx, cy), 4, (0, 0, 255), -1)
            cv.putText(image, str(markerId), (topLeft[0], topLeft[1] - 10), cv.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 2)
    return image


# robot view render
def robot_camera_view():
    while True:
        img = capture_from_web_camera("http://192.168.4.1/capture")
        corners, ids, rejected = detect_aruco(img)
        detected_markers = aruco_display(corners, ids, rejected, img)
        ret, buffer = cv.imencode(".jpg", detected_markers)
        detected_markers = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + detected_markers + b'\r\n')

