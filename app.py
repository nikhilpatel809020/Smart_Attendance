import streamlit as st
import os
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Smart Attendance System")

if not os.path.exists("Images"):
    os.makedirs("Images")

if not os.path.exists("students.csv"):
    with open("students.csv", "w") as f:
        f.write("Roll,Name\n")

if not os.path.exists("Attendance.csv"):
    with open("Attendance.csv", "w") as f:
        f.write("Roll,Date,Time\n")

st.title("📚 Smart Attendance System")

menu = st.sidebar.selectbox(
    "Menu",
    ["New Registration", "Mark Attendance", "View Attendance"]
)

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

            with open(f"Images/{roll}.jpg", "wb") as f:
                f.write(uploaded_file.getbuffer())

            with open("students.csv", "a") as f:
                f.write(f"{roll},{name}\n")

            st.success("Student Registered Successfully")

elif menu == "Mark Attendance":

    st.subheader("Mark Attendance")

    roll = st.text_input("Enter Roll Number")

    if st.button("Mark Present"):

        if not roll:
            st.error("Enter Roll Number")

        else:
            now = datetime.now()

            with open("Attendance.csv", "a") as f:
                f.write(
                    f"{roll},{now.date()},{now.strftime('%H:%M:%S')}\n"
                )

            st.success("Attendance Marked Successfully")

elif menu == "View Attendance":

    st.subheader("Attendance Records")

    try:
        df = pd.read_csv("Attendance.csv")
        st.dataframe(df)
    except:
        st.warning("No Attendance Records Found")