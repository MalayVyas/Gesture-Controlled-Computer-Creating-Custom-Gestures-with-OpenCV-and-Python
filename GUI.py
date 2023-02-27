import tkinter as tk
import customtkinter as ctk
import subprocess


def run_python_file(file_path):
    subprocess.call(['python', file_path])

def run():
    run_python_file(r"Gesture_Idea_Implementation.py")


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.attributes('-fullscreen', True)
# app.geometry()
app.title("GUI")
app.configure(background="red")

button = ctk.CTkButton(master= app,width=120, height=32,
                       border_width=5,
                       corner_radius=8,
                       text="Run app",
                       command=run,
                       fg_color="red")
button.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)

app.mainloop()
