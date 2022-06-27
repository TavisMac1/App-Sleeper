from asyncio.windows_events import NULL
from tabnanny import check
import wmi
import psutil
winRef = wmi.WMI() #ref to WMI

appToExlude = "Steam.exe" #which app should be excluded?
allAvailableApps = [] #get all available apps
appToMonitor = "" #app for us to monitor, when its network usage is normal, awaken apps
suspendedApps = [] # apps that were suspended
#user defined
usrMmryUse = 0 #set a limiter for memory | cpu | network -> allow user defined for ram and cpu
usrCpuUse = 0
usrNetUse = 0 #hard code net use for now
#predefined system vals
mmryUse = 0  # set a limiter for memory | cpu | network -> allow user defined for ram and cpu
cpuUse = 1
netUse = 0  # hard code net use for now

def killAllTmp(tmpToIgnore): # put apps to sleep aside from exluded apps
    for x in psutil.process_iter():
        try:
            print(tmpToIgnore)
            #break
            processHigh = False
            #print(processName, ' : ', processID)
            if x.name() == appToExlude:  # capture the app to monitor
                appToMonitor = x
                while appToMonitor.cpu_percent() > 5.0:
                    print("cpu percent of steam higher than 5")
                    for x in psutil.process_iter():
                        if x.name() != tmpToIgnore:
                            if x.cpu_percent() > cpuUse:
                                x.suspend()
                                suspendedApps.append(x)
                    if appToMonitor.cpu_percent() < 5.0:
                        processHigh = True
                    if processHigh == True:
                        for y in suspendedApps:
                            y.resume()
                            print("trying to resume apps")
                #print(appToMonitor + "MONITORED APP")
            
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def checkStatus():
    for x in psutil.process_iter():
        try:
            #print(x.name)
            if x.name() == "Spotify.exe":  # capture the app to monitor
                print(x.username())

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
checkStatus()

def killSpotify():
    for x in psutil.process_iter():
        try:
            if x.name() == "Spotify.exe":
                x.suspend()
                print("Spotify suspended")
            else:
                print("spotify not found")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
#killSpotify()


def getNames(): #get names of apps -> for displaying to the user in GUI
    for x in psutil.process_iter():
        try:
            allAvailableApps.append(x.name())
            #print(x.name())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
getNames()