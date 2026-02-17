from flask import Flask, Response, render_template, jsonify
import cv2
from ultralytics import YOLO
import os
import time
import smtplib
from email.message import EmailMessage
import threading
import numpy as np
from dotenv import load_dotenv
from playsound import playsound
import atexit

# LOAD ENV
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

app = Flask(__name__)
os.makedirs("evidence", exist_ok=True)

model = YOLO("yolov8n.pt")

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# GLOBAL STATE
last_email_time = 0
person_present = False
intruder_count = 0
last_detection_time = "None"
email_status = "No alerts yet"

EMAIL_COOLDOWN = 180


# ================= EMAIL =================
def send_email(image_path):
    global email_status

    try:
        msg = EmailMessage()
        msg['Subject'] = "🚨 INTRUDER ALERT!"
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg.set_content("Intruder detected by AI Surveillance System.")

        with open(image_path, 'rb') as f:
            msg.add_attachment(
                f.read(),
                maintype='image',
                subtype='jpeg',
                filename='intruder.jpg'
            )

        with smtplib.SMTP_SSL(
                'smtp.gmail.com',
                465,
                timeout=20) as smtp:

            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)

        email_status = "✅ Email Sent"

        print("✅ EMAIL SENT")

    except Exception as e:
        email_status = "❌ Email Failed"
        print("EMAIL ERROR:", e)


# ================= SOUND =================
def play_alert():
    try:
        threading.Thread(
            target=playsound,
            args=("alarm.wav",),
            daemon=True
        ).start()
    except:
        pass


# ================= VIDEO =================
def generate_frames():

    global last_email_time
    global person_present
    global intruder_count
    global last_detection_time

    while True:

        success, frame = camera.read()

        if not success:
            frame = np.zeros((480,640,3), dtype="uint8")
            cv2.putText(frame,"CAMERA OFFLINE",
                        (150,240),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,(0,0,255),2)

        results = model(frame, classes=[0], conf=0.6)
        annotated = results[0].plot()

        person_detected = len(results[0].boxes) > 0

        if person_detected and not person_present:

            intruder_count += 1
            last_detection_time = time.strftime("%H:%M:%S")

            print("🚨 INTRUDER DETECTED")

            image_path = f"evidence/intruder_{int(time.time())}.jpg"
            cv2.imwrite(image_path, annotated)

            if time.time() - last_email_time > EMAIL_COOLDOWN:
                threading.Thread(
                    target=send_email,
                    args=(image_path,),
                    daemon=True
                ).start()

                last_email_time = time.time()

            play_alert()
            person_present = True

        elif not person_detected:
            person_present = False

        if person_detected:
            cv2.putText(
                annotated,
                "!!! INTRUDER ALERT !!!",
                (80,80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,(0,0,255),3
            )

        ret, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame_bytes + b'\r\n')


# ================= ROUTES =================

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# 🔥 LIVE STATUS API
@app.route('/status')
def status():
    return jsonify({
        "intruders": intruder_count,
        "last_detection": last_detection_time,
        "email_status": email_status
    })


@atexit.register
def cleanup():
    camera.release()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
