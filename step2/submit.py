import os
import sys
import math
import re

if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *
from libra_py import hpc_utils

# of trajectories from step1
ntraj = [1,2,3,4,5,6,7,8,9]

iworker = 0            # initial worker
fworker = 20           # final worker
steps_per_worker = 250 # how many steps each worker handles

for traj in ntraj:

    # Make sub-directory for step2 for sub-trajectory
    os.system("mkdir traj%i" % (traj) )
    os.system("mkdir traj%i/res" % (traj) )
    
    step1 = "/budgetdata/academic/alexeyak/brendan/Si_QD/H_capped/1nm/step1/traj0/"
    step2 = os.getcwd()   # step2 dir

    for worker in range(iworker, fworker):
    
        # Make a worker directory
        os.system("mkdir traj%i/worker%i" % (traj, worker) )

        # Copy the trajectory file into each worker dir
        os.system("cp %s/traj%i/md.xyz traj%i/worker%i" % (step1, traj, traj, worker) )

        # Setup the parameters for given worker and trajectory
        params = { "\"out_dir\":\?" : "\"out_dir\":\"%s/traj%i/res\"" % (step2, traj),
                   "\"md_file\":\?" : "\"md_file\":\"%s/traj%i/worker%i/md.xyz\"" % (step2, traj, worker),
                   "\"isnap\":\?" : "\"isnap\":%i" % (worker * steps_per_worker),
                   "\"fsnap\":\?" : "\"fsnap\":%i" % ((worker+1) * steps_per_worker + 1)
                 }
        hpc_utils.substitute("run.py", "traj%i/worker%i/run.py" % (traj, worker), params )

        # Copy the submit file into each worker dir
        os.system("cp submit.slm traj%i/worker%i" % (traj, worker) )

        # Copy the dftb_input files into each worker dir
        os.system("cp dftb_in_ham1.hsd traj%i/worker%i" % (traj, worker) )
        os.system("cp dftb_in_ham2.hsd traj%i/worker%i" % (traj, worker) )
        os.system("cp dftb_in_overlaps.hsd traj%i/worker%i" % (traj, worker) )

        # Go into each worker and submit the calculations from it
        os.chdir("traj%i/worker%i" % (traj, worker) )
        #os.system("python run.py")
        os.system("sbatch submit.slm")
        os.chdir("../../")

