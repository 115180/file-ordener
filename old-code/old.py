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

def sort_extension(map):
    os.chdir(map)
    files = sorted(os.listdir())
    
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

def sort_metadata(): #Create a function to call later copied from test folder
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

def type_time_sorting():
    sortByYear = False
    sortByMonth = False
    sortByDay = False

    if request.method == "POST":
        value = request.form.get("timeSorting")
            
        if value == 'sortByYear':
            sortByYear = True
            sortByMonth = False
            sortByDay = False
        elif value == 'sortByMonth':
            sortByYear = False
            sortByMonth = True
            sortByDay = False
        elif value == 'sortByDay':
            sortByYear = False
            sortByMonth = False
            sortByDay = True
    return sortByDay, sortByMonth, sortByYear

#______________________________________________________________________________________________________________________________#

def sort_mod_time(map): 
    os.chdir(map)
    
    files = sorted(os.listdir())
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

def get_check_map():
    message = ""
    currentMap = request.form.get('map_input')
    mapExists = False
    
    if currentMap:
        mapExists = os.path.exists(currentMap)
        if mapExists:
            message="Er is een map gevonden"
        elif mapExists == False:
            message="Geen geldige map"
    print(f"current map: {currentMap}")
    print(f"map exists: {mapExists}")
    print(f"message: {message}")
    return currentMap, mapExists, message

#______________________________________________________________________________________________________________________________#

def check_choice_map():
    value = None
    action = None
    if request.method == "POST":
        value = request.form.get("action")
        print(f" value: {value}")
        if value == 'yes':
            action = True
        else:
            action = False
        
    return action

#______________________________________________________________________________________________________________________________#

def type_sorting():
    sortByExtension = False
    sortByModTime = False
    type = ""
    if request.method == "POST":
        type = request.form.get('typeSorting')
        if type == 'byExt':
            sortByExtension = True
            sortByModTime = False
        elif type == 'byTime':
            sortByExtension = False
            sortByModTime = True
    return sortByExtension, sortByModTime, type
        
#______________________________________________________________________________________________________________________________#



app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])


def my_form():
    value = None
    mapExists = None
    currentMap = None
    message = None
    sortByExtension, sortByModtime, valueTypeSorting = type_sorting()

    if sortByExtension:
        print("sort by ext")
        currentMap, mapExists, message = get_check_map()

        print(f"De map die je hebt ingevuld is: {currentMap}")

        if currentMap != None and mapExists == True:
            actionCheckChoice = check_choice_map()
            if actionCheckChoice == True:
                message = sort_extension(currentMap)
            elif actionCheckChoice == False:
                message = "Vul een nieuwe map in"


    elif sortByModtime:
        print("sort by time")
        sortByDay, sortByMonth, sortByYear = type_time_sorting()
        print(sortByDay)
        print(sortByMonth)
        print(sortByYear)
        if sortByDay != None or sortByMonth != None or sortByYear != None:
            check_choice_map()
        
    
    

    return render_template(
        'flask_web.html',
        value = valueTypeSorting,
        mapExists = mapExists,
        currentMap = currentMap,
        message = message
    )

if __name__ == '__main__':
    app.run(debug=True)
