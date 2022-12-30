# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 17:42:21 2022

@author: r11403eb
"""

from fO2 import fo2
import numpy as np
import pandas as pd
import os as os 

directory_files = os.listdir()

working_list_txt = [i for i in directory_files if '.txt' in i and 'V' in i]
working_list_excel = [i for i in directory_files if '.xls' in i and 'V' in i]

for i in working_list_txt:
    pd.read_csv(i)
    