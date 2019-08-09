import numpy as np
import matplotlib.pyplot as plt
import fortran_90_ports.bcsaxfort as fort
import pandas as pd


def run():
    print("Running Non-Axial CSA Averaging Simulation")
    w0 = float(input("Enter larmor frequency (MHz): "))
    s11 = float(input("Enter sigma11 (ppm): "))
    s22 = float(input("Enter sigma22 (ppm): "))
    s33 = float(input("Enter sigma33 (ppm): "))
    jfreq = float(input("Enter jump frequency (Hz): "))
    t2 = float(input("Enter T2 (seconds): "))
    hi = float(input("Enter upper plot limit: "))
    lo = float(input("Enter lower plot limit: "))
    
    f,g = fort.bcsax(s11,s22,s33,jfreq,t2,hi,lo,w0)

    gen_data = plt.plot(f,g,label="Simulation") 

    data = True if input("Plot against own data (y/n): ") == "y" else False

    if data:
        infile = np.loadtxt(input("Filename: "), delimiter=",")
        user_data = plt.plot(infile[:, 0], infile[:, 1], label="User Data")

    plt.legend(loc='upper right')

    plt.gca().invert_xaxis()
    plt.show()

    save = True if input("Save (y/n): ") == "y" else False

    if save:
        out = open(input("Filename: "), "w")
        csv = ""
        for i in range(0, g.size):
            csv += f"{float(f[i])},{float(g[i])}\n"
        out.write(csv)

def plot(w0,s11,s22,s33,jfreq,t2,hi,lo, user_data):
    global f,g
    f,g = bcsax(s11,s22,s33,jfreq,t2,hi,lo, w0)

    gen_data = plt.plot(f,g,label="Simulation") 

    data = user_data != ""

    if data:
        infile = pd.read_csv(user_data)
        user_data = plt.plot(infile.iloc[:, 0], infile.iloc[:, 1], label="User Data")

    plt.legend(loc='upper right')

    plt.gca().invert_xaxis()
    plt.xlim(lo, hi)
    plt.show()

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


import tkinter as tk
from tkinter import filedialog



master = tk.Tk()

tk.Label(master, text="larmor frequency (MHz)").grid(row=0)
tk.Label(master, text="sigma11 (ppm)").grid(row=1)
tk.Label(master, text="sigma22 (ppm)").grid(row=2)
tk.Label(master, text="sigma33 (ppm)").grid(row=3)
tk.Label(master, text="jump frequency (Hz)").grid(row=4)
tk.Label(master, text="T2 (seconds)").grid(row=5)
tk.Label(master, text="upper plot limit (ppm)").grid(row=6)
tk.Label(master, text="lower plot limit (ppm)").grid(row=7)
v = tk.StringVar()
user_data = ""
tk.Label(master, textvariable=v).grid(row=8, column = 1)

def callback():
    global user_data
    plot(float(e_w0.get()), float(e_s11.get()), float(e_s22.get()), float(e_s33.get()), 
        float(e_jfreq.get()), float(e_t2.get()), float(e_hi.get()), float(e_lo.get()), 
        user_data)

def filechoose():
    global user_data
    user_data = filedialog.askopenfilename()
    v.set(user_data.rsplit('/', 1)[-1])

def save():
    global f,g
    csv = ""
    out = filedialog.asksaveasfile(mode='w')
    for i in range(0, g.size):
        csv += f"{float(f[i])},{float(g[i])}\n"
    out.write(csv)
    out.close()

e_w0 = tk.Entry(master)
e_s11 = tk.Entry(master)
e_s22 = tk.Entry(master)
e_s33 = tk.Entry(master)
e_jfreq = tk.Entry(master)
e_t2 = tk.Entry(master)
e_hi = tk.Entry(master)
e_lo = tk.Entry(master)

e_w0.grid(row=0, column=1)
e_s11.grid(row=1, column=1)
e_s22.grid(row=2, column=1)
e_s33.grid(row=3, column=1)
e_jfreq.grid(row=4, column=1)
e_t2.grid(row=5, column=1)
e_hi.grid(row=6, column=1)
e_lo.grid(row=7, column=1)

tk.Button(master, text="BROWSE", command = filechoose).grid(row=8)
tk.Button(master, text="PLOT", command = callback).grid(row=9)
tk.Button(master, text="SAVE", command = save).grid(row=9, column = 1)

def main():
    global master
    master.title("bcsax")
    master.mainloop()

if __name__ == "__main__":
    main()