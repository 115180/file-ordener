from flask import Flask, request, render_template
import os
from pathlib import Path
import shutil
from PIL import Image
import time



#______________________________________________________________________________________________________________________________#

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

#______________________________________________________________________________________________________________________________#

def organize_files(map):
    files = sorted(os.listdir())

    os.chdir(map)
    Path("images").mkdir(exist_ok=True)
    Path("else").mkdir(exist_ok=True)

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

#______________________________________________________________________________________________________________________________#

def check_ifexist(map_path): 
    return os.path.exists(map_path)

#______________________________________________________________________________________________________________________________#

def sortByMetadata(): #Create a function to call later copied from test folder
    files = sorted(os.listdir())

    for file in files:
        if file == "else" or file == "images": #Skip if the file is a folder
            continue
        else:
            if file.lower().endswith(('.jpg', '.png', '.jpeg', '.gif')):
                image = Image.open(file)
                print(image.size, image.mode) #Get the metadata from the images by referring to the image which you saved in a var

				#Add code for the actual sorting here
				#I cant be fucked actually doing it right now

#______________________________________________________________________________________________________________________________#

def sortByTimelastchanged():
    files = sorted(os.listdir())

    sortByYear = False
    sortByMonth = False
    sortByDay = False

    messageSorting = ""
    
    for file in files:
        modTime = os.path.getmtime(file) #Create a var with the last time the doc was eddited in sec since the epoch


        locTime = time.ctime(modTime) #Converts time since epoch to real date       May need optimization with datetime.Now()
        date = locTime.split() #Splits the string in an array with 5 elements: [Day of the week, Month, Date, Time, Year] 

        if sortByYear:
            year = date[-1]

            Path(f"Files from {year}").mkdir(exist_ok=True)
            shutil.move(file, f"Files from {year}") #PROBLEM HERE, IT INSTANTLY MOVES IT SO NO MOVE THAN 1 OPTION CAN BE CHOSEN

            messageSorting = "Alles is gesorteerd op jaar!"

        if sortByMonth:
            month = date[1]

            Path(f"Files from {month}").mkdir(exist_ok=True)
            shutil.move(file, f"Files from {month}")

            messageSorting = "Alles is gesorteerd op maand!"

        if sortByDay:
            day = date[2]
            dayoftheweek = date[0]

            Path(f"Files from {dayoftheweek} the {day}").mkdir(exist_ok=True)
            shutil.move(file, f"Files from {dayoftheweek} the {day}")

            messageSorting = "Alles is gesorteerd op dag!"
    return messageSorting

#______________________________________________________________________________________________________________________________#

app = Flask(__name__)
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
