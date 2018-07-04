import fortran_90_ports.q3q4stexfort as fort
import numpy as np
import matplotlib.pyplot as plt


def run():
    print("Running CSA-Gaussian Peak Exchange")
    vlf = float(input("Larmor Frequency (MHz): "))
    avspara = float(input("Delta-Parallel (ppm): "))
    avsperp = float(input("Delta-Perpendicular (ppm): "))
    ncth = float(input("Number of cosine-thetas: "))
    jfreq = float(input("Jump Frequency (Hz): "))
    t2 = float(input("T2 (seconds): "))

    hi = float(input("Upper plot limit: "))
    lo = float(input("Lower plot limit: "))

    posq4 = float(input("Gaussian Peak Position (ppm): "))

    f, g = fort.q3q4stex(vlf, avspara, avsperp, ncth, jfreq, t2, hi, lo, posq4)

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
