import cv2
import dlib
import time
import numpy as np
from kafka import KafkaProducer
from scipy.spatial import distance as dist

# -----------------------------
# Configuration
# -----------------------------
RTSP_STREAM = "rtsp://username:password@camera_ip:554/stream"
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'sleep_alerts'
EYE_AR_THRESH = 0.25   # Threshold for closed eyes
EYE_AR_CONSEC_FRAMES = 20  # Frames to confirm sleep

# -----------------------------
# Kafka Producer
# -----------------------------
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: str(v).encode('utf-8')
)

# -----------------------------
# Dlib face and landmarks detector
# -----------------------------
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Download from dlib model zoo

def eye_aspect_ratio(eye):
    # Compute euclidean distances
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Grab the indexes of the facial landmarks for the left and right eye
(lStart, lEnd) = (42, 48)
(rStart, rEnd) = (36, 42)

# -----------------------------
# Main Loop
# -----------------------------
cap = cv2.VideoCapture(RTSP_STREAM)
sleep_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        shape_np = np.zeros((68, 2), dtype="int")
        for i in range(0, 68):
            shape_np[i] = (shape.part(i).x, shape.part(i).y)

        leftEye = shape_np[lStart:lEnd]
        rightEye = shape_np[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        if ear < EYE_AR_THRESH:
            sleep_counter += 1
            if sleep_counter >= EYE_AR_CONSEC_FRAMES:
                # Send Kafka alert
                alert_msg = {"alert": "Sleep detected", "timestamp": time.time()}
                producer.send(KAFKA_TOPIC, alert_msg)
                print("[ALERT] Sleep detected, Kafka message sent!")
        else:
            sleep_counter = 0

    # Optional: Display the frame for monitoring
    cv2.imshow("Sleep Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
producer.flush()
