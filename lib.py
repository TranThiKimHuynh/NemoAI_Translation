import numpy as np
from PIL import Image
import pytesseract
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to convert image to text using pytesseract
def convert_image_to_text(image):
    text = pytesseract.image_to_string(image)
    return text

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_data = None

    def recv(self, frame):
        audio = frame.to_ndarray()
        self.audio_data = audio
        return frame

    def recognize_speech(self):
        if self.audio_data is not None:
            audio_np = np.int16(self.audio_data * 32767)
            audio_wav = sr.AudioData(audio_np.tobytes(), frame_rate=16000, sample_width=2)
            try:
                text = self.recognizer.recognize_google(audio_wav)
                return text
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError as e:
                return f"Could not request results; {e}"
        return ""