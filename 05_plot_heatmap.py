"""
Created on Jan 2019

@author: Anne Scheibe

Subject: The script is used to perform heatmaps for the output of the social behavior projections from 
script 02_full_run. 

"""

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

basedir = "C:/Users/scheibe/Desktop/master_thesis/new_modelruns/plot_output_2017/"

parameters = ['M', 'H', 'L', 'F', 'D', 'W'] 
societies = ['techno', 'green']

mu_s_values = [0.015,0.03,0.06,0.12,0.24]
alpha_Hs = [15,12,10,9,8,7,6,5,4.5]

surges = ['stationary','non_stationary']
rcps = ["26", "45", "60", "85"]

value_names = {
    'M': 'social memory (M)',
    'L': 'losses (L)',
    'F': 'relativ flood damage (F)',
    'H': 'height of levees (H)',
    'D': 'population density (D)',
    'W': 'water level (W)',
}

society_names = {
        'techno' : 'Levee-building society',
        'green' : 'Levee-less society'}
                    
####################################################################################
# SUPPLEMENT - single plot heatmap, mean of max values
####################################################################################
for parameter in parameters:
    for society in societies: 
        
        fig, ax = plt.subplots(4 , 2,  figsize=(15, 30), dpi=100, sharey=True)
        # [left, bottom, width, height] 
        cbar_ax = fig.add_axes([.92, .3, .03, .4], alpha=0.8) 
        
        for rcp_index, rcp in enumerate(rcps):
            for surge_index, surge in enumerate(surges):
                
                out = np.zeros((len(alpha_Hs), len(mu_s_values)))
                
                for row, alpha_H in enumerate(alpha_Hs):
                    for col, mu in enumerate(mu_s_values):
                        
                        filepath = "{}{}_{}_rcp{}_{}_alphaH{}_mu_{}.csv".format(basedir,
                                parameter, society, rcp, surge, alpha_H, mu)
                                               
                        df = pd.read_csv(filepath, index_col=0)

                        #max_df = df.max(axis=1)
                        out[row, col] = df['quant_995'].max()
                        
                        
                matrix = pd.DataFrame(out, index=alpha_Hs, columns=mu_s_values)        

                fig.suptitle('Maximum of upper percentile {} - {}'.format(
                        value_names[parameter], society_names[society]), fontsize= 20)
                        
                sns.heatmap(matrix, ax=ax[rcp_index, surge_index], 
                            cbar_ax = cbar_ax, cbar=True,
                            linewidths=0.1,
                            linecolor='gray',
                            rasterized=True,
                            alpha=0.8,
                            cmap="YlGnBu",
                            annot=True, annot_kws={"size": 8}
                            )
                
                ax[3, 0].set_xlabel(
                        '${\u03BC_s}$ - Memory loss rate', fontsize= 15)
                ax[3, 1].set_xlabel(
                        '${\u03BC_s}$ - Memory loss rate', fontsize= 15)
                
                
                ax[0, 0].set_ylabel(
                        '${\u03B1_H}$ - Flood water level to relative damage', fontsize= 15)
                ax[1, 0].set_ylabel(
                        '${\u03B1_H}$ - Flood water level to relative damage', fontsize= 15)
                ax[2, 0].set_ylabel(
                        '${\u03B1_H}$ - Flood water level to relative damage', fontsize= 15)
                ax[3, 0].set_ylabel(
                        '${\u03B1_H}$ - Flood water level to relative damage', fontsize= 15)
                
                
                
                ax[rcp_index, surge_index].set_title('RCP{} {}'.format(
                        rcp, surge.replace('_', '-')), fontsize= 12)
                                
                plt.tight_layout()  
               
                
                plt.subplots_adjust(
                        hspace=0.2,     # 0.2 # the amount of height reserved for space between subplots,
                                        # expressed as a fraction of the average axis height
                        wspace=0.15,    # 0.2 # the amount of width reserved for space between subplots,
                                        # expressed as a fraction of the average axis width
                        left= 0.125,    # 0.125 # the left side of the subplots of the figure
                        top = 0.95,     #0.9 # the top of the subplots of the figure
                        right = 0.9,    #0.9 # the right side of the subplots of the figure
                        bottom = 0.1    #0.1 # the bottom of the subplots of the figure
                        )
                
                plt.savefig(
                        'plot_output_2017/heatmap_{}_mean-max_{}.pdf'.format(
                                parameter,society))

