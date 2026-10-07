import cv2
import numpy as np


class NightMode:

    @staticmethod
    def get_brightness(frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        return np.mean(gray)

    @staticmethod
    def enhance(frame):

        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=2.5,
            tileGridSize=(8, 8)
        )

        l = clahe.apply(l)

        lab = cv2.merge((l, a, b))

        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)