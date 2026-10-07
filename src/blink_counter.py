class BlinkCounter:

    def __init__(self):

        self.blinks = 0
        self.eye_closed = False
        self.closed_frames = 0

        self.EAR_THRESHOLD = 0.18
        self.MIN_CLOSED_FRAMES = 2

    def update(self, ear):

        if ear < self.EAR_THRESHOLD:

            self.closed_frames += 1

            if self.closed_frames >= self.MIN_CLOSED_FRAMES:
                self.eye_closed = True

        else:

            if self.eye_closed:

                self.blinks += 1

            self.eye_closed = False
            self.closed_frames = 0

        return self.blinks