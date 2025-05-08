from flask import Flask, request, render_template
import os
from pathlib import Path
import shutil

# Globals
mapExists = True

def name_exists(name, extension, count):
    counterDoubleName = 1
    newName = name

    if extension == [".jpg", ".jpeg"]:
        if os.path.exists(name):
            newName = f"Picture {count}_{counterDoubleName}{extension}"
            counterDoubleName += 1
    else:
        if os.path.exists(name):
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
            newName = f"Picture {counterImages}{ext}"
            newName = name_exists(file, ext, counterImages)
            os.rename(file, newName)
            shutil.move(newName, "images")
            counterImages += 1
        else:
            newNameElse = f"Document {counterElse}{ext}"
            newName = name_exists(file, ext, counterElse)
            os.rename(file, newNameElse)
            shutil.move(newNameElse, "else")
            counterElse += 1

    return "De bestanden zijn geordend!"

def check_ifexist(map): 
    global mapExists
    if not os.path.exists(map):
        mapExists = False
        print(mapExists)
    else:
        mapExists = True
        render_template('flask_web.html', mapExists=mapExists)

        if request.method == "POST":
            action = request.form['action']
            if action == 'yes':
                organize_files(map)
            else:
                mapExists = False #Just for now
    return mapExists

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def my_form():
    result = None
    if request.method == 'POST':
        cwd_map = request.form['map_input']
        result = check_ifexist(cwd_map)

    return render_template('flask_web.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
