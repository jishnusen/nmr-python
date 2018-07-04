import qmasex
import quadex2

options = """
[1] Two-Site Quadrupolar MAS Exchange - For calculation of lineshape resulting from exchange between two quadrupolar MAS lineshapes
[2] Two-Site Quadrupolar Static Exchange - For calculation of lineshape resulting from exchange between two quadrupolar static lineshapes
"""
choice = int(input(f"Enter the simulation you would like to run. Available options are: {options}\nEnsure that the number matches exactly: "))

if choice == 1:
    qmasex.run()
elif choice == 2:
    quadex.run()
