import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import filedialog

class Gauss:
    def __init__(self, master):
        self.frame = master

        tk.Label(master, text="larmor frequency (MHz)").grid(row=0)
        tk.Label(master, text="peak pos (csv, ppm)").grid(row=1)
        tk.Label(master, text="intensities (csv, rel)").grid(row=2)
        tk.Label(master, text="lower plot limit (ppm)").grid(row=3)
        tk.Label(master, text="upper plot limit (ppm)").grid(row=4)
        tk.Label(master, text="T2 (seconds)").grid(row=5)
        tk.Label(master, text="jump frequency (Hz)").grid(row=6)
        self.v = tk.StringVar()
        self.user_data = ""
        tk.Label(master, textvariable=self.v).grid(row=7, column = 1)

        self.e_vlf = tk.Entry(master)
        self.e_pos = tk.Entry(master)
        self.e_inp = tk.Entry(master)
        self.e_lo = tk.Entry(master)
        self.e_hi = tk.Entry(master)
        self.e_t2 = tk.Entry(master)
        self.e_jfreq = tk.Entry(master)

        self.e_vlf.grid(row=0, column=1)
        self.e_pos.grid(row=1, column=1)
        self.e_inp.grid(row=2, column=1)
        self.e_lo.grid(row=3, column=1)
        self.e_hi.grid(row=4, column=1)
        self.e_t2.grid(row=5, column=1)
        self.e_jfreq.grid(row=6, column=1)

        tk.Button(master, text="BROWSE", command = self.filechoose).grid(row=7)
        tk.Button(master, text="PLOT", command = self.callback).grid(row=8)
        tk.Button(master, text="SAVE", command = self.save).grid(row=8, column = 1)
    def plot(self, vlf, pos, inp, lo, hi, t2, jfreq, user_data):
        vlf = vlf * 2. * np.pi
        inp = inp.T
        w = pos * vlf
        wk = np.asmatrix(np.zeros([pos.size,pos.size]))
        lo = lo * vlf
        hi = hi * vlf
        npts = 1000
        t2 = t2 * np.ones([pos.size])
        t2 = -1/t2
        pim = np.ones([w.size,1])*inp.T+np.diag(-(inp.sum()-inp))-np.diag(inp)
        weight = inp
        sumw = weight.sum()
        jfreq = jfreq / (sumw - 1.)
        df = (hi - lo) / (npts - 1.)
        u = np.arange(1,npts+1)
        f = lo + df * (u - 1)
        n = inp.size
        g = np.zeros(npts)
        v = np.arange(1,n)
        k = np.arange(1,n)
        jfreqd = jfreq * np.diag(pim) + t2.T
        omgo = (jfreq + 0j) * (pim + 0j)
        for i in range(0,npts):
            wk = w - f[i]
            omg = omgo-np.diag(np.diag(omgo)) + np.diag(jfreqd+wk*1j)
            g[i] = np.real(np.sum(np.linalg.solve(omg,weight)))

        g = np.absolute(g)
        f = f/vlf
        g = g/np.amax(g)

        self.f,self.g = f,g

        gen_data = plt.plot(self.f,self.g,label="Simulation") 

        if user_data != "":
            infile = np.loadtxt((user_data), delimiter=",")
            user_data = plt.plot(infile[:, 0], infile[:, 1], label="User Data")

        plt.legend(loc='upper right')

        plt.gca().invert_xaxis()
        plt.show()

    def callback(self):
        self.plot(float(self.e_vlf.get()), np.fromstring(self.e_pos.get(), sep=","), np.fromstring(self.e_inp.get(), sep=","), float(self.e_lo.get()), 
            float(self.e_hi.get()), float(self.e_t2.get()), float(self.e_jfreq.get()), self.user_data)

    def filechoose(self):
        self.user_data = filedialog.askopenfilename()
        self.v.set(self.user_data.rsplit('/', 1)[-1])

    def save(self):
        csv = ""
        out = filedialog.asksaveasfile(mode='w')
        for i in range(0, self.g.size):
            csv += f"{float(self.f[i])},{float(self.g[i])}\n"
        out.write(csv)
        out.close()

if __name__ == "__main__":
    master = tk.Tk()

    Gauss(master)
    master.mainloop()
