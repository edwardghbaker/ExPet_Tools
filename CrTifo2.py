# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 10:12:17 2020

@author: user
"""
import math as m
import numpy as np
import pandas as pd
import scipy.optimize as sciop
import matplotlib.pyplot as plt
from pandas import DataFrame
from matplotlib.pyplot import figure
import matplotlib as mpl
from fO2 import fo2

logfo2 = np.linspace(-4,-20,1001)
T = 1274


#%% Borisov 2012 Ti3+/Ti4+

def borisov(T,fO2):
    Tk = T+273.15
    logti4ti3=(0.22*fO2)+(6435/Tk)+0.37
    ti4ti3=10**(logti4ti3)
    ti3ti4=1/(ti4ti3)
    return(ti3ti4)


#%% Berry Oniel 2004

def berryoniel(fO2):
    cr2crt = 1/(1+10**(0.25*fO2+1.871))
    crtcr2 = 1/cr2crt
    cr3cr2 = crtcr2-1
    cr2cr3 = 1/cr3cr2
    return(cr3cr2)

#%% Experiments at WHOI

experimentsFO2 = np.array([-0.7678,-0.8267,-3.301,-0.2919,-2.2747])-9.729
expfo2 = experimentsFO2
col = ['r','g','g','g','g']
exp_labels = ['Fail','Exp',None,None,None]

#%% Plotting 
fig,ax = plt.subplots(1,1,figsize=(5,3),dpi=480)
ax.plot(logfo2,borisov(T,logfo2),lw=1,label='Ti$^{3+}$')
ax.plot(logfo2,berryoniel(logfo2),lw=1,label='Cr$^{3+}$')
ax.vlines(-9.729,-1,5,label='Iron-Wustite buffer',color='k',ls='--',lw=3)

for i,j,col in zip(experimentsFO2[1:],exp_labels[1:],col[1:]):
    ax.vlines(i,-1,5,label=j,color=col,lw=2)

ax.set_ylim((0,1))
ax.set_xlim((-20,-4))
ax.text(-9,0.1,str(str(T)+'$^\circ$C'),weight=520)
#plt.title('Chromium and Titanium Speciation')
ax.set_ylabel('M$^{3+}$/M$^{Other}$')
ax.set_xlabel('Log(fO$_2$)')

ax.legend()