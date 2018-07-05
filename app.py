import qmasex
import quadex2
import bcsax
import gauss
import q3q4stex

options = """
[1] Two-Site Quadrupolar MAS Exchange - For calculation of lineshape resulting from exchange between two quadrupolar MAS lineshapes
[2] Two-Site Quadrupolar Static Exchange - For calculation of lineshape resulting from exchange between two quadrupolar static lineshapes
[3] Non-Axial CSA Averaging - For calculation of lineshape resulting from random exchange between different orientations under a CSA-controlled lineshape
[4] Gaussian Peak Exchange - For calculation of lineshape resulting from dynamical exchange between multiple Gaussian peaks
[5] CSA-Gaussian Peak Exchange - For calculation of lineshape resulting from exchange between a Gaussian and a CSA-controlled lineshape
"""

while (True):
    choice = int(input(f"Enter the simulation you would like to run. Available options are: {options}\nEnsure that the number matches exactly: "))

    if choice == 1:
        qmasex.run()
    elif choice == 2:
        quadex2.run()
    elif choice == 3:
        bcsax.run()
    elif choice == 4:
        gauss.run()
    elif choice ==5:
        q3q4stex.run()

    print("\n\n")
