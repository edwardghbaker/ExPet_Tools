import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% Read the data

ArTest = pd.read_csv(r"C:\Users\User\OneDrive - The University of Manchester\Experiments\Ar test.csv", header = 3, low_memory=False)

#%% Plot the data
ArTest['Time'] = ArTest['Time']/(60*60*24) # convert to days
ArTest.plot(x='Time', y='fO2', kind='line', color='red', label='mV')
plt.ylabel('mV')
plt.xlabel('Time (days)')
pl

# %%
