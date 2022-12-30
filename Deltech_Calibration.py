# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 13:46:30 2022

@author: r11403eb
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import scipy.optimize as sciop

#%% Make the fits and defien function 

cmap = mpl.cm.get_cmap('coolwarm')
T_calib = pd.DataFrame(data = {'1000EUT':[974,977,977,976,972,964,950],
                     '1200EUT':[1169,1172,1172,1170,1168,1162,1152],
                     '1400EUT':[1353,1358,1361,1362,1361,1357,1351],
                     '1500EUT':[1455,1458,1459,1459,1458,1454,1448]})

fit_list = np.array([])
fig,ax = plt.subplots(figsize=(6,8))

ax.set_xlabel('Distance (cm)')
ax.set_ylabel('$\u0394$ Temperature ($\u00B0$C)')

for i,j in zip(T_calib.columns,[1000,1200,1400,1500]):
    k = cmap((j-1000)/500)
    ax.scatter(x=T_calib.index,y=T_calib[i]-j,label=i,cmap='coolwarm',color=k)
    
    fit = (np.polyfit(x=T_calib.index,y=T_calib[i]-j,deg=2))
    fit_list = np.append(fit_list,fit)
    X = np.linspace(min(T_calib.index),max(T_calib.index),1000)
    Y = fit[0]*X**2 + fit[1]*X + fit[2]
    ax.plot(X,Y,color=k)
    ax.legend()

fit_list = fit_list.reshape((4,3))
X = np.linspace(min(T_calib.index),max(T_calib.index),1000)

EUT1000_fit = pd.DataFrame([X,(fit_list[0,0]*X**2 + fit_list[0,1]*X + fit_list[0,2])]).transpose()
EUT1200_fit = pd.DataFrame([X,(fit_list[1,0]*X**2 + fit_list[1,1]*X + fit_list[1,2])]).transpose()
EUT1400_fit = pd.DataFrame([X,(fit_list[2,0]*X**2 + fit_list[2,1]*X + fit_list[2,2])]).transpose()
EUT1500_fit = pd.DataFrame([X,(fit_list[3,0]*X**2 + fit_list[3,1]*X + fit_list[3,2])]).transpose()

abc = pd.DataFrame(data = {'height_index' : [], 'offset' : []})

for df in [EUT1000_fit,EUT1200_fit,EUT1400_fit,EUT1500_fit]:
    xyz = pd.DataFrame(data = {'height_index': [float(df[df[1]==max(df[1])].index.values)],'offset':[max(df[1])]})
    abc = abc.append(xyz)
    
abc['height'] = abc['height_index']*6/1000
abc['target_T'] = np.array([1000,1200,1400,1500])

offset_fit = np.polyfit(abc['target_T'],abc['offset'],deg=2)
height_fit = np.polyfit(abc['target_T'],abc['height'],deg=2)

ax.plot()


def getEUT(TT):
    height = height_fit[0]*TT**2 + height_fit[1]*TT + height_fit[2]
    T_act = lambda EUT, TT : abs(EUT - TT + offset_fit[0]*EUT**2 + offset_fit[1]*EUT + offset_fit[2])
    
    EUT_ideal = sciop.minimize(T_act, x0=TT, args=(TT))
    return round(EUT_ideal.x[0]), height


x,y = getEUT(1200)
