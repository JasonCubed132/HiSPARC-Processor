from tkinter import *
from tkinter import ttk
def GenTabs(window,tabs=["Tab 1","Tab 2","Tab 3", "Tab 4", "Tab 5"],width=800):
    notebook = ttk.Notebook(window,width=width)
    for i in range(len(tabs)):
        hold = tabs[i]
        tabs[i] = [tabs[i],Frame(notebook)]
        notebook.add(tabs[i][1],text=tabs[i][0])
        #tabs[i].append(Label(tabs[i][1],text=tabs[i][0]))
        #tabs[i][2].pack(side="left")
    return [notebook,tabs]
