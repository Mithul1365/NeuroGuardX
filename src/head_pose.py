class HeadPose:

    @staticmethod
    def get_direction(landmarks):

        nose = landmarks[1]

        left_eye = landmarks[33]
        right_eye = landmarks[263]

        left_mouth = landmarks[61]
        right_mouth = landmarks[291]

        eye_center_x = (left_eye.x + right_eye.x) / 2
        eye_center_y = (left_eye.y + right_eye.y) / 2

        mouth_center_y = (left_mouth.y + right_mouth.y) / 2

        dx = nose.x - eye_center_x

        face_height = mouth_center_y - eye_center_y

        dy_ratio = (nose.y - eye_center_y) / face_height
        #print(f"dx={dx:.3f}  dy={dy_ratio:.3f}")
       # print(f"dx = {dx:.3f}")

        

        # LEFT
        if dx > 0.03:
         return "RIGHT"

        elif dx < -0.03:
           return "LEFT"

        # Deep DOWN only
        elif dy_ratio > 0.90 and abs(dx) < 0.03:
            return "DOWN"
          

        return "FORWARD"