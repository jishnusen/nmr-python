import numpy as np
import matplotlib.pyplot as plt


class Q3Q4:
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

        plt.plot(f,g)
        plt.show()

Q3Q4.q3q4stex(100., 100., -100., 1000, 1., 0.001, 200., -200., 0.)