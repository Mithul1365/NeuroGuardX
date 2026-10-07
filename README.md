# NEUROGUARD X

### Low-Cost Edge-AI Retrofit Driver State Monitoring and Safety Event Recording System for Commercial Trucks

NeuroGuard X is a real-time, non-intrusive Edge-AI based driver monitoring system designed to detect drowsiness, fatigue, and loss of driver attention in commercial vehicles.

The system uses computer vision and multiple driver-state indicators including facial landmarks, Eye Aspect Ratio (EAR), PERCLOS, yawning, microsleep detection, and head-pose analysis to assess the driver's state and provide timely safety alerts.

---

## 🚨 Problem Statement

Driver fatigue, drowsiness, and loss of attention can lead to delayed reactions, reduced awareness, and serious road accidents.

Existing driver monitoring solutions can be expensive and may require specialized vehicle systems. NeuroGuard X aims to provide a low-cost, non-intrusive Edge-AI solution that can be retrofitted into existing commercial vehicles.

---

## 🎯 Objectives

- Develop a real-time Edge-AI system for monitoring driver alertness.
- Detect signs of drowsiness and fatigue using multiple facial indicators.
- Calculate Eye Aspect Ratio (EAR) for eye-state analysis.
- Analyze PERCLOS for prolonged eye closure and fatigue estimation.
- Detect yawning and microsleep events.
- Monitor driver head direction and head pose.
- Classify driver state into SAFE, WARNING, and CRITICAL levels.
- Provide timely audio safety alerts.
- Record safety-related events for post-drive analysis.
- Generate automated reports and risk visualizations.

---

## 🧠 Key Features

### Driver State Monitoring
- Real-time face detection and facial landmark tracking
- Eye Aspect Ratio (EAR) calculation
- Blink detection
- Prolonged eye-closure detection
- PERCLOS analysis
- Yawning detection
- Microsleep detection
- Head-pose and head-direction analysis

### Risk Assessment
The system combines multiple driver-state indicators instead of relying on a single parameter.

Driver risk is classified into:

| Risk Level | Description |
|------------|-------------|
| SAFE | Driver appears alert and attentive |
| WARNING | Early signs of drowsiness or distraction are detected |
| CRITICAL | Severe drowsiness or unsafe driver state is detected |

### Safety & Reporting
- Real-time warning alerts
- Multilingual voice alerts
- Safety-event logging
- Risk analysis and visualization
- Automated report generation
- Day/Night monitoring support

---

## 🔬 Innovation

NeuroGuard X uses a multi-indicator driver-state analysis approach.

Instead of depending on a single measurement, the system combines:

- Eye closure
- Eye Aspect Ratio (EAR)
- PERCLOS
- Yawning
- Microsleep indicators
- Head direction and head pose

These indicators are integrated into a unified risk-assessment pipeline for real-time driver safety monitoring.

---

## ⚙️ Technology Stack

- Python
- OpenCV
- MediaPipe
- NumPy
- Computer Vision
- Edge AI
- Real-Time Signal Analysis
- Data Logging
- Data Visualization
- PDF Report Generation

---

## 🔄 System Workflow

```text
Driver-Facing Camera
        ↓
Face Detection & Facial Landmarks
        ↓
Eye & Face Analysis
        ↓
EAR / Blink Analysis
        ↓
PERCLOS Analysis
        ↓
Yawning & Microsleep Detection
        ↓
Head Pose Analysis
        ↓
Multi-Indicator Risk Assessment
        ↓
SAFE / WARNING / CRITICAL
        ↓
Audio Alert
        ↓
Event Logging & Reporting
