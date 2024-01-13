import base64
import io
import json
import os
import re, PyPDF2
import tempfile
from tempfile import gettempdir
from flask import render_template, redirect, request, app, flash, send_file
from werkzeug.utils import secure_filename
from pdfminer.high_level import extract_pages, extract_text
from io import BytesIO
class appController():
    def __init__(self, app):
        pass

    def register(self):
        if request.method == "POST":
            if request.form.get("usreg"):
                name = request.form.get("fname")
                usname = request.form.get("usname")
                usemail = request.form.get("usemail")
                usnum = request.form.get("usphnum")
                uspwd = request.form.get("uspwd")
                return redirect("/")

    def showNewProject(self):
        return render_template("new-project.html")

    def userCode(self):
        if request.method == "GET":
            code = request.args.get("code")
            language = request.args.get("language")
            print(code, language)

    def uploader(self, file):

            filename = secure_filename(file.filename)

            filepath = os.path.join(tempfile.gettempdir(), filename)

            file.save(filepath)
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)

                page = reader.pages[0]

                text = page.extract_text()

            return render_template("new-project.html", text=text)
