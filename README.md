# nmr-python
WebApp to Visualize NMR Spectroscopy Results

- GUI written in `tkinter`
- `matplotlib` used for plotting

See `fortran_90_ports/` for original FORTRAN90 code for these simulaitons.

These fortran codes have been ported to python and optimized for UX. Run: `python3 gui.py`.
Or see releases for a compiled windows exe.

Supports plotting against provided CSV data file. 

## Other utilities included:

`Peak Combiner`: Generate plot for adding two provided CSV data peaks together
`Normalizer`: Normalize provded peak data from specified min/max to [0, 1].
