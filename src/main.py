import cv2
import time
import os
from risk_engine import RiskEngine
from camera import Camera
from face_landmarker import FaceLandmarkerAI
from ear import EARCalculator
from voice_alert import VoiceAlert
from head_pose_3d import HeadPose3D
from blink_counter import BlinkCounter
from yawning import YawnDetector
from face_monitor import FaceMonitor
from logger import DriverLogger
from ear_filter import EARFilter
from eye_validator import EyeValidator
from head_filter import HeadFilter
from face_tracker_cv import FaceTrackerCV
from perclos import PERCLOS
from settings import load_language
from night_mode import NightMode
from datetime import datetime
from report_generator import ReportGenerator
from graph_generator import GraphGenerator



LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [13, 14, 78, 308]


camera = Camera()

ai = FaceLandmarkerAI()
risk = RiskEngine()
voice = VoiceAlert("english")
blink = BlinkCounter()

face_monitor = FaceMonitor()
logger = DriverLogger()
last_log_time = 0
ear_filter = EARFilter()
head_filter = HeadFilter()
perclos = PERCLOS()
tracker = FaceTrackerCV()
missed_frames = 0
fps = 0
last_head_direction = "FORWARD"
last_face_center_y = None
tracked_head_down = False
prev_time = time.time()
start_time = time.time()
os.makedirs("screenshots", exist_ok=True)
last_capture = 0
last_status = "SAFE"
critical_screenshot = None

while True:
    frame = camera.get_frame()
    if frame is None:
            break
    brightness = NightMode.get_brightness(frame)

    night_mode = False

    if brightness < 60:

      frame = NightMode.enhance(frame)

      night_mode = True

    
    current_time = time.time()
    fps = int(1 / (current_time - prev_time))
    elapsed = int(time.time() - start_time)

    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60
    prev_time = current_time
    frame = cv2.resize(frame, (1280,720))
    dashboard = frame.copy()
    now = datetime.now()

    overlay = dashboard.copy()

    cv2.rectangle(
        overlay,
        (0,0),
        (320,720),
        (0,0,0),
        -1
    )

    cv2.addWeighted(
        overlay,
        0.55,
        dashboard,
        0.45,
        0,
        dashboard
    )
    


    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    raw_landmarks = ai.get_landmarks(rgb)

# Default values
    landmarks = raw_landmarks
    tracking_status = "LOST"

    if raw_landmarks is not None:
       missed_frames = 0

       landmarks = raw_landmarks
       tracking_status = "VISIBLE" 
       

       h, w, _ = frame.shape

       xs = [lm.x for lm in landmarks]
       ys = [lm.y for lm in landmarks]

       xmin = int(min(xs) * w)
       xmax = int(max(xs) * w)
       ymin = int(min(ys) * h)
       ymax = int(max(ys) * h)

       bbox = (
          xmin,
           ymin,
          xmax - xmin,
          ymax - ymin
      )
       
       face_width = xmax - xmin
       face_height = ymax - ymin
       if face_width < 120 or face_height < 120:
          tracking_status = "LOST"
          landmarks = None
       tracker.init(frame, bbox)
          
    else:

       missed_frames += 1

       # ---------------------------------
       # Try OpenCV tracker
       # ---------------------------------

       if missed_frames >= 5:

         success, bbox = tracker.update(frame)

         if success:

            tracking_status = "TRACKING"

            x, y, w_box, h_box = map(int, bbox)

            # ---------------------------------
            # Estimate face center
            # ---------------------------------

            face_center_x = x + (w_box / 2)
            face_center_y = y + (h_box / 2)

            # ---------------------------------
            # Extreme DOWN fallback
            #
            # When driver bends head deeply,
            # MediaPipe may lose landmarks.
            # Use tracked face position as fallback.
            # ---------------------------------

            if face_center_y > frame.shape[0] * 0.58:

                tracked_head_down = True

            else:

                tracked_head_down = False

            # ---------------------------------
            # Draw tracker box
            # ---------------------------------

            cv2.rectangle(
                dashboard,
                (x, y),
                (x + w_box, y + h_box),
                (0,255,255),
                3
            )

         else:

            tracking_status = "LOST"

            tracked_head_down = False

            tracker.reset()

       else:

         tracking_status = "LOST"

         tracked_head_down = False


    face_status = face_monitor.update(
        tracking_status == "VISIBLE"
    )

    #print(landmarks is not None, face_status)
    #print("Landmarks:", landmarks is not None) 
    #print("Face Status:", face_status)
    if landmarks is not None:
        # Draw all landmarks
        for landmark in landmarks:

              x = int(landmark.x * w)
              y = int(landmark.y * h)

              cv2.circle(
                dashboard,
                (x, y),
                2,
                (0, 255, 0),
                -1
            )

        # -----------------------------
        # Get Left Eye Points
        # -----------------------------
        left_eye = []

        for index in LEFT_EYE:
            point = landmarks[index]

            left_eye.append((
                point.x * w,
                point.y * h
            ))

        # -----------------------------
        # Get Right Eye Points
        # -----------------------------
        right_eye = []

        for index in RIGHT_EYE:
            point = landmarks[index]

            right_eye.append((
                point.x * w,
                point.y * h
            ))

        # -----------------------------
        # Calculate EAR
        # -----------------------------
        left_ear = EARCalculator.calculate(left_eye)
        right_ear = EARCalculator.calculate(right_eye)

        ear = (left_ear + right_ear) / 2
        

       
        ear = ear_filter.update(ear)
        eye_valid = EyeValidator.validate(
           left_eye,
           right_eye
        )

        if not eye_valid:
           ear = 0.25
        blink_count = blink.update(ear)
        perclos_value = perclos.update(ear)

