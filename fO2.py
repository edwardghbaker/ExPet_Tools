
#%% import the libraries

import math as m
import numpy as np
import pandas as pd
import scipy.optimize as sciop
import matplotlib.pyplot as plt
from pandas import DataFrame
from matplotlib.pyplot import figure
import matplotlib as mpl
import mpl_toolkits as mpltk
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import PySimpleGUI as sg
import tkinter as tk
from functools import partial  
import scipy

#%% define the functions for the fO2 calculation

class utils():

    def floatify(x):
        try:
            float(x)
            return float(x)
        except:
            pass
        
        for i in range(np.shape(x)[0]):
            for j in range(np.shape(x)[1]):
                try:
                    x[i,j] = float(x[i,j])
                except:
                    pass
                try:
                    x.iloc[i,j] = float(x.iloc[i,j])
                except:
                    pass
        return x
#%%

class fo2():
    
    def __init__(self):
        Tc = self.Tc
        mV = self.mV
        buff = self.buff
        

    def NNO(Tc=1200,P=1):
        Tk = Tc+273.15
        fo2 = (-24930/Tk) + 9.36 + 0.046 * (P-1)/Tk
        return fo2
    
    def FMQ(Tc=1200,P=1):
        Tk = Tc+273.15
        fo2 = (-25096.3/Tk) + 8.735 + 0.11 * (P-1)/Tk
        return fo2
    
    def IW(Tc=1200,P=1):
        Tk = Tc+273.15
        fo2 = (-27489/Tk) + 6.702 + 0.055 * (P-1)/Tk
        return fo2

    def MH(Tc=1200,P=1):
        Tk = Tc+273.15
        fo2 = (-25700.6/Tk) + 14.558 + 0.019 * (P-1)/Tk
        return fo2

    def CoCoO(Tc=1200,P=1):
        Tk = Tc+273.15
        fo2 = (-24332.6/Tk) + 7.295 + 0.052 * (P-1)/Tk
        return fo2
        
    def CCO(Tc=1200,P=1):
        Tk = Tc+273.15
        fo2 = (-20586/Tk) - 0.044 + np.log10(P) - 0.028 * (P-1)/Tk
        return fo2

    def measure_ablsolute(Tc=1200,mV=770):
        fo2 =-(0.68 +((20.159*mV)/(Tc+273.15)))
        print(fo2)
        return fo2
    
    def measure(Tc=1200,mV=770,rel='NNO'):
        if 'NNO' in rel:
            x = fo2.NNO(Tc,1)

        if 'FMQ' in rel:
            x = fo2.FMQ(Tc,1)

        if 'IW' in rel:
            x = fo2.IW(Tc,1)

        if 'MH' in rel:
            x = fo2.MH(Tc,1)

        if 'CoCoO' in rel:
            x = fo2.CoCoO(Tc,1)

        if 'CCO' in rel:
            x = fo2.CCO(Tc,1)
            
        y =-(0.68 +((20.159*mV)/(Tc+273.15)))-x
        print(y)
        return y    
           
    def plotT(Tcmin=800,Tcmax=1600,P=1,buff=['NNO','FMQ','IW']):
        Tk = 273.15+np.linspace(Tcmin,Tcmax)
        ax = figure(figsize=(12, 8), dpi=240, facecolor='w', edgecolor='k')
        if 'NNO' in buff:
            plt.plot(Tk-273.15,fo2.NNO(Tk,P),label='NNO')
        
        if 'FMQ' in buff:
            plt.plot(Tk-273.15,fo2.FMQ(Tk,P),label='FMQ')
            
        if 'IW' in buff:
            plt.plot(Tk-273.15,fo2.IW(Tk,P),label='IW')
            
        if 'MH' in buff:
            plt.plot(Tk-273.15,fo2.MH(Tk,P),label='MH')
            
        if 'CoCoO' in buff:
            plt.plot(Tk-273.15,fo2.CoCoO(Tk,P),label='CoCoO')
            
        if 'CCO' in buff:
            plt.plot(Tk-273.15,fo2.CCO(Tk,P),label='CCO')
        plt.legend()
        plt.ylim(top=-1)
        plt.ylabel('fO$_2$ (log)')
        plt.xlabel('Temperature $^\circ$C')

    def plotP(Pmin=1,Pmax=20000,Tc=1200,buff=['NNO','FMQ','IW']):
        Tk = 273.15+Tc
        P = np.linspace(Pmin,Pmax)
        ax = figure(figsize=(12, 8), dpi=240, facecolor='w', edgecolor='k')
        if 'NNO' in buff:
            plt.semilogx(P,fo2.NNO(Tk,P),label='NNO')
        
        if 'FMQ' in buff:
            plt.semilogx(P,fo2.FMQ(Tk,P),label='FMQ')
            
        if 'IW' in buff:
            plt.semilogx(P,fo2.IW(Tk,P),label='IW')
            
        if 'MH' in buff:
            plt.semilogx(P,fo2.MH(Tk,P),label='MH')
            
        if 'CoCoO' in buff:
            plt.semilogx(P,fo2.CoCoO(Tk,P),label='CoCoO')
            
        if 'CCO' in buff:
            plt.semilogx(P,fo2.CCO(Tk,P),label='CCO')
        plt.legend()

        plt.ylabel('fO$_2$ (log)')
        plt.xlabel('P (Bar)')
        
    def gas(Tc=1200,d=0,rel='FMQ',P=1):
        if 'NNO' in rel:
            x = fo2.NNO(Tc,P)+d

        if 'FMQ' in rel:
            x = fo2.FMQ(Tc,P)+d

        if 'IW' in rel:
            x = fo2.IW(Tc,P)+d

        if 'MH' in rel:
            x = fo2.MH(Tc,P)+d

        if 'CoCoO' in rel:
            x = fo2.CoCoO(Tc,P)+d

        if 'CCO' in rel:
            x = fo2.CCO(Tc,P)+d
        
        fO2 = (10**x)
        R = 0.00198726
        TK = T + 273.18
        RK = (R*TK)
        dG1 = (62.110326 -(2.1444460*10**-2)*(T) +(4.720325*10**-7)*(T**2) -(4.5574288*10**-12)*(T**3) -(7.3430182*10**-15)*(T**4))
        K1 = m.exp(-dG1/(R*TK))
        dG2 = (62.110326 +(7.3219457*10**-4)*(T) -(3.416474*10**-7)*(T**2) +(4.7858617*10**-11)*(T**3))
        K2 = m.exp(-dG2/(R*TK))
        Rm = (K1-(3*K1*fO2)-(2*fO2**(3/2)))/(2*K1*fO2 + fO2 + (fO2**(3/2)) + (fO2**(1/2)))
        VolCO2 = 100/(1+Rm)
        return(VolCO2)
    
    
    def gas_absolute(T=1200,d=0,absolute=-12,P=1):
        fO2 = (10**absolute)
        R = 0.00198726
        TK = T + 273.18
        RK = (R*TK)
        dG1 = (62.110326 -(2.1444460*10**-2)*(T) +(4.720325*10**-7)*(T**2) -(4.5574288*10**-12)*(T**3) -(7.3430182*10**-15)*(T**4))
        K1 = m.exp(-dG1/(R*TK))
        dG2 = (62.110326 +(7.3219457*10**-4)*(T) -(3.416474*10**-7)*(T**2) +(4.7858617*10**-11)*(T**3))
        K2 = m.exp(-dG2/(R*TK))
        Rm = (K1-(3*K1*fO2)-(2*fO2**(3/2)))/(2*K1*fO2 + fO2 + (fO2**(3/2)) + (fO2**(1/2)))
        VolCO2 = 100/(1+Rm)
        return(VolCO2)

    def addGasMixingContours(d=0,rel='IW',P=1,xCO2=[0.001,0.01,0.1,0.5,0.9,0.99,0.999],axes=None):
        if axes is None:
            fig, axes = plt.subplots(1, 1, figsize=(8, 8))

        O2_data = utils.floatify(pd.read_csv('ThermoData/O2.csv',index_col=0))
        CO2_data = utils.floatify(pd.read_csv('ThermoData/CO2.csv',index_col=0))
        CO_data = utils.floatify(pd.read_csv('ThermoData/CO.csv',index_col=0))
        del_fH_CO = -110.53	#J/mol
        del_fH_CO2 = -393.52 #J/mol
        del_fH_O2 = 0 #kJ/mol
        xCO2 = np.array(xCO2)

        delH0_func = lambda A,B,C,D,E,F,H,T: A*(T/1000) + (B*(T/1000)**2)/2 + (C*(T/1000)**3)/3 + (D*(T/1000)**4)/4 - E/(T/1000) + F - H
        s0_func = lambda A,B,C,D,E,G,T: A*np.log((T/1000)) + B*(T/1000) + (C*(T/1000)**2)/2 + (D*(T/1000)**3)/3 - E/(2*(T/1000)**2) + G
        def H_S_O2(Tk):
            delH0 = np.array([])
            s0 = np.array([])
            for T in Tk:
                if T <= 700:
                    A,B,C,D,E,F,G,H = O2_data['100. - 700.'][:8]
                    delH0 = np.append(delH0,delH0_func(A,B,C,D,E,F,H,T))
                    s0 = np.append(s0,s0_func(A,B,C,D,E,G,T))
                elif T > 700 and T <= 2000:
                    A,B,C,D,E,F,G,H = O2_data['700. - 2000.'][:8]
                    delH0 = np.append(delH0,delH0_func(A,B,C,D,E,F,H,T))
                    s0 = np.append(s0,s0_func(A,B,C,D,E,G,T))
                elif T > 2000:
                    A,B,C,D,E,F,G,H = O2_data['2000. - 6000.'][:8]
                    delH0 = np.append(delH0,delH0_func(A,B,C,D,E,F,H,T))
                    s0 = np.append(s0,s0_func(A,B,C,D,E,G,T))
                else:
                    print('Error - H_S_O2')
            return delH0,s0
        
        def H_S_CO(Tk):
            delH0 = []
            s0 = []
            for T in Tk:
                if T <= 1200:
                    A,B,C,D,E,F,G,H = CO_data['298. - 1200.'][:8]
                    delH0 = np.append(delH0,delH0_func(A,B,C,D,E,F,H,T))
                    s0 = np.append(s0,s0_func(A,B,C,D,E,G,T))
                elif T > 1200:
                    A,B,C,D,E,F,G,H = CO_data['1200. - 6000.'][:8]
                    delH0 = np.append(delH0,delH0_func(A,B,C,D,E,F,H,T))
                    s0 = np.append(s0,s0_func(A,B,C,D,E,G,T))
                else:
                    print('Error - H_S_CO')
            return delH0,s0

        def H_S_CO2(Tk):
            delH0 = []
            s0 = []
            for T in Tk:
                if T <= 1300:
                    A,B,C,D,E,F,G,H = CO2_data['298. - 1300.'][:8]
                    delH0 = np.append(delH0,delH0_func(A,B,C,D,E,F,H,T))
                    s0 = np.append(s0,s0_func(A,B,C,D,E,G,T))
                elif T > 1300:
                    A,B,C,D,E,F,G,H = CO2_data['1300. - 6000.'][:8]
                    delH0 = np.append(delH0,delH0_func(A,B,C,D,E,F,H,T))
                    s0 = np.append(s0,s0_func(A,B,C,D,E,G,T))
                else:
                    print('Error - H_S_CO2')
            return delH0,s0

        Tc = np.linspace(800,1600,801)
        Tk = Tc + 273.15
        R = scipy.constants.R
        delH0_O2, s0_O2 = H_S_O2(Tk)
        delH0_CO, s0_CO = H_S_CO(Tk)
        delH0_CO2, s0_CO2 = H_S_CO2(Tk)

        delG = 2*(del_fH_CO2+delH0_CO2-Tk*s0_CO2) - 2*(del_fH_CO+delH0_CO-Tk*s0_CO) - (del_fH_O2+delH0_O2-Tk*s0_O2)
        # print(xCO2)
        fO2 = lambda xCO2: ((xCO2/(1-xCO2))**2)*(np.exp(delG/(R*Tk)))

        if rel == 'NNO':
            x = fo2.NNO(Tc,P)+d
        elif rel == 'FMQ':
            x = fo2.FMQ(Tc,P)+d
        elif rel == 'IW':
            x = fo2.IW(Tc,P)+d
        elif rel == 'MH':
            x = fo2.MH(Tc,P)+d
        elif rel == 'CoCoO':
            x = fo2.CoCoO(Tc,P)+d
        elif rel == 'CCO':
            x = fo2.CCO(Tc,P)+d
        else:
            x = 0

        print(x)

        cmap = mpl.cm.get_cmap('Greys')

        for i in xCO2:
            axes.plot(Tc,np.log(fO2(i))-x,label=str(i))
        plt.legend()
        plt.show()
        return axes

#%%