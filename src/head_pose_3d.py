import cv2
import numpy as np


class HeadPose3D:

    @staticmethod
    def get_direction(landmarks, frame_width, frame_height):

        # ---------------------------------
        # 2D facial landmark points
        # ---------------------------------

        image_points = np.array([
            (
                landmarks[1].x * frame_width,
                landmarks[1].y * frame_height
            ),      # Nose

            (
                landmarks[152].x * frame_width,
                landmarks[152].y * frame_height
            ),      # Chin

            (
                landmarks[33].x * frame_width,
                landmarks[33].y * frame_height
            ),      # Left Eye

            (
                landmarks[263].x * frame_width,
                landmarks[263].y * frame_height
            ),      # Right Eye

            (
                landmarks[61].x * frame_width,
                landmarks[61].y * frame_height
            ),      # Left Mouth

            (
                landmarks[291].x * frame_width,
                landmarks[291].y * frame_height
            )       # Right Mouth

        ], dtype=np.float64)

        # ---------------------------------
        # Approximate 3D Face Model
        # ---------------------------------

        model_points = np.array([
            (0.0, 0.0, 0.0),          # Nose
            (0.0, -63.6, -12.5),      # Chin
            (-43.3, 32.7, -26.0),     # Left Eye
            (43.3, 32.7, -26.0),      # Right Eye
            (-28.9, -28.9, -24.1),    # Left Mouth
            (28.9, -28.9, -24.1)      # Right Mouth

        ], dtype=np.float64)

        # ---------------------------------
        # Camera Matrix
        # ---------------------------------

        focal_length = frame_width

        center = (
            frame_width / 2,
            frame_height / 2
        )

        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype=np.float64)

        dist_coeffs = np.zeros((4, 1))

        # ---------------------------------
        # Solve PnP
        # ---------------------------------

        success, rotation_vector, translation_vector = cv2.solvePnP(
            model_points,
            image_points,
            camera_matrix,
            dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            return "FORWARD"

        # ---------------------------------
        # Rotation Matrix
        # ---------------------------------

        rotation_matrix, _ = cv2.Rodrigues(
            rotation_vector
        )

        # ---------------------------------
        # Euler Angles
        # ---------------------------------

        angles, _, _, _, _, _ = cv2.RQDecomp3x3(
            rotation_matrix
        )

        pitch = float(angles[0])
        yaw = float(angles[1])
        roll = float(angles[2])

        # ---------------------------------
        # Normalize Pitch
        # ---------------------------------

        if pitch > 90:
            pitch -= 180

        elif pitch < -90:
            pitch += 180

        # ---------------------------------
        # HEAD LEFT / RIGHT
        # ---------------------------------

        if yaw > 20:
            return "RIGHT"

        elif yaw < -20:
            return "LEFT"

        # ---------------------------------
        # HEAD DOWN
        # ---------------------------------

        # IMPORTANT:
        # Normal straight head should NOT
        # be classified as DOWN.
        #
        # Only significant downward pitch
        # should trigger DOWN.

        if pitch > 15:
            return "DOWN"

        # ---------------------------------
        # NORMAL
        # ---------------------------------

        return "FORWARD"