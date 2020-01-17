import os
import sys

# Fisrt, we add the location of the library to test to the PYTHON path
if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *
import util.libutil as comn
from libra_py import DFTB_methods
from libra_py import units
from libra_py.workflows.nbra import step2_dftb

# For DFTB+
# 140 electrons = 26 Silicon (4*26=104) + 36 Hydrogen (1*36=36)
# HOMO = 70, when index from 0, HOMO = 69
params = {"EXE":"/projects/academic/alexeyak/Software/dftb/dftbplus-18.2.x86_64-linux/bin/dftb+",
          "dt": 1.0 * units.fs2au ,
          "isnap":? ,
          "fsnap":? ,
          "out_dir":? ,
          "md_file":? ,
          "mo_active_space":range(69,99),
         }
#step2_dftb.run_step2(params)
step2_dftb.run_step2_lz(params)

