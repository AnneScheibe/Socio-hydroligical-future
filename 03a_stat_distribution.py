"""
Created on Feb 2019

@author: Anne Scheibe

Subject: The script is used to perform a statistical summary for the social behavior projections from 
script 02_full_run. 

"""

import pandas as pd

basedir = "C:/Users/scheibe/Desktop/master_thesis_scheibe_anne/"

parameters = ['W', 'H', 'F', 'L','D', 'M']
societies = ['techno', 'green']
surges = ['stationary', 'non_stationary']
rcps = ["26", "45", "60", "85"] 


#####################################################################################
## 
#####################################################################################

results = []
for society in societies:
    for rcp in rcps:
        for surge in surges:
            for parameter in parameters:
                print(society, parameter)
                
                
                # Calculations were performed currently for alpha_H = 4.5 and mu_s = 0.06.
                # For another parameter combination these values have to be changed. 
                filepath = "{}output/{}_{}_rcp{}_{}_alphaH4.5_mu_0.06.csv".format(basedir,
                        parameter, society, rcp, surge)
                df = pd.read_csv(filepath, index_col=0)
                print(rcp, surge)
               
                print('1850',rcp, surge, society, df['mean'][1850])
                print('2017',rcp, surge, society, df['mean'][2017])
                print('2100',rcp, surge, society, df['mean'][2100])                
                
                summaries = []
                for col in df.columns:
                    summaries.append(df[col].describe()[1:])
                summary = pd.concat(summaries, axis=1)
                summary = summary.T
                summary['rcp'] = rcp
                summary['parameter'] = parameter
                summary['society'] = society
                summary['surge'] = surge
                results.append(summary)
results = pd.concat(results)

results.index.name = 'variable'
results = results.reset_index()
results = results.set_index(['parameter', 'rcp', 'surge', 'society', 'variable'])
results = results.sort_index()
results.to_csv('{}output/statistics_summary_alphaH4.5_mu_0.06.csv'.format(basedir))
                
#print(results.loc['W', '26', 'stationary'])

