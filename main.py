import cv2
import face_recognition
import numpy as np
import os
import pyttsx3
from datetime import datetime

# -------------------------------
# Folders Setup
# -------------------------------
path = 'Images'

if not os.path.exists('Captured'):
    os.makedirs('Captured')

if not os.path.exists('Attendance.csv'):
    with open('Attendance.csv', 'w') as f:
        f.write('Name,Date,Time')

images = []
classNames = []

attendanceMarked = set()

# Voice Engine
engine = pyttsx3.init()

# -------------------------------
# Load Images
# -------------------------------
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')

    if curImg is not None:
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])

# -------------------------------
# Encode Faces
# -------------------------------
def findEncodings(images):
    encodeList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_encodings(img)

        if len(faces) == 0:
            print("No face found in image")
            continue

        encodeList.append(faces[0])

    return encodeList

# -------------------------------
# Mark Attendance
# -------------------------------
def markAttendance(name, img):
    global attendanceMarked

    if name in attendanceMarked:
        return

    attendanceMarked.add(name)

    print(f"Welcome {name}")
    print("Attendance Marked Successfully")

    now = datetime.now()

    photoTime = now.strftime('%d-%m-%Y_%H-%M-%S')

    cv2.imwrite(
        f"Captured/{name}_{photoTime}.jpg",
        img
    )

    engine.say(f"Welcome {name}")
    engine.say("Attendance Marked Successfully")
    engine.runAndWait()

    dateString = now.strftime('%d-%m-%Y')
    timeString = now.strftime('%H:%M:%S')

    with open('Attendance.csv', 'a') as f:
        f.write(f'\n{name},{dateString},{timeString}')

# -------------------------------
# Encode Known Faces
# -------------------------------
print("Encoding Faces...")

encodeListKnown = findEncodings(images)

print("Encoding Complete")

# -------------------------------
# Webcam Start
# -------------------------------
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

while True:

    success, img = cap.read()

    if not success:
        print("Camera not detected")
        break

    imgS = cv2.resize(
        img,
        (0, 0),
        None,
        0.25,
        0.25
    )

    imgS = cv2.cvtColor(
        imgS,
        cv2.COLOR_BGR2RGB
    )

    facesCurFrame = face_recognition.face_locations(imgS)

    encodesCurFrame = face_recognition.face_encodings(
        imgS,
        facesCurFrame
    )

    for encodeFace, faceLoc in zip(
        encodesCurFrame,
        facesCurFrame
    ):

        matches = face_recognition.compare_faces(
            encodeListKnown,
            encodeFace
        )

        faceDis = face_recognition.face_distance(
            encodeListKnown,
            encodeFace
        )

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex] and faceDis[matchIndex] < 0.45:

            name = classNames[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc

            y1 *= 4
            x2 *= 4
            y2 *= 4
            x1 *= 4

            cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.rectangle(
                img,
                (x1, y2 - 35),
                (x2, y2),
                (0, 255, 0),
                cv2.FILLED
            )

            cv2.putText(
                img,
                name,
                (x1 + 6, y2 - 6),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 255, 255),
                2
            )

            markAttendance(name, img)

    cv2.imshow(
        'Smart Attendance System',
        img
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()