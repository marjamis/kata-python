import subprocess as sp

paths = {
    'notepad': "/usr/bin/gedit",
    'terminal': "/usr/bin/terminator",
    'calculator': "/usr/bin/gnome-calculator",
}

def open_notepad():
    sp.Popen(paths['notepad'])

def open_terminal():
    sp.Popen(paths['terminal'])

def open_calculator():
    sp.Popen(paths['calculator'])
