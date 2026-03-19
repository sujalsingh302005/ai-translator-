import tkinter as tk
from tkinter import ttk
from deep_translator import GoogleTranslator
import speech_recognition as sr
import cv2
import pytesseract
from gtts import gTTS
from playsound import playsound
import os

# -------- LANGUAGE MAP -------- #
languages = {
    "Hindi": "hi",
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-cn"
}

# -------- FUNCTIONS -------- #

def translate_text():
    try:
        input_text = text_input.get("1.0", tk.END).strip()
        target_lang = language_var.get()

        if not input_text:
            status_label.config(text="⚠️ Enter text first", fg="orange")
            return

        translated = GoogleTranslator(source='auto', target=target_lang).translate(input_text)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)

        root.clipboard_clear()
        root.clipboard_append(translated)

        status_label.config(text="✅ Translated + Copied", fg="lightgreen")

    except Exception as e:
        status_label.config(text=f"❌ Error: {str(e)}", fg="red")


def voice_input():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            status_label.config(text="🎤 Listening...", fg="cyan")
            root.update()

            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)

            text = recognizer.recognize_google(audio)

            text_input.delete("1.0", tk.END)
            text_input.insert(tk.END, text)

            status_label.config(text="✅ Voice captured", fg="lightgreen")

    except sr.WaitTimeoutError:
        status_label.config(text="⏱️ Timeout!", fg="orange")
    except sr.UnknownValueError:
        status_label.config(text="❌ Not understood", fg="red")
    except Exception as e:
        status_label.config(text=f"❌ Mic Error: {str(e)}", fg="red")


# 🔥 FINAL SPEAK FUNCTION (gTTS)
def speak_output():
    text = output_text.get("1.0", tk.END).strip()
    lang = language_var.get()

    if not text:
        status_label.config(text="⚠️ Nothing to speak", fg="orange")
        return

    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("voice.mp3")

        playsound("voice.mp3")
        os.remove("voice.mp3")

        status_label.config(text="🔊 Speaking...", fg="lightgreen")

    except Exception as e:
        status_label.config(text=f"❌ Speech Error: {str(e)}", fg="red")


def clear_all():
    text_input.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    status_label.config(text="")


def camera_translate():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        status_label.config(text="❌ Camera not working", fg="red")
        return

    status_label.config(text="📸 Press 'Q' to capture", fg="cyan")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Camera - Press Q", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    text = pytesseract.image_to_string(frame)

    if not text.strip():
        status_label.config(text="❌ No text detected", fg="red")
        return

    text_input.delete("1.0", tk.END)
    text_input.insert(tk.END, text)

    try:
        translated = GoogleTranslator(source='auto', target=language_var.get()).translate(text)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)

        status_label.config(text="🔥 Camera Translation Done", fg="lightgreen")

    except Exception as e:
        status_label.config(text=f"❌ Error: {str(e)}", fg="red")


# -------- UI -------- #

root = tk.Tk()
root.title("🌍 AI Translator App")
root.geometry("750x580")
root.config(bg="#0f172a")

# Title
title = tk.Label(root, text="🌍 AI Translator", font=("Helvetica", 22, "bold"),
                 bg="#0f172a", fg="#38bdf8")
title.pack(pady=10)

# Input
text_input = tk.Text(root, height=5, width=70,
                     bg="#1e293b", fg="white",
                     insertbackground="white", font=("Arial", 12))
text_input.pack(pady=10)

# Dropdown
language_var = tk.StringVar(value="hi")

dropdown = ttk.Combobox(root, values=list(languages.keys()), state="readonly")
dropdown.set("Hindi")
dropdown.pack()

def update_lang(event):
    language_var.set(languages[dropdown.get()])

dropdown.bind("<<ComboboxSelected>>", update_lang)

# Buttons
btn_frame = tk.Frame(root, bg="#0f172a")
btn_frame.pack(pady=10)

def create_btn(text, cmd, color):
    return tk.Button(btn_frame, text=text, command=cmd,
                     bg=color, fg="white", padx=10, pady=5,
                     font=("Arial", 10, "bold"), bd=0)

create_btn("Translate 🚀", translate_text, "#22c55e").grid(row=0, column=0, padx=5)
create_btn("🎤 Speak", voice_input, "#3b82f6").grid(row=0, column=1, padx=5)
create_btn("🔊 Listen", speak_output, "#a855f7").grid(row=0, column=2, padx=5)
create_btn("🧹 Clear", clear_all, "#ef4444").grid(row=0, column=3, padx=5)
create_btn("📸 Camera", camera_translate, "#f59e0b").grid(row=0, column=4, padx=5)

# Output
output_text = tk.Text(root, height=5, width=70,
                      bg="#1e293b", fg="white",
                      insertbackground="white", font=("Arial", 12))
output_text.pack(pady=10)

# Status
status_label = tk.Label(root, text="", bg="#0f172a",
                        font=("Arial", 11))
status_label.pack()

root.mainloop()