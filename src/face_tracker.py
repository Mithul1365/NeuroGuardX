import time


class FaceTracker:

    def __init__(self):

        self.last_seen = time.time()

    def update(self, face_detected):

        current = time.time()

        if face_detected:
            self.last_seen = current
            return "VISIBLE"

        # Keep visible for 2 seconds
        if current - self.last_seen < 2:
            return "VISIBLE"

        return "LOST"