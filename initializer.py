import json

import cv2

WINDOW = 'hello'


class Initializer(object):
    def __init__(self):
        self.rect = []
        self.capture = cv2.VideoCapture(0)

        def on_mouse(event, x, y, unused, user_data):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.click(x, y)

        cv2.namedWindow(WINDOW)
        cv2.setMouseCallback(WINDOW, on_mouse)

    def click(self, x, y):
        self.rect.append([x, y])

    def run(self):
        while len(self.rect) < 4:
            success, frame = self.capture.read()
            if success:
                cv2.imshow(WINDOW, frame)
            if cv2.waitKey(100) != -1:
                break


if __name__ == '__main__':
    initializer = Initializer()
    initializer.run()
    with open('rect.json', 'w') as f:
        json.dump(initializer.rect, f)
