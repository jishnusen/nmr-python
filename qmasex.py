import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import fortran_90_ports.qmasexfort as fort


class Qmasex:
    def __init__(self, master):
        self.frame = master

        tk.Label(self.frame, text="larmor frequency (MHz)").grid(
            sticky=tk.W, row=0)
        tk.Label(self.frame, text="spin quantum number").grid(
            sticky=tk.W, row=1)

        tk.Label(self.frame, text="Upper plot limit").grid(
            sticky=tk.W, row=0, column=3)
        tk.Label(self.frame, text="Lower plot limit").grid(
            sticky=tk.W, row=1, column=3)

        tk.Label(self.frame).grid(row=2, columnspan=5)

        tk.Label(self.frame, text="asymmetry parameter for site #1 (MHz)").grid(
            sticky=tk.W, row=3)
        tk.Label(self.frame, text="Quadrupolar coupling constant for site #1 (Mhz)").grid(
            sticky=tk.W, row=4)
        tk.Label(self.frame, text="Isotropic chemical shift for site #1 (ppm)").grid(
            sticky=tk.W, row=5)
        tk.Label(self.frame, text="number of polar angles for site #1").grid(
            sticky=tk.W, row=6)
        tk.Label(self.frame, text="number of azimuthal angles for site #1").grid(
            sticky=tk.W, row=7)
        tk.Label(self.frame, text="T2 for site #1 (seconds)").grid(
            sticky=tk.W, row=8)

        tk.Label(self.frame).grid(column=2, rowspan=10)

        tk.Label(self.frame, text="asymmetry parameter for site #2 (MHz)").grid(
            sticky=tk.W, row=3, column=3)
        tk.Label(self.frame, text="Quadrupolar coupling constant for site #2 (Mhz)").grid(
            sticky=tk.W, row=4, column=3)
        tk.Label(self.frame, text="Isotropic chemical shift for site #2 (ppm)").grid(
            sticky=tk.W, row=5, column=3)
        tk.Label(self.frame, text="number of polar angles for site #2").grid(
            sticky=tk.W, row=6, column=3)
        tk.Label(self.frame, text="number of azimuthal angles for site #2").grid(
            sticky=tk.W, row=7, column=3)
        tk.Label(self.frame, text="T2 for site #2 (seconds)").grid(
            sticky=tk.W, row=8, column=3)

        self.v = tk.StringVar()
        self.user_data = ""
        tk.Label(self.frame, textvariable=self.v).grid(row=9, column=1)

        tk.Label(self.frame, text="jump frequency (Hz)").grid(
            sticky=tk.W, row=9, column=3)

        self.e_vlf = tk.Entry(self.frame)
        self.e_sqn = tk.Entry(self.frame)
        self.e_eta1 = tk.Entry(self.frame)
        self.e_eqqh1 = tk.Entry(self.frame)
        self.e_cs1 = tk.Entry(self.frame)
        self.e_npolar1 = tk.Entry(self.frame)
        self.e_nazim1 = tk.Entry(self.frame)
        self.e_eta2 = tk.Entry(self.frame)
        self.e_eqqh2 = tk.Entry(self.frame)
        self.e_cs2 = tk.Entry(self.frame)
        self.e_npolar2 = tk.Entry(self.frame)
        self.e_nazim2 = tk.Entry(self.frame)
        self.e_hi = tk.Entry(self.frame)
        self.e_lo = tk.Entry(self.frame)
        self.e_t2one = tk.Entry(self.frame)
        self.e_t2two = tk.Entry(self.frame)
        self.e_jfreq = tk.Entry(self.frame)

        self.e_vlf.grid(row=0, column=1)
        self.e_sqn.grid(row=1, column=1)

        self.e_eta1.grid(row=3, column=1)
        self.e_eqqh1.grid(row=4, column=1)
        self.e_cs1.grid(row=5, column=1)
        self.e_npolar1.grid(row=6, column=1)
        self.e_nazim1.grid(row=7, column=1)

        self.e_eta2.grid(row=3, column=4)
        self.e_eqqh2.grid(row=4, column=4)
        self.e_cs2.grid(row=5, column=4)
        self.e_npolar2.grid(row=6, column=4)
        self.e_nazim2.grid(row=7, column=4)

        self.e_hi.grid(row=0, column=4)
        self.e_lo.grid(row=1, column=4)
        self.e_t2one.grid(row=8, column=1)
        self.e_t2two.grid(row=8, column=4)
        self.e_jfreq.grid(row=9, column=4)

        tk.Button(self.frame, text="BROWSE",
                  command=self.filechoose).grid(row=9)
        tk.Button(self.frame, text="PLOT", command=self.callback).grid(row=10)
        tk.Button(self.frame, text="SAVE",
                  command=self.save).grid(row=10, column=4)

    def plot(self, sqn, vlf, eta1, eqqh1, cs1, t2one, npolar1, nazim1,
             eta2, eqqh2, cs2, t2two, npolar2, nazim2, hi, lo,
             jfreq, user_data):
        self.f, self.g = self.qmasex(sqn, vlf, eta1, eqqh1, cs1, t2one, npolar1, nazim1,
                                      eta2, eqqh2, cs2, t2two, npolar2, nazim2, hi, lo,
                                      jfreq)

        gen_data = plt.plot(self.f, self.g, label="Simulation")

        data = user_data != ""

        if data:
            infile = pd.read_csv(user_data)
            user_data = plt.plot(
                infile.iloc[:, 0], infile.iloc[:, 1], label="User Data")

        plt.legend(loc='upper right')

        plt.gca().invert_xaxis()
        plt.xlim(lo, hi)
        plt.show()

    @staticmethod
    def qmasex(sqn, vlf, eta1, eqqh1, cs1, t2one, npolar1, nazim1,
                eta2, eqqh2, cs2, t2two, npolar2, nazim2, hi, lo,
                jfreq):
        npts = 1000
        f = np.zeros(npts)
        g = np.zeros(npts)
        cs1 = cs1 * vlf
        cs2 = cs2 * vlf

        freq1 = Qmasex.quadfreq(npolar1, nazim1, cs1, eta1, eqqh1, vlf, sqn)
        freq2 = Qmasex.quadfreq(npolar2, nazim2, cs2, eta2, eqqh2, vlf, sqn)
        nfreq1 = npolar1*nazim1
        nfreq2 = npolar2*nazim2

        for i in range(0, nfreq2):
            freq1[i+nfreq1] = freq2[i]

        nfreq = nfreq1+nfreq2
        jfreq = jfreq/float(nfreq-1)
        ar1 = float(nfreq)*jfreq+1.0/t2one
        ar2 = float(nfreq)*jfreq+1.0/t2two
        hi = hi*vlf
        lo = lo*vlf
        dwf = (hi-lo)/float(npts-1)
        gmax = 0.0

        for i in range(0, npts):
            wf = lo+dwf*float(i)
            l = complex(0.0, 0.0)
            for j in range(0, nfreq1):
                l = l+complex(1.0, 0.0)/complex(ar1, wf-freq1[j])
            nfr = nfreq1
            for j in range(nfr, nfreq):
                l = l+complex(1.0, 0.0)/complex(ar2, wf-freq1[j])
            g[i] = (l/(complex(1.0, 0.0)-(complex(jfreq, 0.0)*l))).real
            g[i] = g[i] / float(nfreq)
            if g[i] > gmax:
                gmax = g[i]

        for i in range(0, npts):
            wf = lo + i * dwf
            wf = wf / vlf
            f[i] = wf
            g[i] = g[i] / gmax

        return f, g
        
    @staticmethod
    def quadfreq(npolar, nazim, cs, eta, eqqh, vlf, sqn):
        freq = np.zeros(100000)
        dpolar = 2.0 / float(npolar-1)
        dazim = np.pi / float(nazim-1)
        vq = (3.0*eqqh*1.0e6)/(2.0*sqn*(2.0*sqn-1.0))
        f = (sqn*(sqn+1.0))-0.75
        f = f*vq*vq/(6.0*vlf*1.0e6)
        k = -1

        for i in range(0, npolar):
            ct = -1.0+dpolar*float(i)
            ct2 = ct*ct
            for j in range(0, nazim):
                k=k+1
                phi=dazim*float(j)
                c2phi=np.cos(2.0*phi)
                aphi=1.3125-(0.875*eta*c2phi)+(.1458*eta*eta*c2phi*c2phi)
                bphi=-1.125+((eta*eta)/12)+(eta*c2phi)-(.2917*eta*eta*c2phi*c2phi)
                cphi=0.3125-(.125*eta*c2phi)+(0.1458*eta*eta*c2phi*c2phi)
                v=-((aphi*ct2*ct2)+(bphi*ct2)+cphi)
                freq[k]=(v*f)+cs

        return freq

    def callback(self):
        self.plot(
            float(self.e_sqn.get()), 
            float(self.e_vlf.get()), 
            float(self.e_eta1.get()), 
            float(self.e_eqqh1.get()), 
            float(self.e_cs1.get()), 
            float(self.e_t2one.get()), 
            int(self.e_npolar1.get()), 
            int(self.e_nazim1.get()),
            float(self.e_eta2.get()), 
            float(self.e_eqqh2.get()), 
            float(self.e_cs2.get()), 
            float(self.e_t2two.get()), 
            int(self.e_npolar2.get()), 
            int(self.e_nazim2.get()), 
            float(self.e_hi.get()), 
            float(self.e_lo.get()),
            float(self.e_jfreq.get()), 
            self.user_data)
        return

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

    Qmasex(master)
    master.mainloop()
