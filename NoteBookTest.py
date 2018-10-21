from tkinter import *
from tkinter import ttk
window = Tk()
notebook = ttk.Notebook(window,width=900)
tabs = ["Tab 1","Tab 2","Tab 3", "Tab 4", "Tab 5"]
for i in range(len(tabs)):
    hold = tabs[i]
    tabs[i] = [tabs[i],Frame(notebook)]
    notebook.add(tabs[i][1],text=tabs[i][0])
    tabs[i].append(Label(tabs[i][1],text=tabs[i][0]))
    tabs[i][2].pack(side="left")
notebook.pack()
window.mainloop()
