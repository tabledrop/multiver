import windowgen
import platform

PLATFORM_OS_NAME = platform.system()

def DisplaymacOS():
    result = []

    if PLATFORM_OS_NAME != "Darwin":
        print("[DEBUG]: Not macOS")

    # if somehow you have a non-standard macOS version
    # (impossible unless you're a macOS dev)
    # this is a generic placeholder for that
    DarwinMajorVersion = 0
    DarwinVersion = "Generic"
    result.append(DarwinMajorVersion)
    result.append(DarwinVersion)

    if PLATFORM_OS_NAME == "Darwin":
        if int(float(platform.release()[0:3])) == 0:
            return result
        else:
            result = []
            DarwinVersion = platform.release()
            DarwinMajorVersion = int(float(platform.release()[0:3]))
            result.append(DarwinMajorVersion)
            result.append(DarwinVersion)
            return result

def DisplayWindows():
    result = []

    if PLATFORM_OS_NAME != "Windows":
        print("[DEBUG]: Not Windows")

    WindowsMajorVersion = 5.1
    WindowsVersion = "XP"
    result.append(WindowsMajorVersion)
    result.append(WindowsVersion)

    if PLATFORM_OS_NAME == "Windows":
        if platform.release() == 5.1:
            return result
        else:
            result = []
            WindowsMajorVersion = platform.release()
            WindowsVersion = platform.release()
            result.append(WindowsMajorVersion)
            result.append(WindowsVersion)
            return result

def DisplayLinux():
    result = []

    if PLATFORM_OS_NAME != "Linux":
        print("[DEBUG]: Not Linux")

    if PLATFORM_OS_NAME == "Linux":
        print("[DEBUG]: TO BE IMPLEMENTED")

print(DisplaymacOS())
print(DisplayWindows())
print(DisplayLinux())

# def PlatformDiscover():
#    if PLATFORM_OS_NAME == "Windows":
#        print("Winver exists lol")
#   elif PLATFORM_OS_NAME == "Darwin":
#        DarwinMajorVer = int(float(platform.release()[0:3]))
#       DarwinVersion = platform.release()
#        print(DarwinVersion)
#    elif PLATFORM_OS_NAME == "Linux":
#        print("literal chad lol")

# PlatformDiscover()
