#Import the libraries
import os
from pathlib import Path
import shutil
from PIL import Image
import time

#Set current work directory
os.chdir("file_handling")

#Creates the folders 


#Creates an variable with all the sorted files inside the current directory
files = sorted(os.listdir())

#Varbiables for naming the files
counterImages = 1
counterDoubleName = 1
counterElse = 1

#ONLY SELECT ONE
sortByYear = False
sortByMonth = False
sortByDay = False

def sortByExtension(): #Create a function to call later
	#Use global variables
	global counterImages
	global counterDoubleName
	global counterElse

	Path("images").mkdir(exist_ok=True)
	Path("else").mkdir(exist_ok=True)
	
	#Goes through the entire current directory 
	for file in files: 
	    if file =="images"or file == "else": #If the current directory has the folders "images" or "else" in it: skip these folders
	        continue
	    name, ext = os.path.splitext(file) #Split the entire filename to the name and extension: EG: aPicture.jpg --> name = aPicture, ext = .jpg

		#Sorts by extension, if the extension to lowercase is equal to jpeg (image) create a new name, rename the file and move to the correct folder
	    if ext.lower() == ".jpg" or  ext.lower() == ".jpeg":
	        newName = f"Picture {counterImages}{ext}" #Use of F-string to create new name: EG: f"Picture{1}.{jpg}

			  #If the name is already in use, create a second name with the counterDoubleName variable: EG: f"Picture{1}_{1}.{jpg}
	        while os.path.exists(newName):
	            newName = f"Picture {counterImages}_{counterDoubleName}{ext}"
	            counterDoubleName += 1
	
	        os.rename(file, newName)
	        counterImages += 1
	
	        shutil.move(newName, "images") #Moves the image to the correct folder
		 #Moves all the other files to another folder
	    else:
	        newNameElse = f"Document {counterElse}{ext}"
	        while os.path.exists(newNameElse):
	            newNameElse = f"Document {counterElse}_{counterDoubleName}{ext}"
	            counterElse += 1
	        os.rename(file, newNameElse)
	        counterElse += 1
	
	        shutil.move(newNameElse, "else")

#______________________________________________________________________________________________________________________________#

def sortByMetadata(): #Create a function to call later
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
	for file in files:
		modTime = os.path.getmtime(file) #Create a var with the last time the doc was eddited in sec since the epoch
		

		locTime = time.ctime(modTime) #Converts time since epoch to real date       May need optimization with datetime.Now()
		date = locTime.split() #Splits the string in an array with 5 elements: [Day of the week, Month, Date, Time, Year] 

		if sortByYear:
			year = date[-1]

			Path(f"Files from {year}").mkdir(exist_ok=True)
			shutil.move(file, f"Files from {year}") #PROBLEM HERE, IT INSTANTLY MOVES IT SO NO MOVE THAN 1 OPTION CAN BE CHOSEN

		if sortByMonth:
			month = date[1]

			Path(f"Files from {month}").mkdir(exist_ok=True)
			shutil.move(file, f"Files from {month}")

		if sortByDay:
			day = date[2]
			dayoftheweek = date[0]

			Path(f"Files from {dayoftheweek} the {day}").mkdir(exist_ok=True)
			shutil.move(file, f"Files from {dayoftheweek} the {day}")

sortByTimelastchanged()
