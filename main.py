import subprocess
from ast import And
from asyncio.windows_events import NULL
from tabnanny import check
import wmi
import psutil
winRef = wmi.WMI() #ref to WMI

appToExlude = "steam.exe" #which app should be excluded?
allAvailableApps = [] #get all available apps
appToMonitor = "" #app for us to monitor, when its network usage is normal, awaken apps
appsToSleep = [] # apps to sleep

cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Name'
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def killAllTmp(): # put apps to sleep aside from exluded apps

    for line in proc.stdout:
        if line.rstrip():
            if line.decode().rstrip() != appToExlude:
                appsToSleep.append(line.decode().rstrip() + ".exe")

    for x in psutil.process_iter():
        try:

            if x.name() == appToExlude:  # capture the app to monitor
                appToMonitor = x
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    while 1:
        print("cpu percent of steam higher than 1")
        for x in psutil.process_iter():

            if x.name() != appToMonitor.name():
                for z in appsToSleep:
                    if x.name() == z:
                        try:
                            if x.cpu_percent(interval=0.1) > 0.1:
                                print("putting apps to sleep")
                                x.suspend()
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                            pass

        if appToMonitor.cpu_percent(interval=0.1) < 1.0:
           
            for x in psutil.process_iter():
                try:
                    for i in appsToSleep:
                        if x.name == i:
                            print("trying to wake up apps")
                            x.resume()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            break
killAllTmp()

def getNames(): #get names of apps -> for displaying to the user in GUI
    for x in psutil.process_iter():
        try:
            allAvailableApps.append(x.name())
            print(x.name())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
#getNames()