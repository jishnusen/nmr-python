import bcsax
import tkinter as tk
import gauss
import peak_combiner
import normalizer
import q3q4stex


root = tk.Tk()
root.minsize(300, 3)
tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.rowconfigure(root, 1, weight=1)
tk.Grid.rowconfigure(root, 2, weight=1)
tk.Grid.rowconfigure(root, 3, weight=1)
tk.Grid.rowconfigure(root, 4, weight=1)
tk.Grid.columnconfigure(root, 0, weight=1)

def toplevel():
    global root
    toplevel = tk.Toplevel(root)
    x = root.winfo_x()
    y = root.winfo_y()
    h = root.winfo_height()
    toplevel.geometry("+%d+%d" % (x + 310, y - h))
    return toplevel

def create_bcsax():
    bcsax.BCSax(toplevel())

def create_gauss():
    gauss.Gauss(toplevel())
    
def create_q3q4():
    q3q4stex.Q3Q4(toplevel())
    
def create_peak():
    peak_combiner.PeakCombiner(toplevel())

def create_norm():
    normalizer.Normalizer(toplevel())

bcsax_button = tk.Button(root, text="BCSAX", command = create_bcsax).grid(row=0, sticky=tk.N+tk.S+tk.E+tk.W)
gauss_button = tk.Button(root, text="GAUSS", command = create_gauss).grid(row=1, sticky=tk.N+tk.S+tk.E+tk.W)
gauss_button = tk.Button(root, text="Q3Q4", command = create_q3q4).grid(row=2, sticky=tk.N+tk.S+tk.E+tk.W)
peak_button = tk.Button(root, text="PEAK COMBINER", command = create_peak).grid(row=3, sticky=tk.N+tk.S+tk.E+tk.W)
norm_button = tk.Button(root, text="NORMALIZER", command = create_norm).grid(row=4, sticky=tk.N+tk.S+tk.E+tk.W)

root.mainloop()
