# Project_NBRA-BL-NA-MD_SiNCs
This repository contains the working files used in the work "Hot Electron Cooling in Silicon Nanoclusters via Landau-Zener Non-Adiabatic Molecular Dynamics: Size Dependence and Role of Surface Termination"

Uncompress with  tar -xvf FILENAME 

step1 - DFTB+ MD

step2 - DFTB+ SCC calculation at each MD step - Here, we extract energies to be used in BL-NBRA-NAMD

step3 - scripts for performing BL-NBRA-NAMD computations

      - need to adjust the paths in the step3 files to the locaiton of step2 res folder

F1  - Fluorine ligand with mass of 1 a.m.u

H1  - Hydrogen ligand with mass of 1 a.m.u

F19 - Fluorine ligand with mass of 19 a.m.u

H19 - Hydrogen ligand with mass of 19 a.m.u

sysprop - scripts for performing FFT analysis (for getting some system properties)

xyz structure files can be found in step1 folders

For step1 - need to adjust thermostat freq for the different systems. The number of lines in velocity.txt needs to match the number of atoms in the system. Need to also look for ??? in thermal.py

