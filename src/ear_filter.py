from collections import deque


class EARFilter:

    def __init__(self, window=5):

        self.values = deque(maxlen=window)

    def update(self, ear):

        # Reject impossible EAR values
        if ear < 0.05 or ear > 0.50:

            if len(self.values) > 0:
                return sum(self.values) / len(self.values)

            return 0.20

        self.values.append(ear)

        return sum(self.values) / len(self.values)