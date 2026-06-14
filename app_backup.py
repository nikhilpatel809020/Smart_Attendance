import streamlit as st
import os
import pandas as pd
from datetime import datetime
import face_recognition
import numpy as np
from streamlit_webrtc import webrtc_streamer

st.set_page_config(page_title="Smart Attendance System")

# Create folders/files
os.makedirs("Images", exist_ok=True)

if not os.path.exists("students.csv"):
    with open("students.csv", "w") as f:
        f.write("Roll,Name\n")

if not os.path.exists("Attendance.csv"):
    with open("Attendance.csv", "w") as f:
        f.write("Roll,Date,Time\n")


# Face Encoding Function
def load_known_faces():
    encodings = []
    names = []

    for file in os.listdir("Images"):
        img_path = os.path.join("Images", file)

        try:
            image = face_recognition.load_image_file(img_path)
            face_encoding = face_recognition.face_encodings(image)

            if len(face_encoding) > 0:
                encodings.append(face_encoding[0])
                names.append(os.path.splitext(file)[0])

        except Exception:
            pass

    return encodings, names


# Duplicate Attendance Check
def already_marked(roll):
    today = str(datetime.now().date())

    try:
        df = pd.read_csv("Attendance.csv")

        existing = df[
            (df["Roll"].astype(str) == str(roll))
            &
            (df["Date"].astype(str) == today)
        ]

        return len(existing) > 0

    except Exception:
        return False


st.title("📚 Smart Attendance System")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "New Registration",
        "Mark Attendance",
        "Face Attendance",
        "View Attendance"
    ]
)

# ---------------- REGISTER ----------------

if menu == "New Registration":

    st.subheader("Register Student")

    name = st.text_input("Student Name")
    roll = st.text_input("Roll Number")

    uploaded_file = st.file_uploader(
        "Upload Student Photo",
        type=["jpg", "jpeg", "png"]
    )

    if st.button("Register Student"):

        if not name or not roll:
            st.error("Enter Name and Roll Number")

        elif uploaded_file is None:
            st.error("Upload Student Photo")

        else:

            image_path = f"Images/{roll}.jpg"

            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with open("students.csv", "a") as f:
                f.write(f"{roll},{name}\n")

            st.success("Student Registered Successfully")


# ---------------- MANUAL ATTENDANCE ----------------

elif menu == "Mark Attendance":

    st.subheader("Manual Attendance")

    roll = st.text_input("Enter Roll Number")

    if st.button("Mark Present"):

        if not roll:
            st.error("Enter Roll Number")

        elif already_marked(roll):
            st.warning("Attendance already marked today")

        else:

            now = datetime.now()

            with open("Attendance.csv", "a") as f:
                f.write(
                    f"{roll},{now.date()},{now.strftime('%H:%M:%S')}\n"
                )

            st.success("Attendance Marked Successfully")


# ---------------- FACE ATTENDANCE ----------------

elif menu == "Face Attendance":

    st.subheader("Live Face Attendance")

    st.info(
        "Webcam test mode is active. "
        "If camera opens successfully, next step will be live face matching."
    )

    webrtc_streamer(
        key="attendance-camera"
    )


# ---------------- VIEW ATTENDANCE ----------------

elif menu == "View Attendance":

    st.subheader("Attendance Records")

    try:

        df = pd.read_csv("Attendance.csv")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.download_button(
            "Download Attendance CSV",
            data=df.to_csv(index=False),
            file_name="Attendance.csv",
            mime="text/csv"
        )

    except Exception:

        st.warning(
            "No Attendance Records Found"
        )