import math


class EyeValidator:

    @staticmethod
    def distance(p1, p2):

        return math.sqrt(
            (p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2
        )

    @staticmethod
    def validate(left_eye, right_eye):

        # Eye Width

        left_width = EyeValidator.distance(
            left_eye[0],
            left_eye[3]
        )

        right_width = EyeValidator.distance(
            right_eye[0],
            right_eye[3]
        )

        # Very small width means eye detection is unreliable

        if left_width < 15:
            return False

        if right_width < 15:
            return False

        return True