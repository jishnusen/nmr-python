import matplotlib.pyplot as plt
import numpy as np

def plot(vlf, pos, inp, lo, hi, t2, jfreq, user_data):
    global f,g
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

    gen_data = plt.plot(f,g,label="Simulation") 

    if user_data != "":
        infile = np.loadtxt((user_data), delimiter=",")
        user_data = plt.plot(infile[:, 0], infile[:, 1], label="User Data")

    plt.legend(loc='upper right')

    plt.gca().invert_xaxis()
    plt.show()


import tkinter as tk
from tkinter import filedialog



master = tk.Tk()

tk.Label(master, text="larmor frequency (MHz)").grid(row=0)
tk.Label(master, text="peak pos (csv, ppm)").grid(row=1)
tk.Label(master, text="intensities (csv, rel)").grid(row=2)
tk.Label(master, text="lower plot limit (ppm)").grid(row=3)
tk.Label(master, text="upper plot limit (ppm)").grid(row=4)
tk.Label(master, text="T2 (seconds)").grid(row=5)
tk.Label(master, text="jump frequency (Hz)").grid(row=6)
v = tk.StringVar()
user_data = ""
tk.Label(master, textvariable=v).grid(row=7, column = 1)

def callback():
    global user_data
    plot(float(e_vlf.get()), np.fromstring(e_pos.get(), sep=","), np.fromstring(e_inp.get(), sep=","), float(e_lo.get()), 
        float(e_hi.get()), float(e_t2.get()), float(e_jfreq.get()), user_data)

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

e_vlf = tk.Entry(master)
e_pos = tk.Entry(master)
e_inp = tk.Entry(master)
e_lo = tk.Entry(master)
e_hi = tk.Entry(master)
e_t2 = tk.Entry(master)
e_jfreq = tk.Entry(master)

e_vlf.grid(row=0, column=1)
e_pos.grid(row=1, column=1)
e_inp.grid(row=2, column=1)
e_lo.grid(row=3, column=1)
e_hi.grid(row=4, column=1)
e_t2.grid(row=5, column=1)
e_jfreq.grid(row=6, column=1)

tk.Button(master, text="BROWSE", command = filechoose).grid(row=7)
tk.Button(master, text="PLOT", command = callback).grid(row=8)
tk.Button(master, text="SAVE", command = save).grid(row=8, column = 1)

def main():
    global master
    master.title("gauss")
    master.mainloop()

if __name__ == "__main__":
    main()

