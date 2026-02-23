import pyttsx3
from gtts import gTTS
import pygame
import tkinter as tk
from tkinter import filedialog, messagebox

# -----------------------------
# FUNCTIONS
# -----------------------------

def speak_text():
    text = text_entry.get("1.0", tk.END).strip()

    if text == "":
        messagebox.showwarning("Warning", "Please enter text")
        return

    try:
        engine = pyttsx3.init()
        
        speed = speed_scale.get()
        engine.setProperty('rate', speed)

        voice_choice = voice_var.get()
        voices = engine.getProperty('voices')

        if voices:
            if voice_choice == "Male":
                engine.setProperty('voice', voices[0].id)
            else:
                engine.setProperty('voice', voices[-1].id)
        else:
            messagebox.showwarning("Warning", "No voices available")
            return

        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        messagebox.showerror("Error", f"Error in speak_text: {str(e)}")


def save_audio():
    text = text_entry.get("1.0", tk.END).strip()

    if text == "":
        messagebox.showwarning("Warning", "Enter text first")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                             filetypes=[("MP3 files", "*.mp3")])

    if file_path:
        tts = gTTS(text=text, lang=language_var.get())
        tts.save(file_path)
        messagebox.showinfo("Saved", "Audio saved successfully!")


def play_saved():
    file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])

    if file_path:
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        except Exception as e:
            messagebox.showerror("Error", f"Error playing audio: {str(e)}")

# -----------------------------
# GUI DESIGN
# -----------------------------

root = tk.Tk()
root.title("Text to Speech System")
root.geometry("500x500")
root.resizable(False, False)

title = tk.Label(root, text="Text-to-Speech Converter",
                 font=("Arial", 16, "bold"))
title.pack(pady=10)

text_entry = tk.Text(root, height=8, width=50)
text_entry.pack(pady=10)

# Voice selection
voice_var = tk.StringVar(value="Male")
tk.Label(root, text="Select Voice:").pack()
tk.Radiobutton(root, text="Male", variable=voice_var, value="Male").pack()
tk.Radiobutton(root, text="Female", variable=voice_var, value="Female").pack()

# Speed control
tk.Label(root, text="Speech Speed").pack(pady=5)
speed_scale = tk.Scale(root, from_=100, to=250, orient="horizontal")
speed_scale.set(150)
speed_scale.pack()

# Language selection
tk.Label(root, text="Language (for MP3 saving)").pack(pady=5)
language_var = tk.StringVar(value="en")

lang_menu = tk.OptionMenu(root, language_var,
                          "en",  # English
                          "hi",  # Hindi
                          "bn",  # Bengali
                          "fr",  # French
                          "es")  # Spanish
lang_menu.pack()

# Buttons
tk.Button(root, text="🔊 Speak Text", command=speak_text,
          width=20, bg="lightgreen").pack(pady=10)

tk.Button(root, text="💾 Save as MP3", command=save_audio,
          width=20, bg="lightblue").pack(pady=5)

tk.Button(root, text="▶ Play MP3", command=play_saved,
          width=20, bg="lightyellow").pack(pady=5)

root.mainloop()