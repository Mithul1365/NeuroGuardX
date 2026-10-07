class FacePredictor:

    def __init__(self):

        self.last_landmarks = None
        self.missed_frames = 0

    def update(self, landmarks):

        if landmarks is not None:

            self.last_landmarks = landmarks
            self.missed_frames = 0

            return landmarks, "VISIBLE"

        self.missed_frames += 1

        if self.last_landmarks is not None and self.missed_frames <= 15:

            return self.last_landmarks, "TRACKING"

        return None, "LOST"