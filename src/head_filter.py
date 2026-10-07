import time


class HeadFilter:

    def __init__(self):

        self.down_start = None

    def update(self, direction):

        now = time.time()

        # Start timer only when head is DOWN
        if direction == "DOWN":

            if self.down_start is None:
                self.down_start = now

            # DOWN for 2 seconds
            if now - self.down_start >= 1.5:
                return "DOWN"

            else:
                return "FORWARD"

        # Reset timer on any other direction
        self.down_start = None

        return direction