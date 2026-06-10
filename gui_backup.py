import customtkinter as ctk
import subprocess
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Smart Attendance System")
root.geometry("800x500")

# -------------------
# Functions
# -------------------

def start_attendance():
    subprocess.Popen(["python", "main.py"])

def register_student():

register_window = ctk.CTkToplevel(root)
register_window.title("Register Student")
register_window.geometry("400x300")

name_label = ctk.CTkLabel(
    register_window,
    text="Student Name"
)
name_label.pack(pady=10)

name_entry = ctk.CTkEntry(
    register_window,
    width=250
)
name_entry.pack()

roll_label = ctk.CTkLabel(
    register_window,
    text="Roll Number"
)
roll_label.pack(pady=10)

roll_entry = ctk.CTkEntry(
    register_window,
    width=250
)
roll_entry.pack()

def save_student():

    name = name_entry.get().strip()
    roll = roll_entry.get().strip()

    if not name or not roll:
        messagebox.showerror(
            "Error",
            "Fill all fields"
        )
        return

    with open(
        "students.csv",
        "a"
    ) as f:
        f.write(f"\n{roll},{name}")

    messagebox.showinfo(
        "Success",
        "Student Registered Successfully"
    )

    register_window.destroy()

save_btn = ctk.CTkButton(
    register_window,
    text="Save Student",
    command=save_student
)

save_btn.pack(pady=20)
def view_attendance():
    try:
        subprocess.Popen(["Attendance.csv"], shell=True)
    except:
        messagebox.showerror(
            "Error",
            "Attendance file not found"
        )

# -------------------
# Title
# -------------------

title = ctk.CTkLabel(
    root,
    text="SMART ATTENDANCE SYSTEM",
    font=("Arial", 28, "bold")
)

title.pack(pady=20)

# -------------------
# Dashboard Frame
# -------------------

frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# -------------------
# Buttons
# -------------------

btn1 = ctk.CTkButton(
    frame,
    text="Start Attendance",
    width=250,
    height=50,
    command=start_attendance
)

btn1.pack(pady=15)

btn2 = ctk.CTkButton(
    frame,
    text="Register Student",
    width=250,
    height=50,
    command=register_student
)

btn2.pack(pady=15)

btn3 = ctk.CTkButton(
    frame,
    text="View Attendance",
    width=250,
    height=50,
    command=view_attendance
)

btn3.pack(pady=15)

btn4 = ctk.CTkButton(
    frame,
    text="Exit",
    width=250,
    height=50,
    command=root.destroy
)

btn4.pack(pady=15)

root.mainloop()