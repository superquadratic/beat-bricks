import numpy as np
import cv2

WINDOW_NAME = 'hello'

def global_on_mouse(event, x, y, unknown, lego_player):
    lego_player.on_mouse(event, x, y)

class LegoPlayer(object):
    def __init__(self):
        self.rect = np.empty((4, 2))
        self.rect_index = -1

        cv2.namedWindow(WINDOW_NAME)
        cv2.setMouseCallback(WINDOW_NAME, global_on_mouse, self)
        self.capture = cv2.VideoCapture(0)

    def on_mouse(self, event, x, y):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.has_roi():
                self.rect_index = -1
            self.rect_index += 1
            self.rect[self.rect_index] = [x, y]
            if self.has_roi():
                self.compute_homography()

    def has_roi(self):
        return self.rect_index == 3

    def compute_homography(self):
        src_points = self.rect
        dst_points = np.zeros_like(src_points)
        dst_points[1][0] = 512
        dst_points[2] = [512, 512]
        dst_points[3][1] = 512
        print cv2.findHomography(src_points, dst_points)

    def process_frame(self, frame):
        return cv2.split(frame)[2]

    def loop(self):
        while True:
            success, frame = self.capture.read()
            result = self.process_frame(frame)
            cv2.imshow(WINDOW_NAME, result)
            cv2.waitKey(10)

if __name__ == '__main__':
    lego_player = LegoPlayer()
    lego_player.loop()
