import cv2


class Camera:

    def __init__(self):

        self.cap = cv2.VideoCapture(0)

        # Camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Reduce camera buffer delay
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def get_frame(self):

        success, frame = self.cap.read()

        if not success:
            return None

        # Mirror camera
        frame = cv2.flip(frame, 1)

        return frame

    def release(self):

        self.cap.release()