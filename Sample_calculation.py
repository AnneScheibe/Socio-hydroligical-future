# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 11:47:54 2021

@author: scheibe
"""

import pandas as pd

from scipy.stats import gumbel_r
import numpy as np

import matplotlib.pyplot as plt

basedir = "C:/Users/scheibe/Documents/GitHub/Socio-hydroligical-future"

parameters = ['W', 'H', 'F', 'L','D', 'M', 'P']
societies = ['techno', 'green']
surges = ['stationary', 'non_stationary']
rcps = ["26", "45", "60", "85"] 

#####################################################################################
results = pd.DataFrame()

for society in societies:#[:1]:
    for rcp in rcps:#[:1]:
        for surge in surges:#[:1]:
            for parameter in parameters:#[:1]:
                print(parameter)
                
                filepath = "{}/output/1995_2005/output_{}_{}_rcp{}_{}_alphaH4.5_mu_0.06.csv".format(
                        basedir, parameter, society, rcp, surge)
                file_series = pd.read_csv(filepath, index_col=0)

                file_series = [file_series]
                loc, scale = gumbel_r.fit(file_series)
                
                #print(year)    
                print(loc)
                print(scale)

                df = pd.DataFrame({
                    #"year": year,
                    "parameter" : parameter,
                    "society" : society,
                    "surge": surge,
                    "rcp": rcp,
                    "loc" : loc,
                    "scale" : scale,
                }, index=np.array([0])) 

                results = results.append(df, ignore_index=True)
                outfilepath = "{}/output/1995_2005/loc_scale.csv".format(basedir)
                results.to_csv(outfilepath)
    #print(outfilepath)
                        

                        
                        
#                        df = []
#                        np.random.seed(1) # Makes sure that always the same sample is drawn
#                        for i in range(len(years)):
#                            for j in range(10000):
#                                print("run_id{}".format(j))
#    
#                                a = np.random.gumbel(loc, scale, 1)
#                                a = a[0]
#                                print(a)
#                            
#                                df.append({"projected_parameter": a,
#                                           "time": years[i],
#                                           "run_id": j,})
#                            
#                            data = pd.DataFrame.from_records(df, index="time")
#                            data = data.pivot(columns='run_id', values='projected_parameter')
#                            
#                            print(data.median(axis=1))
#                            print(data.mean(axis=1))
#                            #data.to_csv("{}output/projections/data/NDL_sampled_waterlevel_projections_without_slr_from_history_new.csv".format(basedir))