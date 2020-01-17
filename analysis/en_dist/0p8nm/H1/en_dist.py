#***********************************************************
# * Copyright (C) 2020 Brendan A. Smith, Wei Li, and Alexey V. Akimov
# * This file is distributed under the terms of the
# * GNU General Public License as published by the
# * Free Software Foundation; either version 3 of the
# * License, or (at your option) any later version.
# * http://www.gnu.org/copyleft/gpl.txt
#***********************************************************/

import os
import sys
import time
import math

# Fisrt, we add the location of the library to test to the PYTHON path
if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *
from libra_py import *
import libra_py.workflows.nbra.step4 as step4
import libra_py.workflows.nbra.decoherence_times as decoherence_times
import libra_py.workflows.nbra.lz as lz
from libra_py import influence_spectrum as infsp
import libra_py.workflows.nbra.qsh as qsh




os.system("rm -rf _en_dist")
os.system("mkdir  _en_dist")
params = {}
# Get Hvib from the non-QSH NA-MD run
# Get Hvib from the non-QSH NA-MD run
params["data_set_paths"] = []
params["data_set_paths"].append("/budgetdata/academic/alexeyak/brendan/Si_QD/H_capped/08nm/H1/step2/traj0/res/")
params["Hvib_re_prefix"] = "hvib_"; params["Hvib_re_suffix"] = "_re"
params["Hvib_im_prefix"] = "hvib_"; params["Hvib_im_suffix"] = "_im"
params["nfiles"]         = 5000
params["nstates"]        = 30
params["init_times"]     = [0]
params["active_space"]   = range(30)

times = [5000]
for t in times:

    params["nsteps"] = t
    Hvib = step4.get_Hvib2(params)

    # Compute energy gaps for states i,j in trajectory of length "t"
    dE = decoherence_times.energy_gaps_ave(Hvib, [params["init_times"][0]], params["nsteps"])

    states = range(len(params["active_space"]))
    dens_ij = []
    for i in states:
        for j in states:
            if j > i and j-i == 1:
                print ("i = ", i, "j = ", j)
                data_ij = []
                for de in dE:
                    x = MATRIX(1,1)
                    x.set(0,0, de.get(i,j)/units.ev2Ha)
                    data_ij.append(x)
                bin_supp, dens, cum = data_stat.cmat_distrib(data_ij, 0, 0, 0, 0, 4, 0.01)
                dens_ij.append(dens)
  
    g = open("_en_dist/_en_dist"+str(t)+".txt","w"); g.close()
    for i in range(len(bin_supp)):
        g = open("_en_dist/_en_dist"+str(t)+".txt","a")
        g.write("%0.3f  " % (bin_supp[i]))
        for j in range(len(dens_ij)):
            g.write("%8.5f  " % (dens_ij[j][i]))
        g.write("\n")
        g.close()

