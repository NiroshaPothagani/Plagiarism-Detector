from multiprocessing import context
import os
from random import randint

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from .PlagiarismChecker import PlagiarismChecker

app = Flask(__name__)

ALLOWED_EXTENSIONS = {"txt"}
UPLOAD_FOLDER = os.path.join(os.getcwd(), "input-files")

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":

        if "files" not in request.files:
            return render_template("500.html")

        files = request.files.getlist("files")

        path = os.path.join(UPLOAD_FOLDER, str(randint(10000, 99999)))
        os.mkdir(path)

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(path, filename))

        plagiarism_checker = PlagiarismChecker(path)
        result = plagiarism_checker.get_results()

        formatted_result = []
        for item in result:
            formatted_result.append([item[0], item[1], round(item[2] * 100, 2)])

        context = dict({"result": True, "data": formatted_result})

        return render_template("index.html", result=True, data=formatted_result)

    return render_template("index.html", result=False)
