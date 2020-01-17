import sys
import os
import numpy as np
from scipy.optimize import curve_fit
from libra_py import *


# 1) Define the fitting function(s).
def func1(t, tau, E0):
    return E0*np.exp(-t/tau)
def func2(t, a1, b1, b2, E0):
    return a1*np.exp(-t/b1) + (E0-a1)*np.exp(-t/b2)
def func3(t, tau, beta, E0):
    return E0*np.exp( -(t/tau)**beta )
def func4(t, tau, B, E0):
    return E0*np.exp(-t/tau) + B
def func5(t, tau, beta, B, E0):
    return E0*np.exp( -(t/tau)**beta ) + B

atoms    = ["H1","F19"]
sizes    = ["2_2"]
energies = [1,2,3]

for atom in atoms:
    for size in sizes:
        for energy in energies: 

            # 2) Get the data to be fit.
            filename = atom+"/"+str(energy)+"eV/"+"_out_Markov_.txt" 
            outname  = "_data_"+atom+"_"+str(size)+"nm_"+str(energy)+"eV.txt"

            print ("\n",filename,"\n")

            f = open(filename)
            A = f.readlines()
            sz = len(A)
            f.close()
            xdata, ydata, nydata = [], [], []
            count = 0
            for i in range(sz):
                b = A[i].strip().split()
                # Compute excess energy above LUMO ( b[4] ) 

                if   size == "0_8":
                    excess = (float(b[91])-float(b[4]))/units.ev2Ha
                elif size == "1_5":
                    excess = (float(b[301])-float(b[4]))/units.ev2Ha
                elif size == "2_2":
                    excess = (float(b[901])-float(b[4]))/units.ev2Ha

                thresh = 0.0
                #print ("excess energy above LUMO   = ", excess/units.ev2Ha)
                #print ("energy of the state LUM0+1 = ", (float(b[7])-float(b[4]))/units.ev2Ha)
                if i < 4001:
                    if excess > thresh:
                        #print(excess-thresh)
                        xdata.append(i+1)
                        ydata.append(excess-thresh)

            # 3) Fit for the paramters in the fitting function defined in 1).
            #popt, pcov = curve_fit(func2, xdata, ydata)

            # 4) OPTIONAL: Constrain the optimization to a region: N <= a <= Z, M <= b <= Y and L <= c <= Z.
            # via bounds=(0, [X, Y, Z])
            #popt, pcov = curve_fit(func1, xdata, ydata, bounds=([-np.inf, ydata[0]-0.05], [np.inf, ydata[0]+0.05]))
            #popt, pcov = curve_fit(func2, xdata, ydata, bounds=([-np.inf, -np.inf, -np.inf, ydata[0]-0.05], [np.inf, np.inf, np.inf, ydata[0]+0.05]))
            #popt, pcov = curve_fit(func3, xdata, ydata, bounds=([-np.inf, 0, ydata[0]-0.05], [np.inf, np.inf, ydata[0]+0.05]))
            #popt, pcov = curve_fit(func4, xdata, ydata, bounds=([-np.inf, 0, ydata[0]-0.05], [np.inf, 1, ydata[0]+0.05]))
            popt, pcov = curve_fit(func5, xdata, ydata, bounds=([-np.inf, 0.4, 0.0, ydata[0]-0.05], [np.inf, np.inf, 1.0, ydata[0]+0.05]))

            # 5 Compute decay lifetimes: 
            """
            # For func1
            tau1, E0 = popt
            print ("Printing optimal fitting paramters:")
            print ("tau1 = ", tau1/1000, "ps")
            print ("E0   = ", E0, "eV")
            f = open(outname,"w"); f.close()
            for i in range(len(xdata)):
                f = open(outname,"a")
                f.write("%8.5f  %8.5f  %8.5f\n" % (xdata[i], ydata[i], func1(xdata[i], *popt)))
                f.close()
            #"""
            """
            # For func2
            alp, tau1, tau2, E0 = popt
            tau_total = alp*tau1 + (E0-alp)*tau2
            print ("Printing optimal fitting paramters:")
            print ("alp  = ", alp)
            print ("tau1 = ", tau1/1000, "ps")
            print ("tau2 = ", tau2/1000, "ps")
            print ("E0 = ", E0, "eV")
            print ("Printing average decay lifetime:", tau_total/1000, "ps")
            f = open(outname,"w"); f.close()
            for i in range(len(xdata)):
                f = open(outname,"a")
                f.write("%8.5f  %8.5f  %8.5f\n" % (xdata[i], ydata[i], func2(xdata[i], *popt)))
                f.close()
            """
            """
            # For func3
            tau1, beta, E0 = popt
            print ("Printing optimal fitting paramters:")
            print ("tau1 = ", tau1/1000, "ps")
            print ("beta = ", beta)
            print ("E0   = ", E0, "eV")
            f = open(outname,"w"); f.close()
            for i in range(len(xdata)):
                f = open(outname,"a")
                f.write("%8.5f  %8.5f  %8.5f\n" % (xdata[i], ydata[i], func3(xdata[i], *popt)))
                f.close()
            """
            """
            # For func4
            tau, B, E0 = popt
            print ("Printing optimal fitting paramters:")
            print ("E0   = ", E0, "eV")
            print ("tau1 = ", tau, "fs")
            print ("B    = ", B)
            f = open(outname,"w"); f.close()
            for i in range(len(xdata)):
                f = open(outname,"a")
                f.write("%8.5f  %8.5f  %8.5f\n" % (xdata[i], ydata[i], func4(xdata[i], *popt)))
                f.close()
            """
            #"""
            # For func5
            tau, beta, B, E0 = popt
            print ("Printing optimal fitting paramters:")
            print ("E0   = ", E0, "eV")
            print ("beta = ", beta)
            print ("tau  = ", tau, "fs")
            print ("B    = ", B)
            f = open(outname,"w"); f.close()
            for i in range(len(xdata)):
                f = open(outname,"a")
                f.write("%8.5f  %8.5f  %8.5f\n" % (xdata[i], ydata[i], func5(xdata[i], *popt)))
                f.close()
            #"""

