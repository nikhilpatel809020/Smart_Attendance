import streamlit as st
import os
import pandas as pd
from datetime import datetime
import face_recognition
import numpy as np
import tempfile
import time

st.set_page_config(page_title="Smart Attendance System")

# Create folders/files
os.makedirs("Images", exist_ok=True)
os.makedirs(
    "Streamlit_Captured",
    exist_ok=True
)

if not os.path.exists("students.csv"):
    with open("students.csv", "w") as f:
        f.write("RollNo,Name\n")

if not os.path.exists("Attendance.csv"):
    with open("Attendance.csv", "w") as f:
        f.write("Roll,Name,Date,Time,Photo\n")


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
            (df["RollNo"].astype(str) == str(roll))
            &
            (df["Date"].astype(str) == today)
        ]

        return len(existing) > 0

    except Exception:
        return False


st.title("📚 Smart Attendance System")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Menu",
        [
            "New Registration",
            "Face Attendance",
            "View Attendance",
            "Logout"
        ]
    )

else:

    menu = st.sidebar.selectbox(
        "Menu",
        [
            "Face Attendance",
            "Admin Login"
        ]
    )
    if menu == "Admin Login":

        st.subheader("Admin Login")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        try:

            admin_df = pd.read_csv(
                "admin.csv"
            )

            row = admin_df[
                (
                    admin_df["Username"]
                    == username
                )
                &
                (
                    admin_df["Password"]
                    == password
                )
            ]

            if len(row) > 0:

                st.session_state.logged_in = True

                st.success(
                    "Login Successful"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

        except Exception:

            st.error(
                "admin.csv not found"
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
        students_df = pd.read_csv( 
            "students.csv"
        )
        if str(roll) in (
            students_df["RollNo"]
            .astype(str)
            .values
        ):
            
            st.error(
                "Roll Number Alredy Registered"
            )
            st.stop()

        if not name or not roll:

            st.error(
                "Enter Name and Roll Number"
            )

        elif uploaded_file is None:

            st.error(
                "Upload Student Photo"
            )

        else:

            image_path = (
                f"Images/{roll}.jpg"
            )

            with open(
                image_path,
                "wb"
            ) as f:

                f.write(
                    uploaded_file.getbuffer()
                )

            with open(
                "students.csv",
                "a"
            ) as f:

                f.write(
                    f"{roll},{name}\n"
                )

            st.success(
                "Student Registered Successfully"
            )

            time.sleep(2)

            st.rerun()

# ---------------- FACE ATTENDANCE ----------------

elif menu == "Face Attendance":

    st.subheader("Face Recognition Attendance")

    picture = st.camera_input("Take a Picture")

    if picture:

        st.success("Photo Captured Successfully")

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as tmp_file:

            tmp_file.write(
                picture.getvalue()
            )

            temp_path = tmp_file.name

        try:

            uploaded_image = face_recognition.load_image_file(
                temp_path
            )

            uploaded_encodings = (
                face_recognition.face_encodings(
                    uploaded_image
                )
            )

            if len(uploaded_encodings) == 0:

                st.error("No Face Detected")
            elif len(uploaded_encodings) > 1:
                st.error(
                    "Multiple Face Detected. Please capture only one person."
                )
                

            else:

                uploaded_encoding = uploaded_encodings[0]

                found = False

                for file in os.listdir("Images"):

                    path = os.path.join(
                        "Images",
                        file
                    )

                    try:

                        known_image = (
                            face_recognition.load_image_file(
                                path
                            )
                        )

                        known_encodings = (
                            face_recognition.face_encodings(
                                known_image
                            )
                        )

                        if len(known_encodings) == 0:
                            continue

                        match = (
                            face_recognition.compare_faces(
                                [known_encodings[0]],
                                uploaded_encoding
                            )
                        )

                        if match[0]:

                            found = True

                            roll_no = os.path.splitext(
                                file
                            )[0]

                            st.success(
                                f"Recognized Roll No: {roll_no}"
                            )

                            student_name = ""

                            try:

                                students_df = pd.read_csv(
                                    "students.csv"
                                )

                                row = students_df[
                                    students_df["RollNo"].astype(str)
                                    == str(roll_no)
                                ]

                                if len(row) > 0:

                                    student_name = (
                                        row.iloc[0]["Name"]
                                    )

                            except:
                                pass

                            filename = (
                                f"{roll_no}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                            )

                            filepath = os.path.join(
                                "Streamlit_Captured",
                                filename
                            )

                            with open(
                                filepath,
                                "wb"
                            ) as img_file:

                                img_file.write(
                                    picture.getvalue()
                                )

                            if not already_marked(
                                roll_no
                            ):

                                now = datetime.now()

                                with open(
                                    "Attendance.csv",
                                    "a"
                                ) as f:

                                    f.write(
                                        f"{roll_no},{student_name},{now.date()},{now.strftime('%H:%M:%S')},{filename}\n"
                                    )

                                st.success(
                                    "Attendance Marked Successfully"
                                )

                            else:

                                st.warning(
                                    "Attendance already marked today"
                                )

                            break

                    except Exception:
                        pass

                if not found:

                    st.error(
                        "Unknown Person"
                    )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )

        finally:

            if os.path.exists(
                temp_path
            ):

                os.remove(
                    temp_path
                )

# ---------------- VIEW ATTENDANCE ----------------

elif menu == "View Attendance":

    st.subheader("Attendance Records")

    search = st.text_input(
        "Search Roll No or Name"
    )

    try:

        df = pd.read_csv(
            "Attendance.csv"
        )

        if search:

            df = df[
                df.astype(str)
                .apply(
                    lambda row:
                    row.str.contains(
                        search,
                        case=False
                    ).any(),
                    axis=1
                )
            ]

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader(
            "Attendance Photos"
        )

        for _, row in df.iterrows():

            photo_path = os.path.join(
                "Streamlit_Captured",
                str(row["Photo"])
            )

            if os.path.exists(
                photo_path
            ):

                st.image(
                    photo_path,
                    caption=f"{row['RollNo']} - {row['Name']}",
                    width=250
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
elif menu == "Logout":

    st.session_state.logged_in = False

    st.success(
        "Logged Out Successfully"
    )

    st.rerun()