# Mouth
        mouth = []

        for index in MOUTH:
            point = landmarks[index]
            mouth.append((point.x * w, point.y * h))

        mar = YawnDetector.calculate(mouth)
        yawn = YawnDetector.detect(mar)

# Head
        head_direction = HeadPose3D.get_direction(
           landmarks,
            w,
            h
      )

        head_direction = head_filter.update(head_direction)
        last_head_direction = head_direction

# Risk Engine
        risk_score, status = risk.update(
          ear,
          head_direction,
          yawn,
          face_status,
         perclos_value
       )  
        #print(f"Risk = {risk_score} | Status = {status}")
        cv2.putText(
             dashboard,
             f"Running : {hours:02}:{minutes:02}:{seconds:02}",
             (30,380),
              cv2.FONT_HERSHEY_SIMPLEX,
              0.8,
              (255,255,255),
               2
           )

        cv2.putText(
            dashboard,
            f"Time : {now.strftime('%I:%M:%S %p')}",
            (30,590),
             cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
             (255,255,255),
            2
     )
        # -----------------------------
# Driver Attention Score
# -----------------------------

        attention = max(0, 100 - risk_score)

        
        if status == "SAFE":
           color = (0, 255, 0)

        elif status == "WARNING":
           color = (0, 255, 255)

        else:
          color = (0, 0, 255)
        # FACE DETECTED
        # -----------------------------
# Title
# -----------------------------
        cv2.putText(
            dashboard,
           "NeuroGuard X",
           (30, 40),
           cv2.FONT_HERSHEY_SIMPLEX,
           1,
           (255, 255, 255),
           2
         )

