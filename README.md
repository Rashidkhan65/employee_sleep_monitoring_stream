# Real-Time Sleep Detection System with Kafka Alerts

![Sleep Detection](https://img.shields.io/badge/Python-3.11-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.7-green)
![Dlib](https://img.shields.io/badge/Dlib-19.24-orange)
![Kafka](https://img.shields.io/badge/Kafka-3.5-red)

## Overview
This project implements a **real-time sleep detection system** using computer vision. It monitors a live camera feed (via RTSP) and detects when a person’s
eyes remain closed beyond a threshold, indicating potential sleep. Upon detection, it sends an alert message to a **Kafka topic**, making it suitable
for integration into monitoring systems for workplaces, drivers, or security applications.

---

## Features
- Real-time eye closure detection using **Dlib facial landmarks**.
- **Eye Aspect Ratio (EAR)** calculation to detect drowsiness.
- Configurable threshold for sleep detection and consecutive frames.
- Sends **Kafka messages** for integration with alert systems.
- Optional live video display for monitoring.

---

## Requirements

- Python 3.8+
- OpenCV
- Dlib
- NumPy
- SciPy
- Kafka-Python
- Running Kafka broker

Install dependencies using:

```bash
pip install opencv-python dlib numpy scipy kafka-python
