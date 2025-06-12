import os
from tkinter import Tk, filedialog

# 1. Venster openen om map te kiezen
root = Tk()
folder_path = filedialog.askdirectory(title="Selecteer een map")
