from collections import deque


class PERCLOS:

    def __init__(self, threshold=0.16,window_size=150):
        """
        threshold   : EAR below this = eye closed
        window_size : Number of frames to consider
                      (1800 ≈ 60 sec @ 30 FPS)
        """
        self.threshold = threshold
        self.window = deque(maxlen=window_size)

    def update(self, ear):

        if ear < self.threshold:
            self.window.append(1)
        else:
            self.window.append(0)

        if len(self.window) == 0:
            return 0

        return round((sum(self.window) / len(self.window)) * 100, 1)
    

    