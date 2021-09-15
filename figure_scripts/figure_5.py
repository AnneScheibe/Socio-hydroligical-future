#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 11:29:18 2021

@author: insauer
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

basedir = '/home/insauer/mnt/ebm/anne/Socio-hydroligical-future/output_2017/'


fig = plt.figure(constrained_layout=True, figsize=(9.9, 7.))
gs = fig.add_gridspec(3, 6)
#plt.subplots_adjust(wspace=0)
variables = ['D','L','F']
socs = ['techno', 'green']
rcps = ['rcp85', 'rcp26']
years = [2020, 2060, 2100]
ylabels = ['Population density', 'Damage', 'Relative damage']
soc_title = ['Levee-building society', 'Levee-less society']
colors = ['green', 'blue']
run = '180'


for y,year in enumerate(years):
    
    for v, var in enumerate(variables):
        for s, soc in enumerate(socs):
            if y==0:
                ax1 = fig.add_subplot(gs[:, 2*v+s])
                ax1.set_title(soc_title[s], position=(0.5, 1.02), fontsize=7.5)
                ax1.axis('off')
            #ax1 = fig.add_subplot(gs[y, 5*v+2*s:5*v+2*s+2])
            ax1 = fig.add_subplot(gs[y, 2*v+s])
            for r, rcp in enumerate(rcps):
                dat = pd.read_csv(basedir + 'output_{}_{}_{}_non_stationary_alphaH4.5_mu_0.06.csv'.format(var, soc, rcp))
                dat = dat.loc[dat['Unnamed: 0'] == year]
                dat = np.array(dat.iloc[:, 1:])
    
                ax1.hist(dat[0], bins=20, alpha=0.5, edgecolor='k', label=rcp, color=colors[r])
                ax1.axvline(np.median(dat[0]), color=colors[r], linestyle='dashed', linewidth=1)
            ax1.set_title(str(year), position=(0.5, 1.0), fontsize=7)
        
        ax1 = fig.add_subplot(gs[:, 2*v:2*v+2])
        ax1.set_title(ylabels[v], position=(0.5, -0.1), fontsize=12)
        ax1.axis('off')
            # if v==0:
                
            #     ax1.set_ylim((0,2000))
            #     ax1.set_xlim((0, 1.0))
            
            # if v==1:
                
            #     ax1.set_ylim((0,10000))
            #     ax1.set_xlim((0, 0.5))
            # if v==2:
            #     ax1.set_ylim((0,10000))
            #     ax1.set_xlim((0, 1.0))
            #elif v==1:
                
                
                
                #ax1.plot(dat['Unnamed: 0'], mean, color=colors[0,r], label=rcp, linestyle = '--')
                #ax1.set_ylabel(ylabels[v])
            #ax1.set_ylim((0,3800))
        #     ax1.set_xlim((2020, 2100))
            
        # if (s==1) & (v==1):
        #     handles, labels = ax1.get_legend_handles_labels()
        #     ax1.legend(handles, labels)

plt.savefig('/home/insauer/projects/Anne/socio-hydrological-future/Socio-hydroligical-future/figures/Figure5_pure_ns.pdf',bbox_inches = 'tight', format = 'pdf')
