import cv2
import os
import pandas as pd
import customtkinter as ctk
import subprocess
from tkinter import messagebox
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Smart Attendance System")
root.geometry("800x500")

# Ensure folders
if not os.path.exists("Images"):
    os.makedirs("Images")

if not os.path.exists("Attendance.csv"):
    with open("Attendance.csv", "w") as f:
        f.write("Roll,Date,Time\n")


# Load students
def load_students():
    students = {}
    if os.path.exists("students.csv"):
        with open("students.csv", "r") as f:
            for line in f.readlines()[1:]:
                data = line.strip().split(",")
                if len(data) >= 3:
                    students[data[0]] = data[1:]
    return students


# -------------------- NEW REGISTRATION --------------------
def new_registration():

    win = ctk.CTkToplevel(root)
    win.title("New Registration")
    win.geometry("400x450")

    name = ctk.CTkEntry(win, placeholder_text="Name")
    name.pack(pady=10)

    roll = ctk.CTkEntry(win, placeholder_text="Roll No")
    roll.pack(pady=10)

    dob = ctk.CTkEntry(win, placeholder_text="DOB (DD/MM/YYYY)")
    dob.pack(pady=10)

    def capture():
        r = roll.get().strip()
        n = name.get().strip()

        if not r or not n:
            messagebox.showerror("Error", "Fill details first")
            return

        cam = cv2.VideoCapture(0)

        messagebox.showinfo("Info", "Press SPACE to capture")

        while True:
            ret, frame = cam.read()
            cv2.imshow("Capture Face", frame)

            k = cv2.waitKey(1)
            if k % 256 == 32:

                cv2.imwrite(f"Images/{r}.jpg", frame)
                break

        cam.release()
        cv2.destroyAllWindows()

    def save():

        n = name.get().strip()
        r = roll.get().strip()
        d = dob.get().strip()

        if not n or not r or not d:
            messagebox.showerror("Error", "Fill all fields")
            return

        with open("students.csv", "a") as f:
            f.write(f"\n{r},{n},{d}")

        messagebox.showinfo("Success", "Student Registered")

        win.destroy()

    ctk.CTkButton(win, text="Capture Photo", command=capture).pack(pady=10)
    ctk.CTkButton(win, text="Save Student", command=save).pack(pady=10)


# -------------------- LOGIN ATTENDANCE --------------------
def login_attendance():

    def mark_attendance(roll):

        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")

        with open("Attendance.csv", "a") as f:
            f.write(f"\n{roll},{date},{time}")

        messagebox.showinfo("Success", f"Attendance Marked: {roll}")

    roll = ctk.CTkInputDialog(text="Enter Roll No").get_input()

    if not roll:
        return

    students = load_students()

    if roll not in students:
        messagebox.showerror("Error", "Invalid Roll No")
        return

    cam = cv2.VideoCapture(0)

    messagebox.showinfo("Info", "Press Q to exit camera")

    while True:
        ret, frame = cam.read()
        cv2.imshow("Attendance Camera", frame)

        k = cv2.waitKey(1)

        if k & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    mark_attendance(roll)


# -------------------- VIEW --------------------
def view_attendance():
    subprocess.Popen(["Attendance.csv"], shell=True)


# -------------------- EXIT --------------------
def exit_app():
    root.destroy()


# -------------------- UI --------------------
ctk.CTkLabel(root, text="SMART ATTENDANCE SYSTEM",
             font=("Arial", 28, "bold")).pack(pady=20)

frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

ctk.CTkButton(frame, text="New Registration",
              command=new_registration, width=250).pack(pady=10)

ctk.CTkButton(frame, text="Login Attendance",
              command=login_attendance, width=250).pack(pady=10)

ctk.CTkButton(frame, text="View Attendance",
              command=view_attendance, width=250).pack(pady=10)

ctk.CTkButton(frame, text="Exit",
              command=exit_app, width=250).pack(pady=10)

root.mainloop()