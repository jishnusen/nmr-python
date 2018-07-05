#!/bin/bash
cd "$(dirname "$0")"

f2py3 -c qmasex.f90 -m qmasexfort
f2py3 -c quadex2.f90 -m quadexfort
f2py3 -c bcsax.f90 -m bcsaxfort
f2py3 -c q3q4stex.f90 -m q3q4stexfort

