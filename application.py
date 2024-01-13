import magic
from flask import Flask, redirect, render_template, request
import io
import json
from docx.api import Document
import pytesseract
import os, pyttsx3, speech_recognition
import PIL
from pdfminer.high_level import extract_pages, extract_text
from PIL.Image import Image
import re, PyPDF2
import tempfile
from tempfile import gettempdir
from flask import render_template, redirect, request, app, flash, send_file
from werkzeug.utils import secure_filename
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    def showNewProject(self):
        return render_template("new-project.html")

    def userCode(self):
        if request.method == "GET":
            code = request.args.get("code")
            language = request.args.get("language")
            print(code, language)


    return render_template("index.html")

def is_pdf(filepath):
    """Returns True if the file is a PDF file, False otherwise."""
    mime_type = magic.from_file(filepath, mime=True)
    return mime_type
def is_txt(filepath):
    """Returns True if the file is a text file, False otherwise."""
    mime_type = magic.from_file(filepath, mime=True)
    return mime_type
def is_docx(filepath):
    """Returns True if the file is a docx file, False otherwise."""
    mime_type = magic.from_file(filepath, mime=True)
    return mime_type
def is_image(filepath):
    """Returns True if the file is an image file, False otherwise."""
    mime_type = magic.from_file(filepath, mime=True)
    return mime_type

@app.route("/detect_file_type", methods=["GET", "POST"])
def detect_file_type():
    if request.method == 'POST':
        file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(tempfile.gettempdir(), filename)
    file.save(filepath)
    if is_pdf(filepath) == 'application/pdf':
        pdf_recognition(filepath)
        return redirect("/")
    elif is_txt(filepath) == 'text/plain':
        txt_recognition(filepath)
        return redirect("/")
    elif is_docx(filepath) == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        docx_recognition(filepath)
        return redirect("/")
    elif is_image(filepath) == 'image/png' or 'image/jpeg':
        image_recognition(filepath)
        return redirect("/")
    else:
        return "other"
    
def pdf_recognition(filepath):
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text = page.extract_text()
            print(text)
    return redirect("/")
def txt_recognition(filepath):
    with open(filepath, "rb") as f:
        text = f.read()
        print(text)
    return redirect("/")

def docx_recognition(filepath):
    document = Document(filepath)
    all_text = ""
    for(table) in document.tables:
        for(row) in table.rows:
            print("|".join(cell.text for cell in row.cells))
    for p in document.paragraphs:
        all_text += p.text
        all_text += "\n"
    print(all_text)

def image_recognition(image: Image):
    myconfig = r"--psm 6 --oem 3"
    text = pytesseract.image_to_string(PIL.Image.open(image), config=myconfig)
    print(text)

def text_to_speech(self):
    if request.method == "GET":
        test = request.args.get("tts")
        print(test)
        text_speech = pyttsx3.init()
        text_speech.say(f"{test}")
        text_speech.runAndWait()
        return None

def speech_recognition(self):
    if request.method == "GET":
        recognizer = speech_recognition.Recognizer()
        while True:
                 try:
                     with speech_recognition.Microphone() as mic:
                         recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                         audio = recognizer.listen(mic)
                         text = recognizer.recognize_google(audio)
                         text = text.lower()
                         print(f"Recognized {text}")
                         return json.dumps(text)
                 except speech_recognition.UnknownValueError:
                    # Reset the recognizer
                    recognizer = speech_recognition.Recognizer()
                    # Continue listening
                    continue
                 # Reinitialize the text variable
                 text = ""

if __name__ == "__main__":
    app.run()