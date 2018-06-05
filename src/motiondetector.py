import cv2 as cv
import imutils
import numpy as np
import copy

class MotionDetector():
    def onThresholdChange(self, val):
        self.threshold = val

    def __init__(self, threshold = 0.2, showWindows = True): 
        self.camera = cv.VideoCapture(1)
        self.threshold = threshold
        self.showWindows = showWindows
        self.frame = None

        # Create the initial frame
        (grabbed, sframe) = self.camera.read()

        self.frame = sframe
        self.gray_frame = sframe
        self.average_frame = None
        self.absdiff_frame = None
        self.previous_frame = None
        height, width, channels = self.frame.shape
        self.surface = height * width

        self.current_contours = None
        self.trigger_time = 0

    def getFrame(self):
        grabbed, frame = self.camera.read()

        return frame

    def run(self, callback):
        while True:
            c = cv.waitKey(1) % 0x100
            # If Esc of Enter key is pressed, the process wil be ended.
            if c == 27 or c == 10:
                break

            currentFrame = self.getFrame()
            self.processImage(currentFrame)

            avg = self.somethingHasMoved()

            if avg:
                #print('ja')
                callback(avg)

            if self.showWindows:
                cv.imshow('Image', currentFrame)
                cv.imshow('previous', self.previous_frame)
                cv.imshow('difference', self.absdiff_frame)

        
    def processImage(self, curFrame):
        curFrame = cv.cvtColor(curFrame, cv.COLOR_BGR2GRAY)
        curFrame = cv.blur(curFrame,(25, 25))

        if self.absdiff_frame is None:
            self.absdiff_frame = curFrame.copy()
            self.previous_frame = curFrame.copy()

        self.gray_frame = curFrame
        self.absdiff_frame = cv.absdiff(self.previous_frame, self.gray_frame)
        self.absdiff_frame = cv.threshold(self.absdiff_frame, 10, 255, cv.THRESH_BINARY)[1]
        self.absdiff_frame = cv.dilate(self.absdiff_frame, None, iterations=5)
        self.previous_frame = self.gray_frame.copy()

    def somethingHasMoved(self):
        (_, contours, _) = cv.findContours(self.absdiff_frame.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        currentSurface = 0

        for c in contours:  
            currentSurface += cv.contourArea(c )

        avg = (currentSurface*100)/self.surface

        if avg > self.threshold:
            return avg
        else:
            False


if __name__ == '__main__':
    detector = MotionDetector(threshold=0.2, showWindows=True)
    detector.run()