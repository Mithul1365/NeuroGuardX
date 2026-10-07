from scipy.spatial import distance


class EARCalculator:

    @staticmethod
    def calculate(points):

        A = distance.euclidean(points[1], points[5])

        B = distance.euclidean(points[2], points[4])

        C = distance.euclidean(points[0], points[3])

        ear = (A + B) / (2.0 * C)

        return ear