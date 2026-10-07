class RiskScore:

    def __init__(self):

        self.counter = 0

        self.threshold = 0.20

    def update(self, ear):

        if ear < self.threshold:
            self.counter += 1
        else:
            self.counter = 0

        if self.counter >= 90:
            return "CRITICAL"

        elif self.counter >= 30:
            return "WARNING"

        else:
            return "SAFE"