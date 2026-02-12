from flask import Flask, Response, render_template_string
import cv2
from ultralytics import YOLO
import os
import time

app = Flask(__name__)

# Create evidence folder if not exists
if not os.path.exists("evidence"):
    os.makedirs("evidence")

# Load YOLOv8 model (auto downloads first time)
model = YOLO("yolov8n.pt")

camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        results = model(frame)

        annotated_frame = results[0].plot()

        # Save evidence if objects detected
        if len(results[0].boxes) > 0:
            timestamp = int(time.time())
            cv2.imwrite(f"evidence/detected_{timestamp}.jpg", annotated_frame)

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template_string("""
        <html>
            <head><title>AI Surveillance System</title></head>
            <body>
                <h2>Live Object Detection</h2>
                <img src="/video">
            </body>
        </html>
    """)

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
