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

has_exp = False


def open_peak1():
    global peak1,w,y1,peak1_text,a
    user_data = filedialog.askopenfilename()
    peak1 = pd.read_csv(user_data)
    peak1_text.set(user_data.rsplit('/', 1)[-1])
    y1 = np.array(peak1.iloc[:,1])
    x = np.array(peak1.iloc[:,0])
    a.set_xlim(np.min(x), np.max(x))
    print(a.get_xlim())


def open_peak2():
    global peak2,w,y2,peak2_text
    user_data = filedialog.askopenfilename()
    peak2 = pd.read_csv(user_data)
    peak2_text.set(user_data.rsplit('/', 1)[-1])
    y2 = np.array(peak2.iloc[:,1])


def open_exp():
    global exp,w,exp_text,has_exp
    user_data = filedialog.askopenfilename()
    exp = pd.read_csv(user_data)
    exp_text.set(user_data.rsplit('/', 1)[-1])
    has_exp = True


def update_ratio(value):
    global a,has_exp,y
    if 'peak1' not in globals() or 'peak2' not in globals():
        return

    global peak1,peak2,y1,y2

    value = float(value)
    print(value)

    y = y1 * value + y2 * (1 - value)

    y = (y-np.min(y))/(np.max(y)-np.min(y))

    xlim = a.get_xlim()
    a.cla()

    a.plot(peak1.iloc[:,0], y)

    if has_exp:
        a.plot(exp.iloc[:,0], exp.iloc[:,1])

    a.set_xlim(xlim)
    
    canvas.draw()

def save():
    global y
    x = peak1.iloc[:,0]
    csv = ""
    out = filedialog.asksaveasfile(mode='w')
    for i in range(0, y.size):
        csv += f"{float(x[i])},{float(y[i])}\n"
    out.write(csv)
    out.close()



f = Figure(figsize=(10, 5), dpi=100)
a = f.add_subplot(111)
# a.plot(x, y)
# a.plot(x, np.zeros(x.shape))

peak1_text = tk.StringVar()
peak1_text.set("browse peak1")

peak2_text = tk.StringVar()
peak2_text.set("browse peak2")

exp_text = tk.StringVar()
exp_text.set("browse exp")

tk.Button(root, textvariable=peak1_text,
          command=open_peak1).grid(row=0, column=0)
tk.Button(root, textvariable=peak2_text,
          command=open_peak2).grid(row=0, column=1)
tk.Button(root, textvariable=exp_text, command=open_exp).grid(row=0, column=2)
tk.Button(root, text="SAVE", command=save).grid(row=0, column=3)

w = tk.Scale(root, from_=0, to=1, resolution=0.01,
             orient=tk.HORIZONTAL, command=update_ratio)
w.grid(row=1, columnspan=4, sticky='NSEW')
w.set(0.5)

canvas = FigureCanvasTkAgg(f, root)
canvas.draw()
canvas.get_tk_widget().grid(row=33, columnspan=4)

toolbarFrame = tk.Frame(master=root)
toolbarFrame.grid(row=32, columnspan=3)
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)


root.mainloop()
