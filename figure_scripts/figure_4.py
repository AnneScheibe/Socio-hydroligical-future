#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 07:49:47 2021

@author: insauer
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

basedir = '/home/insauer/mnt/ebm/anne/Socio-hydroligical-future/output_2017/'


fig = plt.figure(constrained_layout=True, figsize=(7., 9.9))
gs = fig.add_gridspec(6, 2)
#plt.subplots_adjust(wspace=0)
variables = ['W','H','D','L','F', 'L']
socs = ['techno', 'green']
rcps = ['rcp85', 'rcp26']
ylabels = [ 'Water level', 'Levee height', 'Population density', 'Damage', 'Relative damage', 'Accumulated damage']

run = '180'

colors=np.array([['green','blue'],
        ['darkslategrey','darkgray'],
        ['sienna','darksalmon'],
        ['darkgreen', 'mediumseagreen'],
        ['orange','gold']
        ])
ax1 = fig.add_subplot(gs[:, 0])
ax1.set_title('Levee-building society', position=(0.5, 1.0))
ax1.axis('off')

ax1 = fig.add_subplot(gs[:, 1])
ax1.set_title('Levee-less society', position=(0.5, 1.0))
ax1.axis('off')

for v, var in enumerate(variables):

    for s, soc in enumerate(socs):
        ax1 = fig.add_subplot(gs[v, s])
        
        for r, rcp in enumerate(rcps):
            dat = pd.read_csv(basedir + 'output_{}_{}_{}_stationary_alphaH4.5_mu_0.06.csv'.format(var, soc, rcp))
            if v==5:
                cuml = dat.iloc[:,1:].cumsum(axis=0)
                mean = cuml.iloc[:,1:].mean(axis=1)
                median = cuml.iloc[:,1:].median(axis=1)
                perc_low = cuml.iloc[:,1:].quantile(q=0.005, axis=1)
                perc_high = cuml.iloc[:,1:].quantile(q=0.995, axis=1)
            else:
                mean = dat.iloc[:,1:].mean(axis=1)
                median = dat.iloc[:,1:].median(axis=1)
                perc_low = dat.iloc[:,1:].quantile(q=0.005, axis=1)
                perc_high = dat.iloc[:,1:].quantile(q=0.995, axis=1)
            ax1.plot(dat['Unnamed: 0'], median, color=colors[0,r], label=rcp)
            #ax1.plot(dat['Unnamed: 0'], mean, color=colors[0,r], label=rcp, linestyle = '--')
            ax1.set_ylabel(ylabels[v])

            ax1.fill_between(dat['Unnamed: 0'],perc_high, perc_low, color=colors[0,r], linewidth = 1., alpha=0.2)

            #ax1.set_ylim((0,3800))
            ax1.set_xlim((2020, 2100))
            
        if (s==1) & (v==1):
            handles, labels = ax1.get_legend_handles_labels()
            ax1.legend(handles, labels)

plt.savefig('/home/insauer/projects/Anne/socio-hydrological-future/Socio-hydroligical-future/figures/Figure4_ext.pdf',bbox_inches = 'tight', format = 'pdf')
