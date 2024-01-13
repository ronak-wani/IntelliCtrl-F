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

@app.route("/")
def index():
    # def register(self):
    #     if request.method == "POST":
    #         if request.form.get("usreg"):
    #             name = request.form.get("fname")
    #             usname = request.form.get("usname")
    #             usemail = request.form.get("usemail")
    #             usnum = request.form.get("usphnum")
    #             uspwd = request.form.get("uspwd")
    #             return redirect("/")
    #
    # def showNewProject(self):
    #     return render_template("new-project.html")
    #
    # def userCode(self):
    #     if request.method == "GET":
    #         code = request.args.get("code")
    #         language = request.args.get("language")
    #         print(code, language)
    #
    # def pdf_uploader(self, file):
    #         filename = secure_filename(file.filename)
    #         filepath = os.path.join(tempfile.gettempdir(), filename)
    #         file.save(filepath)
    #         with open(filepath, "rb") as f:
    #             reader = PyPDF2.PdfReader(f)
    #             page = reader.pages[0]
    #             text = page.extract_text()
    #         return render_template("new-project.html", text=text)
    # def txt_uploader(self, file):
    #         filename = secure_filename(file.filename)
    #         filepath = os.path.join(tempfile.gettempdir(), filename)
    #         file.save(filepath)
    #         with open(filepath, "rb") as f:
    #             text = f.read()
    #         return render_template("new-project.html", text=text)
    #
    # def docx_uploader(self, file):
    #         filename = secure_filename(file.filename)
    #         filepath = os.path.join(tempfile.gettempdir(), filename)
    #         file.save(filepath)
    #         with open(filepath, "rb") as f:
    #             text = f.read()
    #         return render_template("new-project.html", text=text)

    return render_template("index.html")

if __name__ == "__main__":
    app.run()