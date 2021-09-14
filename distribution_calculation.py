# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 11:47:54 2021

@author: scheibe
"""

from scipy.stats import gumbel_r
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

basedir = "C:/Users/scheibe/Documents/GitHub/Socio-hydroligical-future"

#####################################################################################################
###   Draw samples from the distribution:
#####################################################################################################

#mu, beta = 2.048638063558476, 0.4965320953010091 # location and scale for NLD from history time series
#paramaters are drawn from 'output/1995_2005/loc_scale.csv'
loc, scale = 0.102104118, 0.073307957

# Years for ISIMIP projections
years = [1995, 1996, 1997, 1998, 1999, 2000, 2001,2002,2003,2004, 2005]

df = []
np.random.seed(1) # Makes sure that always the same sample is drawn
for i in range(len(years)):
    
    for j in range(10000):
        print("run_id{}".format(j))
        
        a = np.random.gumbel(loc, scale, 1)
        a = a[0]
        print(a)
        
        #parameter
        df.append({"M": a,
                   "time": years[i],
                   "run_id": j,})
    
    data = pd.DataFrame.from_records(df, index="time")
    # parameter
    data = data.pivot(columns='run_id', values='M')
    
    #outfilepath = "{}/output/1995_2005/Sample_M_techno_non_stationary_rcp85.csv".format(basedir)
    outfilepath = "{}/output/1995_2005/Sample_M_green_non_stationary_rcp85.csv".format(basedir)
    
    data.to_csv(outfilepath)


x = data.mean(axis=1)
print("Mean {}".format(x.mean()))

y = data.median(axis=1)
print('Median {}'.format(y.mean()))

