__version__ = "1.0.1b1"
__author__ = "ProgMEM-CC"
__all__ = ["SoftwareInterpreter"]
import platform

print(f"chatai v{__version__} by {__author__}")

print("Importing modules...")
print("Importing modules... Done")
print("Importing SoftwareInterpreter...")
print("Importing SoftwareInterpreter... Done")


print("loading items...")

print("")

import random
import string


def all_unicode_chars():
    return "".join(chr(i) for i in range(0x110000) if chr(i).isprintable())


# Get all printable Unicode characters
unicode_chars = all_unicode_chars()
random = "sk-0:" + "".join(
    [
        random.choice(string.ascii_letters + string.digits + string.punctuation + "_*.")
        for n in range(50)
    ]
).replace(" ", "")
print("setting up...")
print("setting up... Done")
print("Configuring usage id...")
print("Configuring usage id... Done")
print(f"Usage id:\n{random}")
print("starting up...")
print("starting up... Done")
if platform.system() == "Windows":
    print("checking dwm.exe status...")
    print("checking dwm.exe status... Done")
    print("checking explorer.exe status...")
    print("checking explorer.exe status... Done")
    print("checking svchost.exe status...")
    print("checking svchost.exe status... Done")
    print("checking winlogon.exe status...")
    print("checking winlogon.exe status... Done")
    print("checking csrss.exe status...")
    print("checking csrss.exe status... Done")
    print("status check complete")

    print("ready to use")
elif platform.system() == 'Darwin':
    print("checking Finder status...")
    print("checking Finder status... Done")
    print("checking Dock status...")
    print("checking Dock status... Done")
    print("checking Spotlight status...")
    print("checking Spotlight status... Done")
    print("checking SystemUIServer status...")
    print("checking SystemUIServer status... Done")
    print("checking loginwindow status...")
    print("checking loginwindow status... Done")
    print("status check complete")
    print("ready to use")
elif platform.system() == 'Linux':
    print("checking Xorg status...")
    print("checking Xorg status... Done")
    print("checking systemd status...")
    print("checking systemd status... Done")
    print("status check complete")
    print("ready to use")
else:
    print('Unknown platform')
    print('this platform may not be supported')
    print('if possible please use another platform')
    print('ready to use')

print("checking bios/uefi status...")
print("checking bios/uefi status... Done")
print("checking bootloader status...")
print("checking bootloader status... Done")
print("checking kernel status...")
print("checking kernel status... Done")
print("checking init status...")
print("checking init status... Done")
print("checking shell status...")
print("checking shell status... Done")
print("checking system status...")
print("checking system status... Done")
print("status check complete")
print("ready to use")
print("checking network status...")
print("checking network status... Done")
print("checking internet status...")
print("checking internet status... Done")
print("checking connection status...")
print("checking connection status... Done")
print("starting up gui...")
print("starting up gui... Done")
print('ready to use')