import json

import cv2
import numpy

from pattern import SharedPattern

WINDOW = 'beat it'
CELL_SIZE = 16
GRID_SIZE = 16 * CELL_SIZE

def cell_start_end(id):
    start = id * CELL_SIZE + CELL_SIZE / 4
    end = start + CELL_SIZE / 2
    return start, end

def average_cell_color(img, y, x):
    y_start, y_end = cell_start_end(y)
    x_start, x_end = cell_start_end(x)
    cell = img[
      y_start : y_end,
      x_start : x_end,
      :]
    return numpy.average(numpy.average(cell, axis=0), axis=0)

def is_note_color(color):
    b, g, r = color
    return ((r < 100 and g < 200 and b > 150) # blue brick
         or (r > 150 and g < 100 and b < 100) # red brick
         or (r > 200 and g > 150 and b < 150)) # yellow brick

def is_clear_color(color):
    b, g, r = color
    return r < 100 and g > 0 and b < 150

class LegoPatternReader(object):
    def __init__(self, num_tracks, num_steps):
        self.pattern = numpy.ones((num_tracks, num_steps), numpy.bool)
        self.muted = numpy.zeros((num_tracks), numpy.bool)

class LegoPatternDetector(object):
    def __init__(self):
        self.homography = self.compute_homography()
        self.pattern = SharedPattern()

    def compute_homography(self):
        src_points = json.load(open('rect.json'))
        dst_points = [[        0,         0],
                      [GRID_SIZE,         0],
                      [GRID_SIZE, GRID_SIZE],
                      [        0, GRID_SIZE]]
        return cv2.findHomography(
            numpy.asarray(src_points, float),
            numpy.asarray(dst_points, float))[0]

    def process_image(self, img):
        img = cv2.warpPerspective(img, self.homography, (GRID_SIZE, GRID_SIZE))
        self.update_notes(img)
        self.mute_tracks(img)
        return img

    def update_notes(self, img):
        for track in range(self.pattern.num_tracks):
            for step in range(self.pattern.num_steps):
                color = average_cell_color(img, track, step)
                if is_clear_color(color):
                    self.pattern.clear_step(track, step)
                elif is_note_color(color):
                    self.pattern.set_step(track, step)

    def mute_tracks(self, img):
        for track in range(self.pattern.num_tracks):
            color = average_cell_color(img, track + 8, 0)
            if is_clear_color(color):
                self.pattern.unmute(track)
            else:
                self.pattern.mute(track)


if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    cv2.namedWindow(WINDOW)
    pattern_detector = LegoPatternDetector()

    while True:
        success, frame = capture.read()
        if success:
            img = pattern_detector.process_image(frame)
            cv2.imshow(WINDOW, img)
        if cv2.waitKey(1) == 27:
            break
