from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from turtle import bgcolor
from tkinter.ttk import Notebook
import autoMode
import getApps
import usrTakeOver
#GUI setup
window = Tk()
window.geometry('600x600')
window.title('Sleeper')
window.configure(bg='purple')

#selectedApps = ["obs64", "firefox", "Spotify", "Code", "discord", "Discord"]
selectedApps = []

appSelTxt = ttk.Label(text="choose apps to exlude from the sleeper")
appSelTxt.grid(column=0, row=0)

appSel = ttk.Combobox(window, values=getApps.getNames(), width=35)
appSel.grid(column=0, row=2)

def detectNewEntry():
    row = 2
    for x in selectedApps:
        if x == 0:
            break
        row = row + 1
        makeNewEntry("i", x, 0, row)

def makeNewEntry(tmpNme, tmpEntry, tmpCol, tmpRow):
    tmpNme = ttk.Label(text=tmpEntry)
    tmpNme.grid(column=tmpCol, row=tmpRow)

def addNoSleep():
    if appSel.get() != "":
        selectedApps.append(appSel.get())
        for x in selectedApps:
            print(x)
    else:
        messagebox.showerror("empty")

manStrtBtn = ttk.Button(window, text='Sleep', command=usrTakeOver.sleepIt) # manual start
manStrtBtn.grid(column=0, row=10)

manualStopBtn = ttk.Button(window, text='Wake up', command=usrTakeOver.awakenIt) # manual stop
manualStopBtn.grid(column=0, row=11)

addAppBtn = ttk.Button(window, text='add app', command=addNoSleep)  # dont sleep these apps
addAppBtn.grid(column=0, row=12)

window.mainloop()
