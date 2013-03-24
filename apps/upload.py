from flask import Blueprint, request, url_for, g , session, flash, redirect, render_template, current_app, send_from_directory
from decorators import is_admin
from models.forms import Upload
from os import path
from werkzeug import secure_filename

upload = Blueprint("upload", __name__)
    
@upload.route("/", methods=["GET", "POST"])
@is_admin
def upload_file():
    form = Upload()
    if form.validate_on_submit():
        binary = request.files['upload']
        filename = secure_filename(binary.filename)
        if form.filename.data:
            filename = secure_filename(form.filename.data)
        filepath = path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if binary and allowed_extensions(filename):
            if not path.isfile(filepath):
                binary.save(filepath)
                flash("File '{0}' uploaded to {1}.".format(binary.filename, url_for(".get_file", filename=filename)), "info")
            else:
                flash("File '{0}' could not be saved. Filename already exists.".format(filename), "error")
        else:
            flash("File could not be found or extension not allowed.")
    return render_template("forms.jinja.html", form=form)
    
@upload.route("/file/<filename>")
def get_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
        filename)

def allowed_extensions(filename):
    return any(map(lambda extension: filename.endswith(extension), current_app.config['ALLOWED_EXTENSIONS']))
