from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb 
import platform
import distro
import getpass # trust me I don't want your password lol. no network capabilities here
import os
from PIL import ImageTk, Image

PROG_PATH = os.path.dirname(os.path.realpath(__file__))
USERNAME = getpass.getuser() # searches env vars for username
WINDOW_WIDTH = 400 
WINDOW_HEIGHT = 450 

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

# find logo banner in filesystem and reference to ../banner/
def findFileBanner():
    filePath = [PROG_PATH, "/banner/"] # arr to hold filename to be searched
    if platform.system() == "Darwin":
        filePath.append("macOS/")
        filePath.append(str(int(float(platform.release()[0:3])))) # rewrite for older OS X systems
    elif platform.system() == "Linux":
        filePath.append("linux/")
        filePath.append(distro.id())
        # reference https://distro.readthedocs.io/en/latest/#distro.id for possible Linux names, also includes BSD derivatives
    elif platform.system() == "Windows":
        filePath.append("windows/")
        filePath.append(platform.release())

    filePath = ''.join(filePath)
    if checkBannerForJPG(filePath) == True:
        return filePath + ".jpg"
    elif checkBannerForPNG(filePath) == True:
        return filePath + ".png"
    
def checkBannerForJPG(filePath):
    filePath = (filePath + ".jpg")

    if os.path.isfile(filePath):
        return True

    return False

def checkBannerForPNG(filePath):
    filePath = (filePath + ".png")

    if os.path.isfile(filePath):
        return True

    return False

# this is the body of the text that should hopefully show in the window
def returnCopyrightText(OSInfo, user):
    os = OSInfo.pop(0)
    version = OSInfo.pop(0)
    username = user
    text = f"""
    {os} {version}
    Copyright to respective owners above. All rights reserved.

    The {os} operating system may come with a warranty or it may not. Just depends on what it is.

    This product, be it: the combination of software, hardware, and customizations are from the proud owner of this computer:
        {username}

    """
    return text

# debug print to console, will be removed in later commits
print(compileOSInfo())
print(findFileBanner())
print(returnCopyrightText(compileOSInfo(), USERNAME))

# window init
root = tb.Window(themename="cosmo")
root.title("multiver.py")
root.geometry('%dx%d' % (WINDOW_WIDTH, WINDOW_HEIGHT))
root.resizable(False, False)

# banner image logic
img = Image.open(findFileBanner()).resize((int(WINDOW_WIDTH), int(WINDOW_HEIGHT/2.5)))
img = ImageTk.PhotoImage(img)
imglabel = tb.Label(root,
                    image=img)
imglabel.pack()

# img separator to text 
textSeparator = tb.Separator(bootstyle="secondary",
                             orient="horizontal")
textSeparator.pack(fill="x")

# display text to window
textDisplay = tb.Label(text=returnCopyrightText(compileOSInfo(), USERNAME),
                       wraplength=(WINDOW_WIDTH-20),
                       justify="left")



textDisplay.pack()

# exit button and logic
exitButton = tb.Button(text="OK",
                       bootstyle="default, outline",
                       command=lambda: root.quit())
exitButton.place(x=330,
                 y=400)

root.mainloop()
