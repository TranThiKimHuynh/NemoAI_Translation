import streamlit as st
import time
from PIL import Image
from lib import convert_image_to_text, speech_to_text
from transformers import MarianMTModel, MarianTokenizer

model_path = 'fine-tuned-mt-en-vi'
tokenizer = MarianTokenizer.from_pretrained(model_path)
model = MarianMTModel.from_pretrained(model_path)

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
background: linear-gradient(90deg, #6600CC 0%, #FF6600 100%);
}
[data-testid="stHeader"] {
text-color: white;
}
[data-testid="stMarkdownContainer"] h1 {
color: white;
text-align: center;
}
.custom-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.custom-title {
    color: white;
    font-size: 3em;
    font-family: 'Arial', sans-serif;
}
.custom-logo {
    width: 100px; /* Adjust the size as needed */
}
.custom-text-area {
    background-color: white;
    color: black;
    border: 2px solid #6600CC;
    border-radius: 10px;
    padding: 10px;
    width: 100%;
    height: 150px;
    resize: none;
}
.custom-button:hover {
    background-color: darkorange;
}
.custom-label {
    background-color: #3A9CE4;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    display: inline-block;
    margin-bottom: 10px;
}
.arrow-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px 0;
}
.arrow {
    font-size: 2em;
    color: yellow;
}
</style>
"""
# Set page background color
st.markdown(page_bg, unsafe_allow_html=True)

# Logo and title
st.markdown('''
<div class="custom-container">
    <h1 class="custom-title">NEMO AI TRANSLATION  [- -] </h1>
</div>
''', unsafe_allow_html=True)
st.image("ui-res/Bot.png", width=150)

# Radio button to choose input type
input_type = st.radio("Choose input type:", ("Text", "Image", "Voice"), index=0)

input_text = ""

# Input text areas
if input_type == "Text":
    st.markdown('<div class="custom-label">ENGLISH</div>', unsafe_allow_html=True)
    input_text = st.text_area("", height=150, key="input_text", placeholder="Enter text here...", label_visibility="collapsed")

elif input_type == "Image":
    st.markdown('<div class="custom-label">IMAGE INPUT</div>', unsafe_allow_html=True)
    uploaded_image = st.file_uploader("Upload image file", type=["jpg", "png", "jpeg"], key="input_image")
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        with st.spinner('Processing image...'):
            input_text = convert_image_to_text(image)
elif input_type == "Voice":
    st.write("Upload an audio file and convert it to text.")

    uploaded_file = st.file_uploader("Choose an audio file", type=["wav"], key="input_audio")

    if uploaded_file is not None:
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type}
        st.write(file_details)

        with st.spinner('Processing audio...'):
            input_text = speech_to_text(uploaded_file)

# Further processing of input_text if needed
if input_text:
    st.write("Processed Text:", input_text)

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(204, 49, 49);
}
</style>""", unsafe_allow_html=True)

## Translate function
def translate_text(text):
    inputs = tokenizer.encode(text, return_tensors="pt", truncation=True, padding="max_length", max_length=64)
    translated_tokens = model.generate(inputs, max_length=64, num_beams=4, early_stopping=True)
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return translated_text

# Handle translation
if st.button("TRANSLATE", key="translate_button"):
    if input_text == "":
        st.error("Please enter text to translate!")
    else:
        translated_text = translate_text(input_text)
        with st.spinner('Wait for it...'):
            time.sleep(2)
        # Label of Icon translation and Vietnamese language
        st.markdown('<div class="arrow-container"><div class="arrow">⇄</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="custom-label">VIETNAMESE</div>', unsafe_allow_html=True)
        # Output text area
        st.text_area(label = "",value= translated_text, height=150, key="output_text", placeholder="Translated text will appear here...", label_visibility="collapsed")




