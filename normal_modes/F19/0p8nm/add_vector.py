import sys
import os

def get_modes_dftb():
    """
    Get the normal modes from a dftb computation
    Returns:
        modes - a lsit of lists of lists
        modes[specific_mode][atom#][Vx, Vy, Vz]
    """
    tmp = open(params["modes_file"])
    A   = tmp.readlines()
    sz  = len(A)
    tmp.close()
    # modes is a list of lists of lists
    # list of modes - each mode is a list of vectors
    modes = []

    nmodes = len(params["modes"])
    natoms = params["natoms"]

    # go to the mode of intrest
    for i in range(nmodes):

        modes.append([])
        # now we need to get the vectors
        count  = 0
        for j in range(natoms):

            b = A[ natoms*(params["modes"][i]-1) + 2*params["modes"][i] + j ].strip().split()
            if not b:
                continue
            modes[i].append([0,0,0])
            modes[i][count][0] = float(b[5])    
            modes[i][count][1] = float(b[6])    
            modes[i][count][2] = float(b[7])    
            count += 1

    return modes


def get_modes(params): 
    """
    Wrapper function - gets the modes from some output file of a normal modes computation
    """
    if params["out_type"] == "dftb":
        modes = get_modes_dftb()
    return modes




def add_vectors_vesta(modes, params):
    """
    This function takes the information in "modes" and writes it to a file to be visualized
    """

    tmp = open("test.vesta")
    A   = tmp.readlines()
    sz  = len(A)
    tmp.close()

    scl = params["scl"]
    rad = params["rad"]
    re, gr, bl = params["r"], params["g"], params["b"]
    

    # For each mode we want to visualize, we need to make a new .vesta file
    nmodes = len(params["modes"])
    for i in range(nmodes):

        tmp2 = open("mode"+str(params["modes"][i])+".vesta","w"); tmp2.close()
        for j in range(sz):

            b = A[j].strip().split()
            if not b:
                continue

            tmp2 = open("mode"+str(params["modes"][i])+".vesta","a")
            if b[0] == "VECTR":
                tmp2.write(A[j])
                for k in range(params["natoms"]):
                    tmp2.write("   %i    %0.5f    %0.5f    %0.5f %i\n" % (k+1,scl*modes[i][k][0],scl*modes[i][k][1],scl*modes[i][k][2],0))
                    tmp2.write("    %i   %i    %i    %i    %i\n" % (k+1,0,0,0,0))
                    tmp2.write(" %i %i %i %i %i\n" % (0,0,0,0,0))

            elif b[0] == "VECTT":
                tmp2.write(A[j])
                for k in range(params["natoms"]):
                    tmp2.write("   %i  %f %i    %i    %i %i\n" % (k+1,rad,re,gr,bl,2))
      
            else:
                tmp2.write(A[j]) 
            tmp2.close()




def add_vectors(modes, params):
    """
    Wrapper function - takes "modes" and writes it to a file to be visualized
    This function takes the information in "modes" and writes it to a file to be visualized
    """
    if params["vis_type"] == "vesta":
        add_vectors_vesta(modes, params)



# Need to read the modes from modes.xyz. Each mode has Natoms worth of vectors.
params = {"natoms":62, "modes":[186], "modes_file":"modes.xyz", "out_type":"dftb", "vis_type":"vesta"}
params.update( {"rad":0.3, "scl":5.0, "r":0, "g":255, "b":0} )
modes  = get_modes(params)
add_vectors(modes, params)
  