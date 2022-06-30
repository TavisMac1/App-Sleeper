from ast import Not
import psutil
from tabnanny import check
from asyncio.windows_events import NULL
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from turtle import bgcolor
from tkinter.ttk import Notebook
import autoMode
import getApps

#GUI setup
window = Tk()
window.geometry('600x600')
window.title('Sleeper')
window.configure(bg='purple')

#selectedApps = ["obs64", "firefox", "Spotify", "Code", "discord", "Discord"] # hard coded test apps
cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Name'
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
selectedApps = ["python.exe", "Taskmgr.exe", "Code.exe"] #supply some defaults that we don't ever want put to sleep
appsToSleep = []  # apps to sleep

appSelTxt = ttk.Label(text="choose apps to exlude from the sleeper")
appSelTxt.grid(column=0, row=0)

appSel = ttk.Combobox(window, values=getApps.getNames(), width=35)
appSel.grid(column=0, row=2)

def detectNewEntry():
    row = 2
    for x in selectedApps:
        if x == 3:
            break
        row = row + 1
        makeNewEntry("i", x, 0, row)

def makeNewEntry(tmpNme, tmpEntry, tmpCol, tmpRow):
    tmpNme = ttk.Label(text=tmpEntry)
    tmpNme.grid(column=tmpCol, row=tmpRow)

def addNoSleep():
    if appSel.get() != "":
        selectedApps.append(appSel.get())
    else:
        messagebox.showerror("empty")

def sleepIt():  # put apps to sleep manually

    if selectedApps.count == 3:
        messagebox.showinfo("need one app selected")
        exit()

    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Name'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    for line in proc.stdout:
        if line.rstrip():
            if not line.decode().rstrip() + ".exe" in selectedApps:
                appsToSleep.append(line.decode().rstrip() + ".exe")
                #print(line.decode().rstrip())
                #print(appsToSleep)

    for x in psutil.process_iter():
        if not x.name() in selectedApps:
            try:
                #x.suspend()
                print(" ||| putting app to bed ||| - " + x.name())
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass


def awakenIt():  # awaken the apps

    if selectedApps.count == 3:
        messagebox.showinfo("need one app selected")
        exit()

    for x in psutil.process_iter():
        for i in appsToSleep:
            if x.name() == i:
                try:
                    #x.resume()
                    print(" ||| awaken the apps |||" + x.name())
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

manStrtBtn = ttk.Button(window, text='Sleep', command=sleepIt) # manual start
manStrtBtn.grid(column=0, row=10)

manualStopBtn = ttk.Button(window, text='Wake up', command=awakenIt) # manual stop
manualStopBtn.grid(column=0, row=11)

addAppBtn = ttk.Button(window, text='add app', command=addNoSleep)  # dont sleep these apps
addAppBtn.grid(column=0, row=12)

window.mainloop()