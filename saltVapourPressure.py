# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 17:14:03 2022

@author: r11403eb
"""

import math
import numpy as np
from tqdm import tqdm 
import pandas as pd
import scipy.optimize as sciop
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly
from sklearn.metrics import r2_score
from ase import Atom
from scipy.spatial import ConvexHull
from statsmodels.stats.weightstats import DescrStatsW
pi = np.pi
import scipy.special as spec 
from scipy.fft import fft, fftfreq
from scipy.stats import kde
import seaborn as sns
import re 


#%% <div class="csl-entry">Iida, T., Kita, Y., &#38; Morita, Z. ichiro. (1993). An Equation for Vapor Pressure and Its Application to Molten Salts. <i>ISIJ International</i>, <i>33</i>(1), 75–78. https://doi.org/10.2355/ISIJINTERNATIONAL.33.75</div>

class SaltP:
    
    def __init__(self,T=1200,dH,sigma,p):
        
        self.data = pd.DataFrame(data=[[1260,1983,186,127,1.528],
                                  [1074,1738,116,54,1.611],
                                  [1020,1666,100,60,1.615],
                                  [954,1603,79,23,1.512]],
                            columns=['Tm','Tb','Sigma_m','Sigma_b','log_Pm'],
                            index=['NaF','NaCl','NaBr','KI'])
        self.T = T
        self.dH = dH
        self.sigma = sigma
        self.p = p
        
        
        
    def p(self):
        sigma = self.sigma
        T = self.T
        dH = self.dH
    
        C2 = 4.2e13
        N = 6.0221408e23
        k = 1.380649e-23
        
        p = C2*sigma**(3/2)*T**(-1/2)*np.exp(-dH/(N*k*T))
        
        return p 
    
    def getHv(self):
        T = self.T
        p = self.p
        sigma = self.sigma
        
        p = np.e**p
        C2 = 4.2e13
        N = 6.0221408e23
        k = 1.380649e-23
        
        Hv = np.log((p*T**(1/2))/(C2*sigma**(3/2)))*N*k*-T
        
        return Hv
    
    def printAllFour(self):
        
        data = self.data
        T = self.T
        
        
        data['Hv'] = SaltPP.getHv(self,data['log_Pm'],data['Tm'],data['Sigma_m'])
        
        NaF = (SaltPP.p(self,T,data['Hv']['NaF'],data['Sigma_m']['NaF']))/100000
        NaCl = (SaltPP.p(self,T,data['Hv']['NaCl'],data['Sigma_m']['NaCl']))/100000
        NaBr = (SaltPP.p(self,T,data['Hv']['NaBr'],data['Sigma_m']['NaBr']))/100000
        KI = (SaltPP.p(self,T,data['Hv']['KI'],data['Sigma_m']['KI']))/100000
        
        print(f"Partial pressures (Bar) at {T}(\u2103) are: \n NaF - {NaF} \n NaCl - {NaCl} \n NaBr - {NaBr} \n KI - {KI}")

#SaltPP(T=1200).printAllFour()

#%% Volumne calc
from scipy.constants import R

class VolHalo():
    
    '''
    compound: str Silver halides, AgF, AgCl, AgBr, AgI
    g mass of Silver halide in grams
    V volume in M3, just add e-6 after for cm3 
    bar, boolean; if you want to output the value as PA or bar. 
    
    
    This class calculates the volume of Diatomic halogen gas assuming the AgH does completely change into silver metal and diatomic gas. 
    
    
    '''
    

    
    def __init__(self,compound='AgF',Tc=1200,V=5.5e-6,g=1,bar=True):
        
        data = np.array([[107.87,126.87,143.32,187.77,234.77,38.00,70.91,159.81,253.81,19.00,34.45,79.90,126.90],
                [np.nan,np.nan,np.nan,np.nan,np.nan,1.171,6.343,9.75,np.nan,np.nan,np.nan,np.nan,np.nan],
                [np.nan,np.nan,np.nan,np.nan,np.nan,0.02896,0.05422,0.0591,np.nan,np.nan,np.nan,np.nan,np.nan]]).T
        data = data*[1,1e-3,1e-6]

        self.SH = pd.DataFrame(columns = ['Mr','vdw_a','vdw_b'],
                          index = ['Ag','AgF','AgCl','AgBr','AgI','F2','Cl2','Br2','I2','F','Cl','Br','I'],
                          data = data)
        
        self.compound = compound
        self.Tc = Tc
        self.V = V
        self.g = g
        self.bar = bar
        self.Tk = Tc+273.15
        self.n = 0.5/(self.SH['Mr'][compound])
        self.Hal = compound[-1]+'2'
        self.bar = bar
        
    def IdealPressure(self):
        
        '''
        The pressure calcualted using the ideal gas law
        '''
        n = self.n
        Tk = self.Tk
        V = self.V
        bar = self.bar
        
        p_PA = n*R*Tk/V
        
        if bar:
            p_bar = p_PA*1e-5
            return p_bar
        return 
    
    def vdw(self):
        
        '''
        calculated using the Van Der Walls equation of state. 
        
        equation coefficients taken from 
        
        https://www.engineeringtoolbox.com/non-ideal-gas-van-der-Waals-equation-constants-gas-law-d_1969.html
                
        '''
        
        
        Tk = self.Tk
        Hal = self.Hal
        n = self.n
        V = self.V
        bar = self.bar
        a = self.SH['vdw_a'][Hal]
        b = self.SH['vdw_b'][Hal]
        p_PA = (R*Tk/((V/n)-b)) - (a/((n/V)**2))
           
        if bar:
            p_bar = p_PA*1e-5
            return p_bar
        
        return p_PA










