# NEUROGUARD X

### Low-Cost Edge-AI Retrofit Driver State Monitoring and Safety Event Recording System for Commercial Trucks

NeuroGuard X is a real-time, non-intrusive Edge-AI driver monitoring system designed to detect driver drowsiness, fatigue, and loss of attention. The system uses computer vision and multiple driver-state indicators to classify risk and provide timely safety alerts.

## 🚗 Project Overview

Driver fatigue and drowsiness can significantly reduce reaction time and situational awareness, increasing the risk of road accidents. NeuroGuard X provides a low-cost solution that can be retrofitted into existing commercial vehicles using a driver-facing camera and an edge-computing device.

The software analyzes facial landmarks and multiple behavioral indicators in real time to determine the driver's state.

## 🎯 Objectives

- Real-time monitoring of driver alertness
- Detect eye closure and prolonged eye closure
- Measure Eye Aspect Ratio (EAR)
- Analyze PERCLOS for fatigue estimation
- Detect yawning and microsleep events
- Monitor driver head direction and pose
- Classify driver risk as SAFE, WARNING, or CRITICAL
- Provide real-time audio safety alerts
- Record safety events for post-drive analysis
- Generate automated reports and risk visualizations

## 🧠 Key Features

- Facial landmark detection using MediaPipe
- Eye Aspect Ratio (EAR) calculation
- Blink and prolonged-eye-closure detection
- PERCLOS-based fatigue analysis
- Yawning detection
- Microsleep detection
- 3D head-pose estimation
- Multi-indicator risk assessment
- Day/Night monitoring support
- Multilingual voice alerts
- Driver login and monitoring
- Event logging
- Graph generation
- Automated PDF reporting

## ⚙️ Technology Stack

- Python
- OpenCV
- MediaPipe
- NumPy
- Computer Vision
- Edge AI
- Real-time Signal Analysis
- PDF Report Generation

## 🔄 System Workflow

Camera Input  
↓  
Face Detection & Facial Landmarks  
↓  
EAR / Blink Analysis  
↓  
PERCLOS Analysis  
↓  
Yawning & Microsleep Detection  
↓  
Head Pose Analysis  
↓  
Risk Assessment Engine  
↓  
SAFE / WARNING / CRITICAL  
↓  
Audio Alert + Event Logging + Reporting

## 📊 Risk Classification

| Risk Level | Description |
|------------|-------------|
| SAFE | Driver appears alert |
| WARNING | Early signs of drowsiness or distraction detected |
| CRITICAL | Severe drowsiness or unsafe driver state detected |

## 🗂️ Project Structure

```text
NeuroGuardX/
│
├── assets/
│   └── face_landmarker.task
│
├── src/
│   ├── main.py
│   ├── camera.py
│   ├── face_landmarker.py
│   ├── face_monitor.py
│   ├── face_tracker.py
│   ├── face_tracker_cv.py
│   ├── ear.py
│   ├── ear_filter.py
│   ├── blink_counter.py
│   ├── perclos.py
│   ├── yawning.py
│   ├── head_pose.py
│   ├── head_pose_3d.py
│   ├── risk_engine.py
│   ├── voice_alert.py
│   ├── logger.py
│   ├── graph_generator.py
│   └── report_generator.py
│
├── requirements.txt
├── README.md
└── .gitignore