# -----------------------------
# Subtitle
# -----------------------------
        cv2.putText(
            dashboard,
            "AI Driver Monitoring",
            (30, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
             0.55,
            (180, 180, 180),
             1
            )

# -----------------------------
# Status Badge
# -----------------------------
        cv2.putText(
            dashboard,
            f"Status : {status}",
            (30, 100),
             cv2.FONT_HERSHEY_SIMPLEX,
             0.8,
             color,
             2
            )

        # EAR
        cv2.putText(
           dashboard,
            f"Attention : {attention}%",
            (30,410),
            cv2.FONT_HERSHEY_SIMPLEX,
             0.8,
             (255,255,255),
             2
          )
        # -----------------------------
# Risk Progress Bar
# -----------------------------

# Border
        cv2.rectangle(
            dashboard,
            (30, 490),
            (280, 515),
            (255, 255, 255),
             2
         )

# Fill Width
        if status == "CRITICAL":
             bar_width = 250
        else:
              bar_width = int((risk_score / 100) * 250)
        
# Bar Color
        if risk_score < 40:
           bar_color = (0, 255, 0)

        elif risk_score < 70:
             bar_color = (0, 255, 255)

        else:
            bar_color = (0, 0, 255)

# Filled Bar
        cv2.rectangle(
           dashboard,
           (30, 490),
           (30 + bar_width, 515),
           bar_color,
           -1
         )
        
        cv2.putText(
           dashboard,
           "Risk Level",
           (30, 470),
           cv2.FONT_HERSHEY_SIMPLEX,
           0.6,
           (255, 255, 255),
            1
         )

        
        cv2.putText(
            dashboard,
            f"Risk : {risk_score}%",
            (30, 440),
             cv2.FONT_HERSHEY_SIMPLEX,
             0.8,
             (0, 255, 255),
              2
          )
        

        cv2.putText(
          dashboard,
         f"FPS : {fps}",
           (30, 140),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
          (0, 255, 0),
           2
        )
        cv2.putText(
            dashboard,
            f"EAR : {ear:.2f}",
            (30, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )
        cv2.putText(
            dashboard,
            f"PERCLOS : {perclos_value:.1f}%",
            (30, 320),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )
        if night_mode:
          mode = "NIGHT"
          mode_color = (0, 255, 255)
        else:
         mode = "DAY"
         mode_color = (0, 255, 0)

        cv2.putText(
          dashboard,
          f"Mode : {mode}",
          (30, 350),
          cv2.FONT_HERSHEY_SIMPLEX,
          0.8,
         mode_color,
         2
        )
        cv2.putText(
            dashboard,
            f"Head : {head_direction}",
             (30, 200),
             cv2.FONT_HERSHEY_SIMPLEX,
              0.8,
             (255, 255, 0),
              2
        )
        cv2.putText(
             dashboard,
             f"Blinks : {blink_count}",
             (30,230),
             cv2.FONT_HERSHEY_SIMPLEX,
              0.8,
            (255,255,255),
              2
        )
        cv2.putText(
            dashboard,
            f"Yawn : {yawn}",
            (30, 260),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 255),
             2
        )
        if tracking_status == "VISIBLE":
           face_color = (0,255,0)
           face_text = "VISIBLE"

        elif tracking_status == "TRACKING":
           face_color = (0,255,255)
           face_text = "TRACKING"

        else:
           face_color = (0,0,255)
           face_text = "LOST"
        cv2.putText(
             dashboard,
             f"Face : {face_text}",
             (30, 290),
              cv2.FONT_HERSHEY_SIMPLEX,
              0.8,
              face_color,
              2
          )

        # Speak only when status changes

        # -----------------------------
# Voice Alerts
# -----------------------------
        
        if status == "WARNING":

             if last_status != "WARNING":
                  print("WARNING START")

                  voice.speak_warning()
             last_status = "WARNING"


        elif status == "CRITICAL":

            if last_status != "CRITICAL":
                 print("CRITICAL START")

                 voice.speak_critical()

            current = time.time()

            if current - last_capture >= 5:

               filename = time.strftime(
                     "screenshots/critical_%Y%m%d_%H%M%S.png"
               )

               cv2.imwrite(filename, dashboard)

               print("Screenshot Saved :", filename)
               critical_screenshot = filename
               last_capture = current

            last_status = "CRITICAL"


        else:
           last_status = "SAFE"
        # Audio queue update
        voice.update()   
     # -----------------------------
# Save Driver Data
# -----------------------------
        current_time = time.time()
        if current_time - last_log_time >= 1:
        
           logger.log(
               ear,
               head_direction,
                yawn,
               face_status,
               attention,
               risk_score,
               status
            ) 
           last_log_time = current_time    
    if  tracking_status == "TRACKING":

             cv2.putText(
               dashboard,
               "Face : TRACKING",
               (30,290),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2
           )

             cv2.putText(
               dashboard,
               "TRACKING FACE",
               (30,330),
               cv2.FONT_HERSHEY_SIMPLEX,
               1,
               (0,255,255),
               2
           )     
    elif face_status == "MISSING":

         cv2.putText(
          dashboard,
          "Face : LOST",
          (30,290),
          cv2.FONT_HERSHEY_SIMPLEX,
          0.8,
          (0,0,255),
          2
      )

         cv2.putText(
          dashboard,
          "DRIVER NOT VISIBLE",
          (30,330),
          cv2.FONT_HERSHEY_SIMPLEX,
          1,
          (0,0,255),
          3
      )

         if status != "CRITICAL":
          voice.speak_missing()
            
    cv2.imshow("NeuroGuard X", dashboard)

    if cv2.waitKey(1) & 0xFF == ord("q"):
       break
# -----------------------------
# PDF Report
# -----------------------------
data = {
    "Running Time": f"{hours:02}:{minutes:02}:{seconds:02}",
    "Attention": f"{attention}%",
    "Risk": f"{risk_score}%",
    "Status": status,
    "PERCLOS": f"{perclos_value:.1f}%",
    "Blinks": blink_count,
    "Head": head_direction,
    "Yawn": yawn,
    "Mode": mode
}

pdf = ReportGenerator.generate(
    data,
    critical_screenshot
)

print("Report Saved :", pdf)
GraphGenerator.generate()
camera.release()
cv2.destroyAllWindows()
