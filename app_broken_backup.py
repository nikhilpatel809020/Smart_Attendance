import streamlit as st
import os
import pandas as pd
from datetime import datetime
import face_recognition
import numpy as np
import tempfile

st.set_page_config(page_title="Smart Attendance System")

# Create folders/files
os.makedirs("Images", exist_ok=True)
os.makedirs(
    "Streamlit_Captured",
    exist_ok=True
)

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

# ---------------- FACE ATTENDANCE ----------------

elif menu == "Face Attendance":

    st.subheader("Face Recognition Attendance")

    picture = st.camera_input("Take a Picture")

    if picture:

        st.success("Photo Captured Successfully")

        st.image(picture)

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

            uploaded_encodings = face_recognition.face_encodings(
                uploaded_image
            )

            if len(uploaded_encodings) == 0:

                st.error("No Face Detected")

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

                            student = (
                                os.path.splitext(
                                    file
                                )[0]
                            )

                            st.success(
                                f"Recognized: {student}"
                       )
                        filename = (
                                f"{student}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                            )

                        filepath = os.path.join(
                                "Streamlit_Captured",
                                filename
                            )

                               with open(filepath, "wb") as f:

                                f.write(
                                    picture.getvalue()
                                )
                            if not already_marked(student):

                                now = datetime.now()

                                with open(
                                    "Attendance.csv",
                                    "a"
                                ) as f:

                                    f.write(
                                        f"{student},{now.date()},{now.strftime('%H:%M:%S')}\n"
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