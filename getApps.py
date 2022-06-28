import psutil
allAvailableApps = []  # get all available apps
def getNames():  # get names of apps -> for displaying to the user in GUI
    for x in psutil.process_iter():
        try:
            allAvailableApps.append(x.name())
            #print(x.name())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return allAvailableApps
