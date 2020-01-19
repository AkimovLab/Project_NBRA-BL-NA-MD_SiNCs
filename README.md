# Project_NBRA-BL-NA-MD_SiNCs
This repository contains the working files used in the work "Hot Electron Cooling in Silicon Nanoclusters via Landau-Zener Non-Adiabatic Molecular Dynamics: Size Dependence and Role of Surface Termination"

## Running NA-MD

1. Step1 - DFTB+ MD. 
    1. The initial .xyz files for each structure considered herein is given in this folder. I recommend making a separate folder for each structure present (each .xyz file). Then, copy the files "convert.py", "dftb_in.hsd", "submit.sh", "submit.slm", "thermal.py", "velocity.txt", as well as the specific "SYSTEM.xyz" files into their respective folders. 
    2. Go into "convert.py" and make sure to change the ".xyz" string to the correct file name. This script converts the .xyz file into a .gen file to be read by DFTB+. 
    3. Go into the velocity.txt file to make sure that the number of rows of 0's (three columns per row) is equal to the number of atoms in the respective system. By doing this, we are basically setting the initial velocities for all atoms in all dimensions equal to 0. This is the start of our thermal sampling trajectory. 
    4. Run the program by running “sh submit.sh”. This will create folder called “traj0”, which is the 0th trajectory in your thermal MD. Now, all of the relevant files should be copied into the “traj0” directory. Now, go into the folder “traj0”. 
    5. After the thermalization trajectory is complete (5 ps MD in this case). Go into the file “thermal.py” and set the value of natoms to the number of atoms in your respective case (ex. natoms = 62 atoms, for the smallest NC). 
    6. Select the number of production MD trajectories (which I call sub trajectories in the script) you wish run (ex. nsub = 10 ). Please note in the file “thermal.py” the line with “range(4000,5000)”. This tells the code to sample “nsub” random points between 4000 and 5000, as starting times for the production MD. The script “thermal.py” will then take these randomly selected times and make new a new folder with the DFTB+ input files (positions and velocities!) according to that time stamp. 
    7. Run the thermal.py via “python thermal.py”. To adjust the length of the production Md trajectories. Adjust the number of steps in the “dftb_in.hsd” file within the thermalization “traj0” folder  

2. Step2 - DFTB+ SCC calculation at each MD step - Due to size constraints, many of the files herein are compressed. One can uncompressed the files with "tar -xvf FILENAME". These instructions also serve as notes. 
    1. Inside each compressed file one will find a res directory with the results from running the step2 calculations. Additionally, one will find copies of the files that are currently uncompressed, such as “check.py”, “dftb_in.hsd”, “submit.py”, “submit.slm”, “get_properties.py”. Inside the compressed files, these scripts will be tailored to the respective system. 
    2. One can run step2 by running “python submit.py”. Inside ”submit.py”, one can set the number of sub-trajectories  to consider from step1, as well as assign the umber of workers and jobs per worker to perform the step2 computations. The script “check.py” checks to see the progress of the step2 calculation (ex. how many steps have been completed). 
    3. The script “get_properties.py” reads the energies from the “res” folder and outputs a file “en.txt”, which is used to plot the states’ energies vs. time. 

3. Step3/4 (NAMD folder) - scripts for performing BL-NBRA-NAMD computations. Also need to adjust the paths in the step3 files to the locaiton of step2 res folder 
    1. The driver script is "run_step4.py". Some people may be used to the typical NBRA workflow having only 3 steps. Past internal developments have lead to a 4th step being added (the NA-MD step was moved to step4). Step3 was made into a step that post-procresses the Hamiltonian. So here, we skip step3 and go right to step4, but it is labeled as step3 herein for ease. 

## Normal Modes calculations

1. Normal_modes - This is divided into 3 sections. For each system considered in the normal modes analysis:
    1. geom_opt - this folder contains scripts to perform geometry optimization using the SCC-DFTB method via the DFTB+ software.
    2. hessian  - the hessian is computed here. Also uses the SCC-DFTB method
    3. normal_modes - this folder contains scripts to compute the normal modes using the modes program within DFTB+

## Charge density
1. Uses the waveplot program within the DFTB+ software to compute charge densities

## Analysis
1. Scripts for computing energy gap distribution functions and the influence specta
    1. en_dist - folder containing scripts for computing energy gap distribution functions  
    2. inf_sp  - folder containing scripts for computing influence spectra

## POTENTIALLY USEFUL INFORMATION ##

F1  - Fluorine ligand with mass of 1 a.m.u

H1  - Hydrogen ligand with mass of 1 a.m.u

F19 - Fluorine ligand with mass of 19 a.m.u

H19 - Hydrogen ligand with mass of 19 a.m.u

Fcap - F-termination
Hcap - H-termination

xyz structure files can be found in step1 folders


