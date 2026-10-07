from ear import EARCalculator
from blink_counter import BlinkCounter
from head_pose import HeadPose
from yawning import YawnDetector
from face_monitor import FaceMonitor
from risk_engine import RiskEngine


class Detector:

    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]
    MOUTH = [13, 14, 78, 308]

    def __init__(self):

        self.blink = BlinkCounter()
        self.face_monitor = FaceMonitor()
        self.risk = RiskEngine()

    def process(self, landmarks, width, height):

        face_status = self.face_monitor.update(
            landmarks is not None
        )

        if landmarks is None:

            return {
                "face_status": face_status
            }

        # -------------------------
        # Left Eye
        # -------------------------

        left_eye = []

        for index in self.LEFT_EYE:

            point = landmarks[index]

            left_eye.append((
                point.x * width,
                point.y * height
            ))

        # -------------------------
        # Right Eye
        # -------------------------

        right_eye = []

        for index in self.RIGHT_EYE:

            point = landmarks[index]

            right_eye.append((
                point.x * width,
                point.y * height
            ))

        # -------------------------
        # EAR
        # -------------------------

        left_ear = EARCalculator.calculate(left_eye)

        right_ear = EARCalculator.calculate(right_eye)

        ear = (left_ear + right_ear) / 2

        blink_count = self.blink.update(ear)

        # -------------------------
        # Mouth
        # -------------------------

        mouth = []

        for index in self.MOUTH:

            point = landmarks[index]

            mouth.append((
                point.x * width,
                point.y * height
            ))

        mar = YawnDetector.calculate(mouth)

        yawn = YawnDetector.detect(mar)

        # -------------------------
        # Head
        # -------------------------

        head = HeadPose.get_direction(
            landmarks
        )

        # -------------------------
        # Risk
        # -------------------------

        risk_score, status = self.risk.update(

            ear,

            head,

            yawn,

            face_status

        )

        return {

            "ear": ear,

            "blink": blink_count,

            "head": head,

            "yawn": yawn,

            "face_status": face_status,

            "risk": risk_score,

            "status": status

        }