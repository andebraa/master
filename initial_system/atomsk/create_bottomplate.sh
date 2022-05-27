#!/bin/bash
#lx_tot = 200
#ly_tot = 200
#lz_tot = 20

#let "lx = $lx_tot/2"
#let "ly = $ly_tot/2"
#let "lz = $lz_tot/2"

atomsk --create diamond 4.3596 Si C -spacegroup 216 -orient [100] [010] [001] [10-1] [010] [101] -duplicate 200 200 20 sto_orig.xsf
atomsk sto_orig.xsf -cut above 20 z sto_cut1.xsf
atomsk sto_cut1.xsf -cut below -20 z sto_cut2.xsf
atomsk sto_cut2.xsf -cut above 100 x sto_cut3.xsf
atomsk sto_cut3.xsf -cut below -100 x sto_cut4.xsf
atomsk sto_cut4.xsf -cut above 100 y sto_cut5.xsf
atomsk sto_cut5.xsf -cut below -100 y sto_cut6.xsf
