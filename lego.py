import numpy as np
import cv2

from midi import PatternPlayer

MAIN_WINDOW = 'hello'
CELL_SIZE = 32
GRID_SIZE = 16 * CELL_SIZE

def is_note_color(color):
    b, g, r = color
    return ((r < 100 and g < 200 and b > 150) # blue brick
         or (r > 200 and g < 100 and b < 100) # red brick
         or (r > 200 and g > 150 and b < 150)) # yellow brick

def is_clear_color(color):
    b, g, r = color
    return r < 100 and g > 100 and b < 150

class PatternCreator(object):
    def __init__(self, num_channels, num_steps):
        self.pattern = np.empty((num_channels, num_steps), np.bool)

    def update_pattern(self, img):
        for channel in range(self.pattern.shape[0]):
            for step in range(self.pattern.shape[1]):
                cell = self.get_cell(img, channel, step)
                average_color = np.average(np.average(cell, axis=0), axis=0)
                if is_clear_color(average_color):
                    self.pattern[channel][step] = False
                elif is_note_color(average_color):
                    self.pattern[channel][step] = True

    def cell_start_end(self, id):
        start = id * CELL_SIZE + CELL_SIZE / 4
        end = start + CELL_SIZE / 2
        return start, end

    def get_cell(self, img, channel, step):
        channel_start, channel_end = self.cell_start_end(channel)
        step_start, step_end = self.cell_start_end(step)
        return img[
          channel_start : channel_end,
          step_start : step_end,
          :]

    def print_pattern(self):
        for channel in self.pattern:
            for step in channel:
                if step:
                    print '*',
                else:
                    print ' ',
            print
        print

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

        self.pattern_creator = PatternCreator(4, 16)
        self.pattern_player = PatternPlayer(self.pattern_creator.pattern, 120)

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
            success, frame = self.capture.read()
            if success:
                if self.homography is None:
                    cv2.imshow(MAIN_WINDOW, frame)
                else:
                    warped = cv2.warpPerspective(frame, self.homography, (GRID_SIZE, GRID_SIZE))
                    cv2.imshow(MAIN_WINDOW, warped)
                    self.pattern_creator.update_pattern(warped)
                    self.pattern_creator.print_pattern()
                    self.pattern_player.pattern = self.pattern_creator.pattern
            if cv2.waitKey(100) != -1:
                self.pattern_player.stop()
                break


if __name__ == '__main__':
    lego_player = LegoPlayer()
    lego_player.loop()
