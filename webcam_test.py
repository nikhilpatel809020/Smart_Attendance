import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import cv2
import av
import face_recognition
import os
import numpy as np

st.set_page_config(page_title="Live Face Recognition")

st.title("🎥 Live Face Recognition")

# Load Known Faces
known_encodings = []
known_names = []

if os.path.exists("Images"):
    for file in os.listdir("Images"):

        path = os.path.join("Images", file)

        try:
            image = face_recognition.load_image_file(path)

            encodings = face_recognition.face_encodings(image)

            if len(encodings) > 0:
                known_encodings.append(encodings[0])
                known_names.append(
                    os.path.splitext(file)[0]
                )

        except Exception:
            pass


class FaceProcessor(VideoProcessorBase):

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        rgb = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        face_locations = face_recognition.face_locations(rgb)

        face_encodings = face_recognition.face_encodings(
            rgb,
            face_locations
        )

        for face_encoding, face_loc in zip(
            face_encodings,
            face_locations
        ):

            top, right, bottom, left = face_loc

            name = "Unknown"

            if len(known_encodings) > 0:

                try:

                    matches = face_recognition.compare_faces(
                        known_encodings,
                        face_encoding
                    )

                    distances = face_recognition.face_distance(
                        known_encodings,
                        face_encoding
                    )

                except Exception as e:

                    print("ERROR:", e)

                    matches = []
                    distances = []

                if len(distances) > 0:

                    best_match = np.argmin(
                        distances
                    )

                    if matches[best_match]:

                        name = known_names[
                            best_match
                        ]

            cv2.rectangle(
                img,
                (left, top),
                (right, bottom),
                (0, 255, 0),
                2
            )

            cv2.putText(
                img,
                name,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )


webrtc_streamer(
    key="face-recognition",
    video_processor_factory=FaceProcessor
)