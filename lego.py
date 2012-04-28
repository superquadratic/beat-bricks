import cv2

WINDOW_NAME = 'hello'

def global_on_mouse(event, x, y, unknown, lego_player):
    lego_player.on_mouse(event, x, y)

class LegoPlayer(object):
    def __init__(self):
        self.rect = []

        cv2.namedWindow(WINDOW_NAME)
        cv2.setMouseCallback(WINDOW_NAME, global_on_mouse, self)
        self.capture = cv2.VideoCapture(0)

    def on_mouse(self, event, x, y):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.rect) == 4:
                self.rect = []
            self.rect.append((x, y))
            print self.rect

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
