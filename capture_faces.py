import cv2
import os
import csv

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
csv_file = "Student_detail.csv"
csv_file = "Student_detail.csv"

# create csv with header if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['student_id', 'student_name'])

student_id = input("Enter the Student Id :").strip()
student_name = input("Enter Student Name : ").strip()

# check for duplicate id
duplicate = False
with open(csv_file, "r", newline='') as file:
    reader = csv.reader(file)
    # skip header if present
    rows = list(reader)
    for row in rows[1:]:
        if len(row) >= 1 and row[0] == student_id:
            duplicate = True
            break

if duplicate:
    print("Student Id Already Exists")
    exit()

with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([student_id, student_name])

# Create folder for the student
path = f"dataset/{student_name}"
os.makedirs(path, exist_ok=True)

camera= cv2.VideoCapture(0)
count=0

while True:
    success, frame = camera.read()

    if not success:
        print("Failed to capture faces")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]

        cv2.imwrite(f"{path}/{student_name}.{student_id}.{count}.jpg", face)

        count += 1

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Capture Faces", frame)

    # Stop after capturing 30 images
    if count >= 30:
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

print(f"{count} images saved for {student_name}")

       
