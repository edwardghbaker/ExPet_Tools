
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



from matplotlib.backends.backend_tkagg import *
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import tkinter as tk  
from tkinter import ttk


    
def COMPandDISP():
    Tc = Tcinput.get()
    P = Pinput.get()
    a = str(round(fo2.NNO(Tc,P),2))
    b = str(round(fo2.FMQ(Tc,P),2))
    c = str(round(fo2.IW(Tc,P),2))
    d = str(round(fo2.MH(Tc,P),2))
    e = str(round(fo2.CoCoO(Tc,P),2))
    f = str(round(fo2.CCO(Tc,P),2))
    tk.Label(root,text=a).grid(row=1,column=4,padx=(30,0))
    tk.Label(root,text=b).grid(row=2,column=4,padx=(30,0))
    tk.Label(root,text=c).grid(row=3,column=4,padx=(30,0))
    tk.Label(root,text=d).grid(row=4,column=4,padx=(30,0))
    tk.Label(root,text=e).grid(row=5,column=4,padx=(30,0))
    tk.Label(root,text=f).grid(row=6,column=4,padx=(30,0))
   
root = tk.Tk()
root.title('Oxygen Fugacity')
root.geometry("500x400")


Tcinput = tk.IntVar(master=root,value=1200)  
Pinput = tk.IntVar(master=root,value=1)   
Temp_input = tk.Entry(root, width=15, borderwidth=5,textvariable=Tcinput)
Temp_input.grid(row=1,column=1)
P_input = tk.Entry(root, width=15, borderwidth=5,textvariable=Pinput)
P_input.grid(row=2,column=1)

Templabel = tk.Label(root,text='Temperature (C)').grid(row=1,column=0)
Plabel = tk.Label(root,text='Pressure (bar)').grid(row=2,column=0)

tk.Label(root, text='NNO').grid(row=1,column=3,padx=(30,0),pady=(10,10))
tk.Label(root, text='FMQ').grid(row=2,column=3,padx=(30,0),pady=(10,10))
tk.Label(root, text='IW').grid(row=3,column=3,padx=(30,0),pady=(10,10))
tk.Label(root, text='MH').grid(row=4,column=3,padx=(30,0),pady=(10,10))
tk.Label(root, text='CoCoO').grid(row=5,column=3,padx=(30,0),pady=(10,10))
tk.Label(root, text='CCO').grid(row=6,column=3,padx=(30,0),pady=(10,10))

comp = tk.Button(root, text='Compute', command=lambda: COMPandDISP()).grid(row=3,column=1)


root.mainloop()
