import time


class FaceMonitor:

    def __init__(self):

        self.last_seen = time.time()

    def update(self, face_detected):

        if face_detected:

            self.last_seen = time.time()

            return "VISIBLE"

        elapsed = time.time() - self.last_seen

        # Temporary face loss
        if elapsed <= 2:

            return "LOST"

        # Face missing for more than 5 seconds
        if elapsed > 5:

            return "MISSING"

        # Between 2 and 5 seconds
        return "LOST"