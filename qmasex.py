import fortran_90_ports.qmasexfort as fort
import numpy as np
import matplotlib.pyplot as plt


def run():
    print("Running Two-Site Quadrupolar MAS Exchange Simulation")
    vlf = float(input("Larmor Frequency (MHz): "))
    sqn = float(input("Enter the Spin Quantum Number: "))

    eta1 = float(input("Enter asymmetry parameter for site #1 (MHz): "))
    eqqh1 = float(input("Quadrupolar coupling constant for site #1 (Mhz): "))
    cs1 = float(input("Isotropic chemical shift for site #1 (ppm): "))
    npolar1 = float(input("Enter number of polar angles for site #1: "))
    nazim1 = float(input("Enter number of azimuthal angles for site #1: "))

    eta2 = float(input("Enter asymmetry parameter for site #2 (MHz): "))
    eqqh2 = float(input("Quadrupolar coupling constant for site #2 (Mhz): "))
    cs2 = float(input("Isotropic chemical shift for site #2 (ppm): "))
    npolar2 = float(input("Enter number of polar angles for site #2: "))
    nazim2 = float(input("Enter number of azimuthal angles for site #2: "))

    hi = float(input("Upper plot limit: "))
    lo = float(input("Lower plot limit: "))

    t2one = float(input("Enter T2 for site #1 (seconds): "))
    t2two = float(input("Enter T2 for site #2 (seconds): "))

    jfreq = float(input("Enter the jump frequency (Hz): "))

    f, g = fort.qmasex(sqn, vlf, eta1, eqqh1, cs1, t2one, npolar1, nazim1,
                       eta2, eqqh2, cs2, t2two, npolar2, nazim2, hi, lo, jfreq)
    gen_data = plt.plot(f, g, label="Simulation")

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
