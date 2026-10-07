import cv2


class FaceTrackerCV:

    def __init__(self):

        self.tracker = None
        self.initialized = False

    def init(self, frame, bbox):

        self.tracker = cv2.TrackerKCF_create()

        self.tracker.init(frame, bbox)

        self.initialized = True

    def update(self, frame):

        if not self.initialized:
            return False, None

        success, bbox = self.tracker.update(frame)

        if success:

            x, y, w, h = map(int, bbox)

            return True, (x, y, w, h)

        self.initialized = False

        return False, None

    def reset(self):

        self.initialized = False
        self.tracker = None