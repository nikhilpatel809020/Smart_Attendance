import streamlit as st
import cv2
import os
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Smart Attendance System", layout="centered")

# ---------------- FOLDERS SETUP ----------------
if not os.path.exists("Images"):
    os.makedirs("Images")

if not os.path.exists("students.csv"):
    with open("students.csv", "w") as f:
        f.write("Roll,Name\n")

if not os.path.exists("Attendance.csv"):
    with open("Attendance.csv", "w") as f:
        f.write("Roll,Date,Time\n")

# ---------------- TITLE ----------------
st.title("📚 Smart Attendance System")

menu = st.sidebar.selectbox(
    "Select Menu",
    ["New Registration", "Mark Attendance", "View Attendance"]
)

# ---------------- NEW REGISTRATION ----------------
if menu == "New Registration":

    st.subheader("Register New Student")

    name = st.text_input("Enter Name")
    roll = st.text_input("Enter Roll No")

    if st.button("📸 Capture Face"):

        if name == "" or roll == "":
            st.error("Please fill all fields")
        else:
            cam = cv2.VideoCapture(0)

            st.info("Press SPACE to capture image")

            while True:
                ret, frame = cam.read()
                cv2.imshow("Capture Face", frame)

                k = cv2.waitKey(1)

                if k == 32:
                    cv2.imwrite(f"Images/{roll}.jpg", frame)
                    break

            cam.release()
            cv2.destroyAllWindows()

            with open("students.csv", "a") as f:
                f.write(f"{roll},{name}\n")

            st.success("Student Registered Successfully")

# ---------------- MARK ATTENDANCE ----------------
if menu == "Mark Attendance":

    st.subheader("Mark Attendance")

    roll = st.text_input("Enter Roll No")

    if st.button("Mark Present"):

        if roll == "":
            st.error("Enter Roll Number")
        else:
            now = datetime.now()

            with open("Attendance.csv", "a") as f:
                f.write(f"{roll},{now.date()},{now.time()}\n")

            st.success(f"Attendance Marked for Roll {roll}")

# ---------------- VIEW ATTENDANCE ----------------
if menu == "View Attendance":

    st.subheader("Attendance Records")

    if os.path.exists("Attendance.csv"):
        df = pd.read_csv("Attendance.csv")
        st.dataframe(df)
    else:
        st.warning("No data found")