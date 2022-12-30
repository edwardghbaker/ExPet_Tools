# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 14:35:18 2022

@author: r11403eb
"""

from fO2 import fo2

import numpy as np
import pandas as pd
import scipy.optimize as sciop
import matplotlib.pyplot as plt
from pandas import DataFrame
from matplotlib.pyplot import figure

def D_Cl_fo2(Tc=1200,Ppa=10,plot=True):
    Tk = Tc+273.15
    Pgpa = Ppa*1e-9
    Pbar = Ppa-1e-5
    fo2_arg = np.linspace(0,-6,1000)
    
    fugacity = fo2.IW(Tc,Pbar)
    
    Cl_melt_Cl_fug = 0.5*10**(0.984-((930*Pgpa)/Tc)-0.25*(fugacity-fo2_arg))
    
    if plot:
        fig,ax=plt.subplots(figsize=(12,8))
        ax.plot((fo2_arg),Cl_melt_Cl_fug)
        ax.set_xlabel('Relative to IW (log10)')
        
        
        
    return Cl_melt_Cl_fug
    

D_Cl_fo2()