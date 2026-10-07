import math


class YawnDetector:

    @staticmethod
    def distance(p1, p2):

        return math.sqrt(
            (p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2
        )

    @staticmethod
    def calculate(mouth):

        top = YawnDetector.distance(mouth[0], mouth[1])

        width = YawnDetector.distance(mouth[2], mouth[3])

        if width == 0:
            return 0

        return top / width

    @staticmethod
    def detect(mar):

        if mar > 0.60:
            return "YES"

        return "NO"