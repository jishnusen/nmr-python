import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import filedialog

class BCSax:
    def __init__(self, master):
        self.frame = master

        tk.Label(self.frame, text="larmor frequency (MHz)").grid(row=0)
        tk.Label(self.frame, text="sigma11 (ppm)").grid(row=1)
        tk.Label(self.frame, text="sigma22 (ppm)").grid(row=2)
        tk.Label(self.frame, text="sigma33 (ppm)").grid(row=3)
        tk.Label(self.frame, text="jump frequency (Hz)").grid(row=4)
        tk.Label(self.frame, text="T2 (seconds)").grid(row=5)
        tk.Label(self.frame, text="upper plot limit (ppm)").grid(row=6)
        tk.Label(self.frame, text="lower plot limit (ppm)").grid(row=7)
        self.v = tk.StringVar()
        self.user_data = ""
        tk.Label(self.frame, textvariable=self.v).grid(row=8, column = 1)

        self.e_w0 = tk.Entry(self.frame)
        self.e_s11 = tk.Entry(self.frame)
        self.e_s22 = tk.Entry(self.frame)
        self.e_s33 = tk.Entry(self.frame)
        self.e_jfreq = tk.Entry(self.frame)
        self.e_t2 = tk.Entry(self.frame)
        self.e_hi = tk.Entry(self.frame)
        self.e_lo = tk.Entry(self.frame)

        self.e_w0.grid(row=0, column=1)
        self.e_s11.grid(row=1, column=1)
        self.e_s22.grid(row=2, column=1)
        self.e_s33.grid(row=3, column=1)
        self.e_jfreq.grid(row=4, column=1)
        self.e_t2.grid(row=5, column=1)
        self.e_hi.grid(row=6, column=1)
        self.e_lo.grid(row=7, column=1)

        tk.Button(self.frame, text="BROWSE", command = self.filechoose).grid(row=8)
        tk.Button(self.frame, text="PLOT", command = self.callback).grid(row=9)
        tk.Button(self.frame, text="SAVE", command = self.save).grid(row=9, column = 1)

        #self.frame.title("bcsax")

    def plot(self,w0,s11,s22,s33,jfreq,t2,hi,lo, user_data):
        self.f,self.g = self.bcsax(s11,s22,s33,jfreq,t2,hi,lo, w0)

        gen_data = plt.plot(self.f,self.g,label="Simulation") 

        data = user_data != ""

        if data:
            infile = pd.read_csv(user_data)
            user_data = plt.plot(infile.iloc[:, 0], infile.iloc[:, 1], label="User Data")

        plt.legend(loc='upper right')

        plt.gca().invert_xaxis()
        plt.xlim(lo, hi)
        plt.show()

    @staticmethod
    def bcsax(s11,s22,s33,jfreq,t2,fu,fl,w0):
        smo = 1
        nt = 5000
        f = np.zeros(1000)
        g = np.zeros(1000)
        tint = np.zeros(500000)
        w = np.zeros(500000)

        wfu = fu*w0
        wfl = fl*w0
        nsite = int(round(fu - fl)) * 10
        nf = 1000
        dwf = (wfu - wfl) / float(nf - 1)
        df = (fu - fl) / float(nf - 1)

        for i in range(0, nf):
            f[i] = fl + df * float(i - 1)

        wsig11 = s11 * w0
        wsig22 = s22 * w0
        wsig33 = s33 * w0

        for i in range(0,nsite):
            tint[i] = 0

        for i in range(0,nsite):
            w[i] = 0
        
        sum = 0.0
        dif1 = s33-s11
        dif2 = s33-s22
        dif3 = s22-s11

        m_is = int(round(s11 - fl)) + 1
        m_ib = int(round(s22 - fl)) + 1
        m_it = int(round(s33 - fl)) + 1

        ibm1 = m_ib - 1

        a0=1.3862944
        a1=0.1119723
        b0=0.50
        a2=0.0725296
        b1=0.1213478
        b2=0.0288729

        for k in range(m_is, ibm1):
            pm = np.sqrt(dif1*dif2/((m_it-k)*dif3))
            par = (k-m_is)*dif2/((m_it-k)*dif3)
            v = 1.0 - par
            eint = a0+a1*v+a2*v**2+(b0+b1*v+b2*v**2)*np.log(1.0/v)
            tint[k] = pm*eint
            sum=sum+tint[k]
        
        ibp1 = m_ib + 1
        for k in range(ibp1, m_it):
            pm = np.sqrt(dif1/(k-m_is))
            par=dif3*(m_it-k)/(dif2*(k-m_is))
            v=1.0-par
            eint=a0+a1*v+a2*v**2+(b0+b1*v+b2*v**2)*np.log(1.0/v)
            tint[k]=pm*eint
            sum=sum+tint[k]
        
        isgn = 1

        if (tint[m_ib-1] < tint[m_ib+1]):
            isgn = -1
        
        tint[m_ib] = 6*tint[m_ib-isgn] - 5 * tint[m_ib - isgn * 2]
        sum = sum + tint[m_ib]
        temp1 = 0.0
        temp2 = 0.0

        for i in range(0, smo):
            for k in range(1, nsite - 1):
                temp1 = tint[k]
                tint[k] = (temp2 + 2 * tint[k] + tint[k + 1] + 1e-30)/4.0
                temp2 = temp1
        
        pts = 5000
        dsum = sum / pts
        ipeak = 0

        for i in range(0, nsite):
            wf = fl + float(i - 1)
            n = int(round(tint[i]/dsum))
            for j in range(0, n):
                ipeak = ipeak + 1
                w[ipeak] = wf + ((j - 1) / n)
        
        for k in range(0, ipeak):
            w[k] = w0 * w[k]
        
        jfreq = jfreq / (float(ipeak) - 1.0)
        ar = float(ipeak) * jfreq + (1.0 / t2)

        for j in range(0, nf):
            wf = wfl + dwf * float(j - 1)
            l = complex(0.0, 0.0)
            for k in range(0, ipeak):
                l = l + complex(1.0, 0.0) / complex(ar, wf - w[k])
            
            g[j] = (l/(complex(1.0,0.0)-(complex(jfreq,0.0)*l))).real
            g[j] = g[j] / float(ipeak)
        
        gmax = 0.0
        for i in range(0, nf):
            if g[i] > gmax: gmax = g[i]
        
        for i in range(0, nf):
            ppm = fl + df * float(i - 1)
            g[i] = g[i] / gmax
            f[i] = ppm

        return f,g

    def callback(self):
        self.plot(float(self.e_w0.get()), float(self.e_s11.get()), float(self.e_s22.get()), float(self.e_s33.get()), 
            float(self.e_jfreq.get()), float(self.e_t2.get()), float(self.e_hi.get()), float(self.e_lo.get()), 
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

    BCSax(master)
    master.mainloop()