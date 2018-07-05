import fortran_90_ports.bcsaxfort as fort
import numpy as np
import matplotlib.pyplot as plt


def run():
    print("Running Non-Axial CSA Averaging Simulation")
    s11 = float(input("Enter sigma11 (ppm): "))
    s22 = float(input("Enter sigma22 (ppm): "))
    s33 = float(input("Enter sigma33 (ppm): "))
    jfreq = float(input("Enter jump frequency (Hz): "))
    t2 = float(input("Enter T2 (seconds): "))
    hi = float(input("Enter upper plot limit: "))
    lo = float(input("Enter lower plot limit: "))
    
    f,g = fort.bcsax(s11,s22,s33,jfreq,t2,hi,lo)

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
