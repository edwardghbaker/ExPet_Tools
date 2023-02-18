import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

#%% scrape the NIST tables for O2, CO2 and CO from the NIST website

# NIST website for O2
O2_url = 'https://webbook.nist.gov/cgi/inchi?ID=C7782447&Mask=1&Type=JANAFG&Table=on#JANAFG'

# NIST website for CO2
CO2_url = 'https://webbook.nist.gov/cgi/inchi?ID=C630080&Mask=1&Type=JANAFG&Table=on#JANAFG'

# NIST website for CO
CO_url = 'https://webbook.nist.gov/cgi/inchi?ID=C124389&Mask=1&Type=JANAFG&Table=on#JANAFG'

# read the tables from the NIST website
O2 = pd.read_html(O2_url, header=0, index_col=0)
CO2 = pd.read_html(CO2_url, header=0, index_col=0)
CO = pd.read_html(CO_url, header=0, index_col=0)


#%% save the tables as csv files

O2[0].to_csv('ThermoData/O2.csv')
CO2[0].to_csv('ThermoData/CO2.csv')
CO[0].to_csv('ThermoData/CO.csv')

