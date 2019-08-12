from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
import pandas as pd
import numpy as np
from tkinter import filedialog
from tkinter import simpledialog
import tkinter as tk

matplotlib.use("TkAgg")

has_exp = False

class PeakCombiner:
    def __init__(self, root):
        f = Figure(figsize=(10, 5), dpi=100)
        self.a = f.add_subplot(111)

        self.peak1_text = tk.StringVar()
        self.peak1_text.set("browse peak1")

        self.peak2_text = tk.StringVar()
        self.peak2_text.set("browse peak2")

        self.exp_text = tk.StringVar()
        self.exp_text.set("browse exp")

        tk.Button(root, textvariable=self.peak1_text,
                command=self.open_peak1).grid(row=0, column=0)
        tk.Button(root, textvariable=self.peak2_text,
                command=self.open_peak2).grid(row=0, column=1)
        tk.Button(root, textvariable=self.exp_text, command=self.open_exp).grid(row=0, column=2)
        tk.Button(root, text="SAVE", command=self.save).grid(row=0, column=3)

        self.w = tk.Scale(root, from_=0, to=1, resolution=0.01,
                    orient=tk.HORIZONTAL, command=self.update_ratio)
        self.w.grid(row=1, columnspan=4, sticky='NSEW')
        self.w.set(0.5)

        canvas = FigureCanvasTkAgg(f, root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=33, columnspan=4)

        toolbarFrame = tk.Frame(master=root)
        toolbarFrame.grid(row=32, columnspan=3)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        self.canvas = canvas
        self.has_exp = False

    def open_peak1(self):
        user_data = filedialog.askopenfilename()
        self.peak1 = pd.read_csv(user_data)
        self.peak1_text.set(user_data.rsplit('/', 1)[-1])
        self.y1 = np.array(self.peak1.iloc[:,1])
        x = np.array(self.peak1.iloc[:,0])
        self.a.set_xlim(np.min(x), np.max(x))

    def open_peak2(self):
        user_data = filedialog.askopenfilename()
        self.peak2 = pd.read_csv(user_data)
        self.peak2_text.set(user_data.rsplit('/', 1)[-1])
        self.y2 = np.array(self.peak2.iloc[:,1])


    def open_exp(self):
        user_data = filedialog.askopenfilename()
        self.exp = pd.read_csv(user_data)
        self.exp_text.set(user_data.rsplit('/', 1)[-1])
        self.has_exp = True


    def update_ratio(self, value):
        if not hasattr(self, 'peak1') or not hasattr(self, 'peak2'):
            return

        value = float(value)

        y = self.y1 * value + self.y2 * (1 - value)

        y = (y-np.min(y))/(np.max(y)-np.min(y))

        xlim = self.a.get_xlim()
        self.a.cla()

        self.a.plot(self.peak1.iloc[:,0], y)

        if self.has_exp:
            self.a.plot(self.exp.iloc[:,0], self.exp.iloc[:,1])

        self.a.set_xlim(xlim)
        
        self.canvas.draw()

        self.y = y

    def save(self):
        x = self.peak1.iloc[:,0]
        csv = ""
        out = filedialog.asksaveasfile(mode='w')
        for i in range(0, self.y.size):
            csv += f"{float(x[i])},{float(self.y[i])}\n"
        out.write(csv)
        out.close()

if __name__ == "__main__":
    master = tk.Tk()

    PeakCombiner(master)
    master.mainloop()
