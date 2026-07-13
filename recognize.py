import cv2
import sqlite3
import json
from datetime import datetime

# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# Load labels
with open("labels.json", "r") as f:
    labels = json.load(f)

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
if face_cascade.empty():
    print("❌ Failed to load Haar Cascade")
    exit()

print("✅ Haar Cascade loaded successfully")

# Prevent duplicate attendance in one session
marked_students = set()

camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()

    if not success:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        label, confidence = recognizer.predict(face)

        # Lower confidence = better match
        if confidence < 80:

            name = labels[str(label)]

            if name not in marked_students:

                conn = sqlite3.connect("attendance.db")
                cursor = conn.cursor()

                now = datetime.now()

                date = now.strftime("%d-%m-%Y")
                time = now.strftime("%H:%M:%S")

                cursor.execute(
                    """
                    INSERT INTO attendance(student_name, date, time)
                    VALUES (?, ?, ?)
                    """,
                    (name, date, time)
                )

                conn.commit()
                conn.close()

                marked_students.add(name)

                print(f"✅ Attendance marked for {name}")

            color = (0, 255, 0)

        else:
            name = "Unknown"
            color = (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        cv2.putText(
            frame,
            f"{name} ({confidence:.1f})",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    cv2.imshow("AI Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()