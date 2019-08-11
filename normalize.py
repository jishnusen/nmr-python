from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
import pandas as pd
import numpy as np
from tkinter import filedialog
from tkinter import simpledialog
import tkinter as tk

root = tk.Tk()

matplotlib.use("TkAgg")

data = pd.read_csv(filedialog.askopenfilename())

x = np.array(data.iloc[:, 0])
y = np.array(data.iloc[:, 1])


tk.Label(root, text="Lower Bound:").grid(row=0)
tk.Label(root, text="Upper Bound:").grid(row=1)

e1 = tk.Entry(root)
e2 = tk.Entry(root)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

f = Figure(figsize=(10, 5), dpi=100)
a = f.add_subplot(111)
a.plot(x, y)
a.plot(x, np.zeros(x.shape))

canvas = FigureCanvasTkAgg(f, root)
canvas.draw()
canvas.get_tk_widget().grid(row=3, columnspan=5)

toolbarFrame = tk.Frame(master=root)
toolbarFrame.grid(row=2,columnspan=5)
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

def normalize():
    global x,y,g
    x_min = float(e1.get())
    x_max = float(e2.get())

    idx = np.where(np.logical_and(x>x_min, x<x_max))
    zero = np.trapz(y[idx], x[idx]) / (x_max - x_min)
    print(zero)
    
    g = (y-zero)/(np.max(y)-zero)
    a.plot(x, g)
    canvas.draw()

def clear():
    a.cla()
    a.plot(x, y)
    a.plot(x, np.zeros(x.shape))
    canvas.draw()

def save():
    csv = ""
    out = filedialog.asksaveasfile(mode='w')
    for i in range(0, g.size):
        csv += f"{float(x[i])},{float(g[i])}\n"
    out.write(csv)
    out.close()


tk.Button(root, text="NORMALIZE", command=normalize).grid(row=0, column=2, rowspan=2)
tk.Button(root, text="CLEAR", command=clear).grid(row=0, column=3, rowspan=2)
tk.Button(root, text="SAVE", command=save).grid(row=0, column=4, rowspan=2)

root.title("normalize")
root.mainloop()
