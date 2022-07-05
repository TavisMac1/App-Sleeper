from turtle import bgcolor
import psutil
from tabnanny import check
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Notebook
from PIL import ImageTk, Image
import winsound
import autoMode
import getApps
import getUser

#GUI setup
window = Tk()
window.geometry('600x400')
window.title('Goodnight Computer!')
window.configure(bg='pink')
window.resizable(False, False)
window.iconbitmap('images/favicon.ico')

photoimage = ImageTk.PhotoImage(file="images/Untitled_design.png")

width, height = 600, 400
canvas = Canvas(window, bg="pink", width=width, height=height)
canvas.pack()
s = ttk.Style()
s.theme_use('clam')

canvas.create_image(-40, 100, image=photoimage, anchor=NW)

#selectedApps = ["obs64", "firefox", "Spotify", "Code", "discord", "Discord"] # hard coded test apps
cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Name'
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
selectedApps = ["python.exe",
                "Taskmgr.exe",
                "Code.exe",
                "ApplicationFrameHost.exe",
                "TextInputHost.exe"]  # supply some defaults that we don't ever want put to sleep
appsToSleep = []  # apps to sleep
appToMonitor = []

appSelTxt = ttk.Label(
    text= getUser.getUsr()).place(x=190, y=0)

appSelTxt = ttk.Label(
    text=" |> choose apps to exlude from the sleeper <|", background="pink").place(x=190, y=80)

appSel = ttk.Combobox(window, values=getApps.getNames(), width=40)
appSel.place(x=180, y=100)

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
        winsound.Beep(300, 300)
        messagebox.showinfo(title="App added", message="App has been added -> " + appSel.get())
    else:
        messagebox.showerror(
            title="Err", message="need at least one app selected")

def sleepIt():  # put apps to sleep manually
    winsound.Beep(100, 300)
    if selectedApps.count == 4:
        messagebox.showerror(title="Err", message="need at least one app selected")
        exit()

    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Name'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    for line in proc.stdout:
        if line.rstrip():
            if not line.decode().rstrip() + ".exe" in selectedApps:
                appsToSleep.append(line.decode().rstrip() + ".exe")

    for x in psutil.process_iter():
        if x.name() in appsToSleep:
            try:
                x.suspend()
                #print(" ||| putting app to bed ||| - " + x.name())
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

def awakenIt():  # awaken the apps
    winsound.Beep(200, 300)
    if selectedApps.count == 4:
        messagebox.showerror(
            title="Err", message="need at least one app selected")
        exit()

    for x in psutil.process_iter():
        if x.name() in appsToSleep:
            try:
                x.resume()
                print(" ||| awaken the apps |||" + x.name())
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

def viewAdded():
    i = 0
    anotherWin = Toplevel(window)
    anotherWin.title("added apps")
    anotherWin.geometry("300x600")
    anotherWin.configure(bg='pink')
    anotherWin.resizable(False, False)
    anotherWin.iconbitmap('images/favicon.ico')
    for x in selectedApps:
        i = i + 1
        Label(anotherWin, text=x, background="pink").grid(column=4, row=i)

def openAuto():
    autoApp = ""
    anotherWin = Toplevel(window)
    anotherWin.title("auto mode")
    anotherWin.geometry("600x400")
    anotherWin.configure(bg='pink')
    anotherWin.resizable(False, False)
    anotherWin.iconbitmap('images/favicon.ico')
    Label(anotherWin, text=" |> choose one app to monitor <|", background="pink").place(x=220, y=80)
    appMonitorSel = ttk.Combobox(anotherWin, values=getApps.getNames(), width=40)
    appMonitorSel.place(x=180, y=100)
    Button(anotherWin, text='add app', command=lambda:addAutoApp(
        appMonitorSel.get())).place(x=300, y=150)  # open automatic mode
    Button(anotherWin, text='start automode', command=startAutoMode).place(
        x=200, y=150)  # open automatic mode

def addAutoApp(tmpApp):
    if tmpApp != "":
            appToMonitor.append(tmpApp)
            print("app to monitor added")
            messagebox.showinfo(title="Success", message= tmpApp + " was added")
    else:
        messagebox.showinfo(title="Err", message="must select 1 app")

def startAutoMode():
    if appToMonitor[0] != "":
        autoMode.automaticSleep(appToMonitor[0])
    else:
        messagebox.showerror(title="Err", message="no app to monitor :(")
        exit()


manStrtBtn = ttk.Button(window, text='sleep', 
                        command=sleepIt).place(x=175, y=150)  # manual start

manualStopBtn = ttk.Button(window, text='wake up',
                           command=awakenIt).place(x=275, y=150)  # manual stop

addAppBtn = ttk.Button(window, text='add app',
                       command=addNoSleep).place(x=375, y=150)  # dont sleep these apps

viewAddedBtn = ttk.Button(window, text='view added',
                       command=viewAdded).place(x=275, y=200)  # dont sleep these apps

autoModeBtn = ttk.Button(window, text='auto mode',
                          command=openAuto).place(x=175, y=200)  # open automatic mode

window.mainloop()