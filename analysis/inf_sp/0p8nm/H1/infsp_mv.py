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




os.system("rm -rf _spectra")
os.system("mkdir  _spectra")
params = {}
# Get Hvib from the non-QSH NA-MD run
# Get Hvib from the non-QSH NA-MD run
params["data_set_paths"] = []
params["data_set_paths"].append("/budgetdata/academic/alexeyak/brendan/Si_QD/H_capped/1nm/step2/traj0/res/")
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

    # For computing influence spectra
    params2 = {}
    params2["dt"]                = 1.0       # MD timestep in fs
    params2["wspan"]             = 16384.0   #  cm^-1
    params2["dw"]                = 1.0       # cm^-1
    params2["do_output"]         = False
    params2["do_center"]         = True
    params2["acf_type"]          = 1
    params2["data_type"]         = 0
    states = range(len(params["active_space"]))
    ACF, W, J2 = [], [], []
    for i in states:
        for j in states:
            if j > i and j-i == 1:
                print ("i = ", i, "j = ", j)
                data_ij = []
                for de in dE:
                    x = MATRIX(1,1)
                    x.set(0,0, de.get(i,j))
                    data_ij.append(x)
                Tij, ACFij, uACFij, Wij, Jij, J2ij = infsp.recipe1(data_ij, params2)
                ACF.append(ACFij)
                W.append(Wij)
                J2.append(J2ij)
    #print (len(ACF))

    g = open("_spectra/_spectra"+str(t)+".txt","w"); g.close()
    for w in range(len(W[0])):
        g = open("_spectra/_spectra"+str(t)+".txt","a")
        g.write("%8.5f  " % (W[0][w]))
        for tr in range(len(J2)):
            g.write("%8.5f  " % (J2[tr][w]))
        g.write("\n")
        g.close()

