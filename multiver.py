from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb 
import platform
import distro
import getpass # trust me I don't want your password lol. no network capabilities here

# simply gathers OS name, version, and includes Linux distro guesser since Linux distros are weird lol
def compileOSInfo():
    result = [] # arr to store OS name and version
    if platform.system() == "Darwin":
        result.append(platform.system())
        result.append(platform.release())
    elif platform.system() == "Linux":
        result.append(distro.name())
        if distro.os_release_attr("version") == '':
            result.append("rolling")
        else:
            result.append(distro.os_release_attr("version"))
    elif platform.system() == "Windows":
        print("windows key + r, type in 'winver.exe', and boom. you don't need this tool")
        result.append("lol")
        result.append("nope")
    return result

USERNAME = getpass.getuser() # searches env vars for username

# find logo banner in JSON master list and reference to ../banner/
def findFileBanner():
    fileName = [] # arr to hold filename to be searched
    if platform.system() == "Darwin":
        fileName.append(int(float(platform.release()[0:3]))) # might fix later for OS X 10.2-10.12
    elif platform.system() == "Linux":
        fileName.append(distro.id())
        # reference https://distro.readthedocs.io/en/latest/#distro.id for possible Linux names, also includes BSD derivatives
    elif platform.system() == "Windows":
        file.append(platform.release())
    fileName.append(".png")
    return fileName

# debug print to console, will be removed in later commits
print(compileOSInfo())
print(findFileBanner())
print(USERNAME)

# window init
root = tb.Window(themename="cosmo")
root.title("multiver.py")
root.geometry('400x450')

exitButton = tb.Button(text="OK",
                       bootstyle="default, outline")
exitButton.place(x=330,y=400)

root.mainloop()
