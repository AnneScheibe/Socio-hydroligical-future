#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 13:32:07 2021

@author: insauer
This plot script provides a histograms of waterlevels for different time periods
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

basedir = '/home/insauer/mnt/ebm/anne/Socio-hydroligical-future/output/'


fig = plt.figure(constrained_layout=True, figsize=(7., 9.9))
gs = fig.add_gridspec(3, 2)
plt.subplots_adjust(wspace=0., hspace=0)
rcps = ['rcp26', 'rcp85']
statics = ['stationary', 'non_stationary']

years = [2020, 2060, 2100]

colors = ['blue', 'green']

for s, stat in enumerate(statics):
    
    ax1 = fig.add_subplot(gs[:, s])
    ax1.set_title(stat, position = (0.5,1.0))
    ax1.axis('off')

    for y, year in enumerate(years):
        ax1 = fig.add_subplot(gs[y, s])

        for r,rcp in enumerate(rcps):

            dat = pd.read_csv(basedir + 'output_W_green_{}_{}_alphaH4.5_mu_0.06.csv'.format(rcp, stat))
            dat = dat.loc[dat['Unnamed: 0'] == year]
            dat = np.array(dat.iloc[:, 1:])

            ax1.hist(dat[0], bins=20, alpha=0.5, edgecolor='k', label=rcp, color=colors[r])
            ax1.axvline(np.median(dat[0]), color=colors[r], linestyle='dashed', linewidth=1)
            ax1.set_title(year, position = (0.5,0.85))
        
        ax1.set_ylim((0,3800))
        ax1.set_xlim((0, 11))
        if s == 1:
            ax1.set_yticklabels([])
        if y != 2:
            ax1.set_xticklabels([])
        if (s==0) & (y==1):
            ax1.set_ylabel('Frequency')
    ax1.set_xlabel('Water level in m')



handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles, labels)
plt.savefig('/home/insauer/projects/Anne/socio-hydrological-future/Socio-hydroligical-future/figures/Figure2.pdf',bbox_inches = 'tight', format = 'pdf')

