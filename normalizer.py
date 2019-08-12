from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
import pandas as pd
import numpy as np
from tkinter import filedialog
from tkinter import simpledialog
import tkinter as tk

matplotlib.use("TkAgg")

class Normalizer():
    def __init__(self, root):
        data = pd.read_csv(filedialog.askopenfilename())

        self.x = np.array(data.iloc[:, 0])
        self.y = np.array(data.iloc[:, 1])


        tk.Label(root, text="Lower Bound:").grid(row=0)
        tk.Label(root, text="Upper Bound:").grid(row=1)

        self.e1 = tk.Entry(root)
        self.e2 = tk.Entry(root)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        f = Figure(figsize=(10, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot(self.x, self.y)
        a.plot(self.x, np.zeros(self.x.shape))
        self.a = a

        canvas = FigureCanvasTkAgg(f, root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, columnspan=5)
        self.canvas = canvas

        toolbarFrame = tk.Frame(master=root)
        toolbarFrame.grid(row=2,columnspan=5)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

        tk.Button(root, text="NORMALIZE", command=self.normalize).grid(row=0, column=2, rowspan=2)
        tk.Button(root, text="CLEAR", command=self.clear).grid(row=0, column=3, rowspan=2)
        tk.Button(root, text="SAVE", command=self.save).grid(row=0, column=4, rowspan=2)

    def normalize(self):
        x = self.x
        y = self.y
        x_min = float(self.e1.get())
        x_max = float(self.e2.get())

        idx = np.where(np.logical_and(x>x_min, x<x_max))
        zero = np.trapz(y[idx], x[idx]) / (x_max - x_min)
        
        self.g = (y-zero)/(np.max(y)-zero)
        self.a.plot(x, self.g)
        self.canvas.draw()

    def clear(self):
        self.a.cla()
        self.a.plot(self.x, self.y)
        self.a.plot(self.x, np.zeros(self.x.shape))
        self.canvas.draw()

    def save(self):
        csv = ""
        out = filedialog.asksaveasfile(mode='w')
        for i in range(0, self.g.size):
            csv += f"{float(self.x[i])},{float(self.g[i])}\n"
        out.write(csv)
        out.close()

if __name__ == "__main__":
    master = tk.Tk()

    Normalizer(master)
    master.mainloop()