import numpy as np
import cv2

MAIN_WINDOW = 'hello'
RECT_WINDOW = 'rect'
CELL_WINDOW = 'cell'
CELL_SIZE = 32
GRID_SIZE = 16 * CELL_SIZE

class Frame(object):
    def __init__(self, img, homography):
        self.warped = cv2.warpPerspective(img, homography, (GRID_SIZE, GRID_SIZE))
        cv2.namedWindow(RECT_WINDOW)
        cv2.namedWindow(CELL_WINDOW)
        cv2.imshow(RECT_WINDOW, self.warped)

    def process(self):
        cell = self.get_cell(0, 4)
        cv2.imshow(CELL_WINDOW, cell)

    def cell_start_end(self, id):
        start = id * CELL_SIZE + CELL_SIZE / 4
        end = start + CELL_SIZE / 2
        return start, end

    def get_cell(self, channel, step):
        channel_start, channel_end = self.cell_start_end(channel)
        step_start, step_end = self.cell_start_end(step)
        return self.warped[
          channel_start : channel_end,
          step_start : step_end,
          :]

def global_on_mouse(event, x, y, unknown, lego_player):
    lego_player.on_mouse(event, x, y)

class LegoPlayer(object):
    def __init__(self):
        self.homography = None
        self.roi = np.empty((4, 2))
        self.roi_index = -1

        cv2.namedWindow(MAIN_WINDOW)
        cv2.setMouseCallback(MAIN_WINDOW, global_on_mouse, self)
        self.capture = cv2.VideoCapture(0)

    def on_mouse(self, event, x, y):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.has_roi():
                self.roi_index = -1
            self.roi_index += 1
            self.roi[self.roi_index] = [x, y]
            if self.has_roi():
                self.compute_homography()

    def has_roi(self):
        return self.roi_index == 3

    def compute_homography(self):
        src_points = self.roi
        dst_points = np.zeros_like(src_points)
        dst_points[1][0] = GRID_SIZE
        dst_points[2] = [GRID_SIZE, GRID_SIZE]
        dst_points[3][1] = GRID_SIZE
        self.homography = cv2.findHomography(src_points, dst_points)[0]

    def loop(self):
        while True:
            success, img = self.capture.read()
            if success:
                cv2.imshow(MAIN_WINDOW, img)
                if self.homography is not None:
                    frame = Frame(img, self.homography)
                    frame.process()
            cv2.waitKey(10)

if __name__ == '__main__':
    lego_player = LegoPlayer()
    lego_player.loop()
