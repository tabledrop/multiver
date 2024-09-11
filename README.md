# multiver

*like winver.exe on Windows but universally and terribly executed*
![sample of multiver.py running on my macOS Sonoma machine](/assets/sample.png)

## purpose

this project is meant to replicate the experience of winver while being platform agnostic. I'm feeling evil and making this run on Linux and macOS only

## requirements (also seen in requirements.txt)

* python3
* tkinter
* distro==1.9.0
* Pillow==10.2.0
* ttkbootstrap==1.10.1

## usage

when multiver is summoned, it spawns a window with information in a similar fashion as winver.exe on Windows. and also like Windows, there are no option flags or anything fancy. but if for whatever reason there is an option flag, it would probably spit this out:

```
  multiver.py [-h]

  -h  Calls this help menu (which is not useful).

  Summon multiver.py as it is a GUI program and not a CLI program.
```


