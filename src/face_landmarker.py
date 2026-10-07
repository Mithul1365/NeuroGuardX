import mediapipe as mp


BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions


class FaceLandmarkerAI:

    def __init__(self):

        options = FaceLandmarkerOptions(

            base_options=BaseOptions(
                model_asset_path="../assets/face_landmarker.task"
            ),

            # ---------------------------------
            # VIDEO MODE
            # ---------------------------------

            running_mode=VisionRunningMode.VIDEO,

            num_faces=1,

            # ---------------------------------
            # Detection confidence
            # ---------------------------------

            min_face_detection_confidence=0.30,
            min_face_presence_confidence=0.30,
            min_tracking_confidence=0.30
        )

        self.landmarker = FaceLandmarker.create_from_options(
            options
        )

        # Timestamp for VIDEO mode
        self.timestamp_ms = 0

    # ---------------------------------
    # Detect face
    # ---------------------------------

    def detect(self, rgb_frame):

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        self.timestamp_ms += 1

        result = self.landmarker.detect_for_video(
            mp_image,
            self.timestamp_ms
        )

        return result

    # ---------------------------------
    # Get facial landmarks
    # ---------------------------------

    def get_landmarks(self, rgb_frame):

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        self.timestamp_ms += 1

        result = self.landmarker.detect_for_video(
            mp_image,
            self.timestamp_ms
        )

        if result.face_landmarks:

            return result.face_landmarks[0]

        return None