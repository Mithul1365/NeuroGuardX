import cv2


class Display:

    @staticmethod
    def draw(frame, data):

        # -----------------------------
        # Colors
        # -----------------------------
        if data["status"] == "SAFE":
            color = (0, 255, 0)

        elif data["status"] == "WARNING":
            color = (0, 255, 255)

        else:
            color = (0, 0, 255)

        # -----------------------------
        # Driver
        # -----------------------------
        cv2.putText(
            frame,
            "DRIVER DETECTED",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # -----------------------------
        # EAR
        # -----------------------------
        cv2.putText(
            frame,
            f"EAR : {data['ear']:.2f}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        # -----------------------------
        # Status
        # -----------------------------
        cv2.putText(
            frame,
            f"Status : {data['status']}",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        # -----------------------------
        # Head
        # -----------------------------
        cv2.putText(
            frame,
            f"Head : {data['head']}",
            (20, 140),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        # -----------------------------
        # Blink
        # -----------------------------
        cv2.putText(
            frame,
            f"Blinks : {data['blink']}",
            (20, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # -----------------------------
        # Yawn
        # -----------------------------
        cv2.putText(
            frame,
            f"Yawn : {data['yawn']}",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 255),
            2
        )

        # -----------------------------
        # Face
        # -----------------------------
        cv2.putText(
            frame,
            f"Face : {data['face_status']}",
            (20, 230),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # -----------------------------
        # Risk
        # -----------------------------
        cv2.putText(
            frame,
            f"Risk : {data['risk']}%",
            (20, 260),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        return frame