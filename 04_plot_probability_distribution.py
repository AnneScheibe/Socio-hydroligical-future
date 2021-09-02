"""
Created on Jan 2019

@author: Anne Scheibe

Subject: The script is used to perform figures for the output of the social behavior projections from 
script 02_full_run. 

"""

import pandas as pd
import matplotlib.pyplot as plt


basedir = "C:/Users/scheibe/Desktop/master_thesis_scheibe_anne/"


parameters = ['M', 'L','H', 'F', 'W','D', ]
societies = ['green', "techno"] 
surges = ['stationary', 'non_stationary' ]
rcps = ["26",  "45", "60", "85"] 

y_labels = {
    'M': 'Social memory [-]',
    'L': 'Accumulated losses [-]',
    'F': 'Relativ flood damage [-]',
    'H': 'Height of levees [m]',
    'D': 'Population density [-]',
    'W': 'Water level [m]',
}

value_names = {
    'M': 'Social memory (M)',
    'L': 'Losses (L)',
    'F': 'Relativ flood damage (F)',
    'H': 'Height of levees (H)',
    'D': 'Population density (D)',
    'W': 'Water level (W)',
}

society_names = {
        'techno' : 'Levee-building society',
        'green' : 'Levee-less society'
}

####################################################################################
# Plot 
####################################################################################
for parameter in parameters:#[:1]:
    print(parameter)
    for society in societies: 
        fig, ax = plt.subplots(4 , 2,  figsize=(15, 20), dpi=100, sharey=True)
#                            
#        fig.suptitle('{} - {} \n with {} = 10 m and {} = 0.06'.format(
#                value_names[parameter],
#                society_names[society], '$\\alpha_H$', '$\\mu_s$'), fontsize= 20)  
        
        fig.suptitle('{} - {}'.format(
                value_names[parameter],
                society_names[society]), fontsize= 20) 
        
        for row, rcp in enumerate(rcps):
            for col, surge in enumerate(surges):
                
                filepath = "{}output/{}_{}_rcp{}_{}_alphaH4.5_mu_0.06.csv".format(basedir,
                        parameter, society, rcp, surge)
                file_series = pd.read_csv(filepath, index_col=0)
                #print(rcp, surge)
               
                #max      mean    median       min  quant_005  quant_995
               # The gray stripe shows data from the 99,5 % quantiel to the 0,05% quantiel. 
                ax[row, col].fill_between(file_series.index, 
                                 file_series['quant_005'], 
                                 file_series['quant_995'], 
                                 color='lightgray')
                
                #plots the selected quantiel, in this case 0.995 % quantiel 
                file_series['median'].plot(ax=ax[row, col], 
                                      color='black',
                                      linewidth=3)
                             
#                #plots the selected quantiel, in this case 0.995 % quantiel 
#                file_series['mean'].plot(ax=ax[row, col], 
#                                      color='black',
#                                      linewidth=3)
                
                # select time series with extreme values, in that case values 
                # that are higher than mean_tide_series.max()  -> this selection 
                # returned a boolean             
                file_series['select_max'].plot(ax=ax[row, col], 
                           legend=False,
                           color='xkcd:coral',
                           alpha=0.8,
                           linewidth=2)
              
                file_series['select_min'].plot(ax=ax[row, col],
                           legend=False,
                           color='xkcd:azure',
                           alpha=0.8,
                           linewidth=2)
                
                ax[row, col].set_ylabel(y_labels[parameter], fontsize=12)
                ax[row, col].set_xlim(2017.,2100.)
                #ax[row, col].set_ylim(0.35, 0.45)
                ax[0, 0].set_xlabel('Time', fontsize= 12)
                ax[0, 1].set_xlabel('Time', fontsize= 12)
                
                ax[row, col].set_title('RCP{} {}'.format(
                            rcp, surge.replace('_', '-')), fontsize= 12)
                                    
                plt.tight_layout()  
                  
                plt.subplots_adjust(hspace=0.4, wspace=0.15, left= 0.125, 
                                    top = 0.9, right = 0.9, bottom = 0.1)
                    
        plt.savefig('{}output/probability_distribution_from_2017_{}_{}_alphaH45_mu_006.pdf'.format(
                basedir, parameter,society))

