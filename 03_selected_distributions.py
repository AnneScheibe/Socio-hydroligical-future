"""
Created on Feb 2019

@author: Anne Scheibe

Subject: The script is used to perform statistical calculations for the social behavior projections from 
script 02_full_run. The historical time series is calibrated and no water levels above 5 m are taken into account. 
For each variable, society, RCP, surge and per parameters alpha_H and my_s, a seperate dataframe is saved. 
This dataframe includes statistical quantities calculated for the total data length of 10,000 SOWs. 

"""
import pandas as pd

basedir = "C:/Users/scheibe/Desktop/master_thesis_scheibe_anne/"

parameters = ['W', 'H', 'F', 'L','D', 'M', 'H']
societies = ['techno', 'green']
surges = ['stationary', 'non_stationary']
rcps = ["26", "45", "60", "85"] 

s_values = [0.06]# 0.015,0.03,0.12,0.24]
alpha_Hs = [4.5]#,5,6,7,8,9,10,12,15]

#####################################################################################
## 
#####################################################################################

for my_s in s_values:
    for alpha_H in alpha_Hs:
        for society in societies:
            for rcp in rcps:
                for surge in surges:
                    for parameter in parameters:
                        print(parameter)
                        
                        filepath = "output/output_{}_{}_rcp{}_{}_alphaH{}_mu_{}.csv".format(
                                parameter, society, rcp, surge, alpha_H, my_s)
                        file_series = pd.read_csv(filepath, index_col=0)
                        print(rcp, surge, alpha_H, my_s)
                        
                        if parameter is ('W'):
                            #adjustment of historical values 
                            selection_hist = file_series.loc[:2017].max() < 5
                            
                        print(len(file_series.columns))
                        file_series = file_series[selection_hist[selection_hist].index]
                        print(len(file_series.columns))
                        
                        # two example time series are selected 
                        median_file_series = file_series.median(axis=1)
                        selection_min  = (file_series.min() <= median_file_series.min())                   
                        selection_max  = (file_series.max() >= median_file_series.mean()) 
                                               
                        df = pd.DataFrame({
                            "min": file_series.min(axis=1),
                            "quant_005" : file_series.quantile(0.005, axis=1),
                            "mean" : file_series.mean(axis=1),
                            "median" : file_series.median(axis=1), 
                            "max" : file_series.max(axis=1),
                            "quant_995" : file_series.quantile(0.995, axis=1), 
                            "select_min" : file_series[selection_min[selection_min].index[2]],
                            "select_max" : file_series[selection_max[selection_max].index[1]] 
                        })
          
                        outfilepath = "{}output/{}_{}_rcp{}_{}_alphaH{}_mu_{}.csv".format(basedir,
                                parameter, society, rcp, surge, alpha_H, my_s)
                        df.to_csv(outfilepath)
                        print(outfilepath)
