import matplotlib.pyplot as plt
import numpy as np

def run(vlf, pos, inp, lo, hi, t2, jfreq):
    # print("Running Gaussian Peak Exchange Simulation")
    # vlf = float(input("Larmor Frequency (MHz): "))
    pos = np.fromstring(pos, sep=",") 
    inp = np.fromstring(inp, sep=",")
    # lo = float(input("Upper plot limit: "))
    # hi = float(input("Lower plot limit: "))
    # t2 = float(input("T2 (seconds): ")) 
    # jfreq = float(input("Jump Frequency (Hz): "))

    pos = pos / vlf
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
    
    return f,g

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
