from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb 
import platform
import distro

# simply gathers OS name, version, and includes Linux distro guesser
def compileOSInfo():
    result = []
    result.append(platform.system()) # OS name
    if platform.system() == "Darwin":
        result.append(int(float(platform.release()[0:3]))
    elif platform.system() == "Linux":
        if distro.os_release_attr("version") == '':
            result.append("rolling")
        else:
            result.append(distro.os_release_attr("version"))
    return result

print(compileOSInfo())

# window init
root = tb.Window(themename="cosmo")
root.title("multiver.py")
root.geometry('400x450')

exitButton = tb.Button(text="OK",
                       bootstyle="default, outline")
exitButton.place(x=330,y=400)

root.mainloop()
