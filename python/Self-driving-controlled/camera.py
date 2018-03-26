import argparse
import imutils
from imutils.video import VideoStream
import argparse
import cv2
import time
class Camera:
    def __init__(self):

        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-p", "--picamera", type = int, default = 0,
                        help="whether or not the Raspberry Pi Camera should be used")
        self.args = vars(ap.parse_args())

        self.vs = VideoStream(usePiCamera=self.args["picamera"] >=0).start()
        time.sleep(2.0)

        self.frame = None

    def get_frame(self):
        self.frame = self.vs.read()
        return self.frame
