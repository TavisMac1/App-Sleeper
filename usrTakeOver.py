import subprocess
from asyncio.windows_events import NULL
from tabnanny import check
import psutil
#from mainGUI import selectedApps

appToMonitor = psutil
appsToSleep = []  # apps to sleep
selectedApps = ["obs64", "firefox", "Spotify", "discord", "Discord", "Code", "python", "node", "Sleeper"]

cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Name'
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

def sleepIt():  # put apps to sleep manually

    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Name'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    for line in proc.stdout:
        if line.rstrip():
            for x in selectedApps:
                if line.decode().rstrip() != x:
                    appsToSleep.append(line.decode().rstrip() + ".exe")
                    #print(line.decode().rstrip())

    for x in appsToSleep:
        print(x)
    exit()

    for x in psutil.process_iter():
        for i in appsToSleep:
            if x.name() == i:
                try:
                    x.suspend()
                    print(" ||| putting app to bed ||| - " + x.name())
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

def awakenIt(): #awaken the apps
    for x in psutil.process_iter():
        for i in appsToSleep:
            if x.name() == i:
                try:
                    x.resume()
                    print(" ||| awaken the apps |||")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
