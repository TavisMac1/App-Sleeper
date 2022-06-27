from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import main
#GUI setup
window = Tk()
window.geometry('300x300')
window.title('Sleeper')

selectedApps = []

main.getNames()

availableApps = main.allAvailableApps
appSel = ttk.Combobox(window, values=availableApps, width=15)
appSel.grid(column=2, row=0)

#sleepBtn = ttk.Button(window, text='Sleep', command=main.killAllTmp("Steam.exe"))
#sleepBtn.grid(column=1, row=5)

window.mainloop()
