#!/bin/bash
#lx_tot = 200
#ly_tot = 200
#lz_tot = 20

#let "lx = $lx_tot/2"
#let "ly = $ly_tot/2"
#let "lz = $lz_tot/2"

atomsk --create diamond 4.3596 Si C -spacegroup 216 -orient [100] [010] [001] [10-1] [010] [101] -duplicate 100 0 100 testrun.xsf
#100x100: origo in bottom corner. height 613, xmin xmax +/-305. midpoint z at 305 
atomsk testrun.xsf -cut above 315 z xsf
atomsk testrun.xsf -cut below 295 z xsf
atomsk testrun.xsf -cut above 201 x xsf
atomsk testrun.xsf -cut below -200 x xsf

atomsk testrun.xsf -duplicate 0 92 0 xsf

atomsk testrun.xsf -shift 200 0 0 testrun_shifted.xsf
atomsk testrun_shifted.xsf -shift 0 0 -296


# PRIMVEC
#     401.0832000        0.00000000        0.00000000
#      0.00000000      401.08320000        0.00000000
#      0.00000000        0.00000000       18.47027233
