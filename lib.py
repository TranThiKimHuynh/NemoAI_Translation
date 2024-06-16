import numpy as np
from PIL import Image
import pytesseract
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to convert image to text using pytesseract
def convert_image_to_text(image):
    text = pytesseract.image_to_string(image)
    return text

#Function speecn to text
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error: {str(e)}"
