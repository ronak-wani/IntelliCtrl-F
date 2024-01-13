from flask import Flask, redirect, render_template, request
import io
import json
import os
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
    def txt_uploader(self, file):
            filename = secure_filename(file.filename)
            filepath = os.path.join(tempfile.gettempdir(), filename)
            file.save(filepath)
            with open(filepath, "rb") as f:
                text = f.read()
            return render_template("new-project.html", text=text)
    #
    # def docx_uploader(self, file):
    #         filename = secure_filename(file.filename)
    #         filepath = os.path.join(tempfile.gettempdir(), filename)
    #         file.save(filepath)
    #         with open(filepath, "rb") as f:
    #             text = f.read()
    #         return render_template("new-project.html", text=text)

    return render_template("index.html")
@app.route("/pdf_uploader", methods=["GET", "POST"])
def pdf_uploader():
    if request.method == 'POST':
        file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(tempfile.gettempdir(), filename)
    file.save(filepath)
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text = page.extract_text()
            print(text)
    return redirect("/")
if __name__ == "__main__":
    app.run()