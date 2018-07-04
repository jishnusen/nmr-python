from oct2py import Oct2Py
import numpy as np
import matplotlib.pyplot as plt

def run():
    print("Running Gaussian Peak Exchange Simulation")
    oc = Oct2Py()

    vlf = float(input("Larmor Frequency (MHz): "))
    pos = np.fromstring(input("Enter peak positions (ppm, comma separated): "), sep=",") 
    inp = np.fromstring(input("Enter intensities (comma separated): "), sep=",")
    flo = float(input("Upper plot limit: "))
    fhi = float(input("Lower plot limit: "))
    t2 = float(input("T2 (seconds): ")) 
    jfreq = float(input("Jump Frequency (Hz): "))

    gauss_mat = f"""
    twopi = 2*pi;
    vlf = {vlf}*twopi;
    pos = {pos};
    pos = pos/{vlf};
    inp = {inp};
    inp = inp';
    w = pos*vlf;
    wk = zeros(length(pos));
    flo = {flo};
    fhi = {fhi};
    flo = flo*vlf;
    fhi = fhi*vlf;
    npts = 1000;
    t2 = {t2}.*{np.ones(pos.size)};
    t2 = -1./t2;
    jfreq = {jfreq};
    pim = ones(length(w),1)*inp'+diag(-(sum(inp)-inp))-diag(inp);
    weight = inp;
    sumw = sum(weight);
    jfreq = jfreq / (sumw - 1.);
    df = (fhi - flo) / (npts - 1);
    u = [1:npts];
    f = flo + df * (u-1);
    n = length(inp);
    g = zeros(1, npts);
    v = [1:n];
    k = [1:n];
    jfreqd = jfreq * diag(pim) + t2';
    pim(v,k);
    omgo = (jfreq + 0*1i)*(pim(v, k) + 0*1i);
    for u = 1:npts
        wk = w - f(u);
        wk = wk';
        omg = omgo-diag(diag(omgo)) + diag([jfreqd + wk*1i]);
        g(u) = real(sum(omg\weight));
    end

    f = f/vlf;
    g = abs(g);
    g = g/max(g);
    f = transpose(f);
    g = transpose(g);
    """
    oc.eval(gauss_mat)

    f = oc.pull('f')
    g = oc.pull('g')
    plt.plot(f,g, label="Simulation")

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
