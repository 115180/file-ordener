from flask import Flask, request, render_template
import os
from pathlib import Path
import shutil

app = Flask(__name__)

def name_exists(name, extension, count):
    counterDoubleName = 1
    newName = name

    if extension in [".jpg", ".jpeg"]:
        while os.path.exists(newName):
            newName = f"Picture {count}_{counterDoubleName}{extension}"
            counterDoubleName += 1
    else:
        while os.path.exists(newName):
            newName = f"Document {count}_{counterDoubleName}{extension}"
            counterDoubleName += 1

    return newName

def organize_files(map):
    os.chdir(map)
    Path("images").mkdir(exist_ok=True)
    Path("else").mkdir(exist_ok=True)

    files = sorted(os.listdir())
    counterImages = 1
    counterElse = 1

    for file in files:
        if file in ["images", "else"]:
            continue
        name, ext = os.path.splitext(file)

        if ext.lower() in [".jpg", ".jpeg"]:
            newName = name_exists(file, ext, counterImages)
            os.rename(file, newName)
            shutil.move(newName, "images")
            counterImages += 1
        else:
            newName = name_exists(file, ext, counterElse)
            os.rename(file, newName)
            shutil.move(newName, "else")
            counterElse += 1

    return "De bestanden zijn geordend!"

def check_ifexist(map_path): 
    return os.path.exists(map_path)

@app.route('/', methods=['GET', 'POST'])
def my_form():
    result = None
    message = ""
    map_check = None
    mapExists = None

    if request.method == 'POST':
        cwd_map = request.form['map_input']
        map_check = cwd_map
        mapExists = check_ifexist(cwd_map)
        action = request.form.get('action')

        if mapExists:
            if action == 'yes':
                result = organize_files(cwd_map)
                message = "De map bestaat en is geordend!" if result else "Er is iets misgegaan bij het ordenen."
            elif action == 'no':
                message = "Vul een nieuwe map in om te ordenen"
        else:
            message = "De map bestaat niet. Vul een andere map in."

    return render_template(
        'flask_web.html',
        result=result,
        message=message,
        mapExists=mapExists,
        map_check=map_check
    )

if __name__ == '__main__':
    app.run(debug=True)
