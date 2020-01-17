#***********************************************************
# * Copyright (C) 2017-2018 Brendan A. Smith, Wei Li, and Alexey V. Akimov
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
import libra_py.workflows.nbra.lz as lz

from libra_py import units
import libra_py.workflows.nbra.step4 as step4
import libra_py.workflows.nbra.lz as lz
import libra_py.workflows.nbra.decoherence_times as decoherence_times
from libra_py import data_conv
from libra_py import fit
from libra_py import influence_spectrum as infsp

params = {}

#excess_eV = 1
#excess_eV = 2
excess_eV = 3

#case = 1   # 0.8 nm Si NC - H 1  a.m.u capped
case = 2   # 0.8 nm Si NC - H 19 a.m.u capped
#case = 3   # 0.8 nm Si NC - F 1  a.m.u capped
#case = 4   # 0.8 nm Si NC - F 19 a.m.u capped

if case == 1:
    trajs = range(10)
    params["data_set_paths"] = []
    for itraj in trajs:
        params["data_set_paths"].append( "/budgetdata/academic/alexeyak/brendan/Si_QD/H_capped/08nm/step2_H1/traj"+str(itraj)+"/res/" )
    if excess_eV == 1:
        params["istate"] = 5
    if excess_eV == 2:
        params["istate"] = 14
    if excess_eV == 3:
        params["istate"] = 24

if case == 2:
    trajs = range(10)
    params["data_set_paths"] = []
    for itraj in trajs:
        params["data_set_paths"].append( "/budgetdata/academic/alexeyak/brendan/Si_QD/H_capped/08nm/step2_H19/traj"+str(itraj)+"/res/" )
    if excess_eV == 1:
        params["istate"] = 6
    if excess_eV == 2:
        params["istate"] = 17
    if excess_eV == 3:
        params["istate"] = 28

if case == 3:
    trajs = range(10)
    params["data_set_paths"] = []
    for itraj in trajs:
        params["data_set_paths"].append( "/budgetdata/academic/alexeyak/brendan/Si_QD/F_capped/08nm/step2_F1/traj"+str(itraj)+"/res/" )
    if excess_eV == 1:
        params["istate"] = 5
    if excess_eV == 2:
        params["istate"] = 11
    if excess_eV == 3:
        params["istate"] = 18

if case == 4:
    trajs = range(10)
    params["data_set_paths"] = []
    for itraj in trajs:
        params["data_set_paths"].append( "/budgetdata/academic/alexeyak/brendan/Si_QD/F_capped/08nm/step2_F19/traj"+str(itraj)+"/res/" )
    if excess_eV == 1:
        params["istate"] = 6
    if excess_eV == 2:
        params["istate"] = 12
    if excess_eV == 3:
        params["istate"] = 19


params["nstates"] = 30
params["nfiles"]  = 4000  # Ex) # of Hvib files to read for a given traj
params["Hvib_re_prefix"] = "hvib_"; params["Hvib_re_suffix"] = "_re"
params["Hvib_im_prefix"] = "hvib_"; params["Hvib_im_suffix"] = "_im"

# General simulaiton parameters
params["T"]                  = 300.0                 # Temperature, K
params["dt"]                 = 1.0*units.fs2au       # Nuclear dynamics integration timestep, in a.u.
params["nsteps"]             = params["nfiles"]      # The length of the NA-MD trajectory
params["init_times"]         = [0]                   # starting points for sub-trajectories
params["do_output"]          = True                  # request to print the results into a file
params["do_return"]          = False                 # request to not store the date in the operating memory

# For running NA-MD
start = time.time()
Hvib = step4.get_Hvib2(params)      # get the Hvib for all data sets, Hvib is a lists of lists
init_time = params["init_times"][0]
end = time.time()
print("Time to read / assemble data = ", end - start)

# Compute average decoherence time over entire trajectory
tau, rates = decoherence_times.decoherence_times_ave(Hvib, [init_time], params["nfiles"]-init_time, 0)
avg_deco = tau/units.fs2au
avg_deco.show_matrix()

"""
#====================== One case =====================
# Looking on the "SH" populations - NBRA-TSH approach
params["gap_min_exception"]  = 0
params["Boltz_opt"]          = 1                     # Option for the frustrated hops acceptance/rejection
params["Boltz_opt_BL"]       = 0                     # Option to incorporate hte frustrated hops into BL probabilities
params["outfile"]            = "_out_TSH_.txt"       # output file
params["evolve_Markov"]      = False                 # don't propagate Markov
params["evolve_TSH"]         = True                  # Rely on propagating trajectories
params["ntraj"]              = 100                   # how many stochastic trajectories
start = time.time()
res = lz.run(Hvib, params)
end = time.time()
print("Time to run TSH = ", end - start)
"""

#====================== Another case =====================
# Looking on the "SE" populations - Markov chain approach
params["target_space"]       = 1
params["gap_min_exception"]  = 0
params["Boltz_opt"]          = 0                     # Option for the frustrated hops acceptance/rejection
params["Boltz_opt_BL"]       = 1                     # Option to incorporate hte frustrated hops into BL probabilities
params["outfile"]            = "_out_Markov_.txt"    # output file
params["evolve_Markov"]      = True                  # Rely on the Markov approach
params["evolve_TSH"]         = False                 # don't care about TSH
params["ntraj"]              = 1                     # how many stochastic trajectories
start = time.time()
res = lz.run(Hvib, params)
end = time.time()
print("Time to run Markov = ", end - start)

