from liblibra_core import *
from libra_py import *

from libra_py.workflows.nbra import*

import sys
import math

def track_energy(ntraj, norbitals, orb_list, file_prefix, file_suffix):
    """ 
    tracks the energy of orbtials/states versus time
    """

    norbs = len(orb_list)

    #g = open("_en.txt","w")
    #g.close

    en = MATRIXList()
    for i in range(ntraj):
        f  = open( file_prefix + str(i) + file_suffix)
        A  = f.readlines()
        sz = len(A)
        f.close()

        en.append( MATRIX(norbs,1) )
        for j in range(norbs):

            b = A[orb_list[j]].strip().split()
            en[i].set(j,0, float( b[ orb_list[j] ] ) / units.ev2Ha )      

        #g = open("_en.txt","a")
        #g.write("%0.10f " % ( i*(units.fs2au) ) )
        #for j in range(norbs):
        #    g.write("%0.10f " % ( en[i].get(j,0) ) )
        #g.write( "\n" % () )
        #g.close()

    return en


def track_error(ntraj, norbitals, orb_list, file_prefix, file_suffix):
    """
    computes the error 
    """

    norbs = len(orb_list) - 1

    g = open("_err.txt","w")
    g.close

    nac = MATRIXList()
    for i in range(ntraj):

        f  = open( file_prefix + str(i) + file_suffix)
        A  = f.readlines()
        sz = len(A)
        f.close()

        # For each step, we get the nacs for adjacent states
        # ex) < orb_list(i) | orb_list(i+1) >
        nac.append( MATRIX(norbs,1) )
        for j in range(norbs):

            b = A[orb_list[j]].strip().split()   
            nac[i].set(j,0, abs( float( b[ orb_list[j]+1 ]  ) / units.ev2Ha ) )

    avg, dev, upper, lower = common_utils.mat_stat(nac)

    # for printing 
    g = open("_err.txt","a")
    for j in range(norbs):
        g.write("%0.10f %0.10f %0.10f \n" % ( orb_list[j], avg.get(j,0), dev.get(j,0) ) )
    g.write( "\n" % () )
    g.close()




def main(ntraj, norbitals, orb_list, En_prefix):
  return track_energy(ntraj, norbitals, orb_list, En_prefix, "_re")



# Define number of sub-trajectories  
trajs  = [0]
ntrajs = len(trajs)

# Define number of steps 
nsteps = 5000

# Define number of dynamical states
nstates = range(30)

# Make energy list
En = []
for traj in trajs:

    # Go into sub-directory folder
    res_dir = "traj"+str(traj)+"/res"
    # For each timestep, get energy of each state. _En is a list of MATRICES
    _En = main(nsteps, len(nstates), nstates, res_dir+"/hvib_")
    # Appens the list _En to En
    En.append( _En )

### Average the energy of each trajectory at each step number

avg = []
# For each step
for t in range(nsteps):

    _avg = MATRIX(len(nstates),1)

    #For each trajectory, get energy step number t
    for traj in trajs:
        _avg += En[traj][t]
    _avg /= ntrajs
    # _avg is the MATRIX that contains the trajectory averaged energies for step 1
    avg.append(_avg)

# Write the data to _en.txt
g = open("_en.txt","w"); g.close
for t in range(nsteps):

    g = open("_en.txt","a")
    g.write("%0.10f " % ( t*(units.fs2au) ) )
 
    for j in range(len(nstates)):
        g.write("%0.10f " % ( avg[t].get(j,0) ) )
    g.write( "\n" % () )
    g.close()


"""
print "printing average energies over all sub-trajectories"
avg1, dev1, upper1, lower1 = data_stat.mat_stat(avg)
avg1.show_matrix()
dev1.show_matrix()

### Let's average the tNACS over all sub-trajectories
tNAC = []
for traj in trajs:

    g = open("_tnac"+str(traj)+".txt")    
    A = g.readlines()
    sz = len(A)
    g.close()

    tNAC.append( MATRIX(nstates,nstates) )

    for l in range(sz):
        b = A[l].strip().split()
        if not b:
            continue
        else:
            tNAC[traj].set(int(b[0]),int(b[1]),float(b[2]))

    
avg2, dev2, upper2, lower2 = data_stat.mat_stat(tNAC)
avg2.show_matrix()
"""
