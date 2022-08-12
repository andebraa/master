import subprocess
import os
import shutil 

L = 410
N = 24

input_script_template = f"box {L} {L} {L}\nrandom {N}"
output_filename = f"hydrate_polycrystal_L{L}"
atomsk_command = f"atomsk --polycrystal s1_unit_cell_mw.data polycrystal.txt -ow -wrap -remove-doubles 2.0 {output_filename}.cfg"

with open("atomsk_tmp/polycrystal.txt", "w") as ofile:
    ofile.write(input_script_template)

shutil.makedirs("atomsk_tmp", exist_ok=True)
os.chdir("atomsk_tmp")
#subprocess.run(atomsk_command.split(" "), capture_output=True)
os.chdir("..")

from ovito.io import *
from ovito.modifiers import *
from ovito.pipeline import *

pipeline = import_file("atomsk_tmp/"+output_filename+".cfg")

# Compute property:
mod = ComputePropertyModifier()
#print(mod.expressions)
mod.expressions = ('grainID')
mod.output_property = 'Molecule Identifier'
pipeline.modifiers.append(mod)

output = pipeline.compute()

export_file(pipeline, output_filename+".data", format="lammps/data", atom_style="molecular")
