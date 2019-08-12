import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import filedialog

class Q3Q4:
    def __init__(self, root):
        tk.Label(root, text="Larmor Frequency (MHz)").grid(row=0)
        tk.Label(root, text="Delta-Parallel (ppm)").grid(row=1)
        tk.Label(root, text="Delta-Perpendicular (ppm)").grid(row=2)
        tk.Label(root, text="Number of cosine-thetas").grid(row=3)
        tk.Label(root, text="jump frequency (Hz)").grid(row=4)
        tk.Label(root, text="T2 (seconds)").grid(row=5)
        tk.Label(root, text="upper plot limit (ppm)").grid(row=6)
        tk.Label(root, text="lower plot limit (ppm)").grid(row=7)
        tk.Label(root, text="Gaussian Peak Position (ppm)").grid(row=8)
        self.v = tk.StringVar()
        self.user_data = ""
        tk.Label(root, textvariable=self.v).grid(row=9, column = 1)

        self.e_vlf = tk.Entry(root)
        self.e_avspara = tk.Entry(root)
        self.e_avsperp = tk.Entry(root)
        self.e_ncth = tk.Entry(root)
        self.e_jfreq = tk.Entry(root)
        self.e_t2 = tk.Entry(root)
        self.e_hi = tk.Entry(root)
        self.e_lo = tk.Entry(root)
        self.e_posq4 = tk.Entry(root)

        self.e_vlf.grid(row=0, column=1)
        self.e_avspara.grid(row=1, column=1)
        self.e_avsperp.grid(row=2, column=1)
        self.e_ncth.grid(row=3, column=1)
        self.e_jfreq.grid(row=4, column=1)
        self.e_t2.grid(row=5, column=1)
        self.e_hi.grid(row=6, column=1)
        self.e_lo.grid(row=7, column=1)
        self.e_posq4.grid(row=8, column=1)

        tk.Button(root, text="BROWSE", command = self.filechoose).grid(row=9)
        tk.Button(root, text="PLOT", command = self.callback).grid(row=10)
        tk.Button(root, text="SAVE", command = self.save).grid(row=10, column = 1)

    def plot(self, vlf, avspara, avsperp, ncth, jfreq, t2, fu, fl, posq4, user_data):
        self.f,self.g = self.q3q4stex(vlf, avspara, avsperp, ncth, jfreq, t2, fu, fl, posq4)

        gen_data = plt.plot(self.f,self.g,label="Simulation") 

        data = user_data != ""

        if data:
            infile = pd.read_csv(user_data)
            user_data = plt.plot(infile.iloc[:, 0], infile.iloc[:, 1], label="User Data")

        plt.legend(loc='upper right')

        plt.gca().invert_xaxis()
        plt.xlim(fl, fu)
        plt.show()

    @staticmethod
    def q3q4stex(vlf, avspara, avsperp, ncth, jfreq, t2, fu, fl, posq4):
        f = np.zeros(1000)
        w = np.zeros(61000)
        g = np.zeros(1000)
        q4int = np.zeros(5000)
        pq4 = np.zeros(1000)
        gnsperp = np.zeros(50)
        sperp = np.zeros(50)
        spara = np.zeros(50)

        nf = 1000
        f0 = vlf
        w0 = 2 * np.pi * f0

        dcth = 2.0 / float(ncth - 1)
        wfu = fu * w0
        wfl = fl * w0
        dwf = (wfu - wfl) / float(nf - 1)
        df = (fu - fl) / float(nf - 1)

        for i in range(0, nf):
            f[i] = fl + df * float(i - 1)
        
        width = 22.0

        deltaq4 = (2.0 * width / 160.0)
        width = width / 2.354
        width = 1.0 / width
        sum = 0.0

        for i in range(0, 161):
            gb = 0.0
            pq4[i] = posq4 - deltaq4 * float(81 - i)
            gb = (pq4[i] - posq4) * width
            gb = (gb * gb) / 2.0
            gb = width * 0.3989 * np.exp(-gb)
            q4int[i] = gb
            sum = sum + q4int[i]
        
        for i in range(0, 161):
            q4int[i] = q4int[i] * float(ncth) / sum

        k = 0
        m = 0

        for i in range(0, 161):
            m = m + int(round(q4int[i]))
            for j in range(k,m):
                w[ncth + j] = pq4[i] * w0
            
            k = m
        
        jfreq = jfreq / (float(2*ncth) - 1.0)
        ar = float(2* ncth) * jfreq + 1.0 / t2

        sum = 0.0
        gwidth = 20.0
        deltagw = 1.5 * gwidth / 40.0
        gwidth = 1.0 / (gwidth / 2.354)

        for i in range(0, 31):
            sperp[i] = avsperp - float(21 - i) * deltagw
            spara[i] = avspara - float(21 - i) * deltagw
            gb = 0.0
            gb = (sperp[i] - avsperp) * gwidth
            gb = (gb * gb) / 2.0
            gb = gwidth * 0.3989 * np.exp(-gb)
            gnsperp[i] = gb
            sum = sum + gb
        
        for i in range(0, 41):
            gnsperp[i] = gnsperp[i] * (float(ncth) / sum)
        
        ik = 0
        im = 0

        for k in range(0, 41):
            ng = int(round(gnsperp[k]))
            im = im + ng
            dcth = 2.0 / float(ng - 1)
            wperp = sperp[k] * w0
            wpara = spara[k] * w0
            for i in range(ik, im):
                ii = i - ik
                cth = 1.0 - dcth * float(ii)
                csqth = cth * cth
                ssqth = 1.0 - csqth
                w[i] = wperp * ssqth + wpara * csqth
            
            ik = im
        
        ncth = 2 * ncth
        for j in range(0, nf):
            wf = wfl + dwf * float(j)
            l = complex(0.0, 0.0)
            for k in range(0, ncth):
                l = l + complex(1.0, 0.0) / complex(ar, wf - w[k])
            
            g[j] = (l/(complex(1.0,0.0)-(complex(jfreq,0.0)*l))).real
            g[j] = g[j] / float(ncth)
        
        rmax = 0.0

        for i in range(0, nf):
            if g[i] > rmax: rmax = g[i]
        
        for i in range(0, nf):
            ppm = fl + df * float(i)
            g[i] = g[i] / rmax
            f[i] = ppm

        return f,g

    def callback(self):
        self.plot(float(self.e_vlf.get()), float(self.e_avspara.get()), float(self.e_avsperp.get()), int(self.e_ncth.get()), 
            float(self.e_jfreq.get()), float(self.e_t2.get()), float(self.e_hi.get()), float(self.e_lo.get()), float(self.e_posq4.get()),
            self.user_data)

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

    Q3Q4(master)
    master.mainloop()
