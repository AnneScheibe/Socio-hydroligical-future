#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 16:25:07 2021

@author: insauer
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

basedir = '/home/insauer/mnt/ebm/anne/Socio-hydroligical-future/output_2017/'


fig = plt.figure(constrained_layout=True, figsize=(7., 3.))
gs = fig.add_gridspec(1, 2)
plt.subplots_adjust(wspace=0.25)
socs = ['techno', 'green']
titles = ['Levee-building society', 'Levee-less society']
rcps = ['rcp26', 'rcp85']

run = '180'


for s, soc in enumerate(socs):
    ax1 = fig.add_subplot(gs[0, s])
    ax2 = ax1.twinx()
    ax1.set_title(titles[s])
    w = pd.read_csv(basedir + 'output_W_{}_rcp26_stationary_alphaH4.5_mu_0.06.csv'.format(soc))
    h = pd.read_csv(basedir + 'output_H_{}_rcp26_stationary_alphaH4.5_mu_0.06.csv'.format(soc))
    l = pd.read_csv(basedir + 'output_L_{}_rcp26_stationary_alphaH4.5_mu_0.06.csv'.format(soc))
    d = pd.read_csv(basedir + 'output_D_{}_rcp26_stationary_alphaH4.5_mu_0.06.csv'.format(soc))
    ax2.plot(w['Unnamed: 0'], w[run], label='Water level')
    ax2.plot(h['Unnamed: 0'], h[run], color = 'k', linewidth=3, label='Levee height')
    ax1.plot(d['Unnamed: 0'], d[run], color = 'firebrick', label='Population density')
    #ax1.stem(l['Unnamed: 0'], l[run], linefmt='green',markerfmt='go', basefmt=' ', markeredgecolor='seagreen')
    (markers, stemlines, baseline) = ax1.stem(l['Unnamed: 0'], l[run], label = 'Damage')
    plt.setp(stemlines, linestyle="-", color="green", linewidth=3 )
    plt.setp(baseline, visible=False)
    plt.setp(markers, marker='o', markersize=7, markeredgecolor="darkgreen", markeredgewidth=2, color='green')
    ax1.set_ylim((-0.02, 0.53))
    ax2.set_xlim((2020, 2100))
    if s==1:
        ax2.set_ylabel('Waterlevel in m')
    else:
        ax1.set_ylabel('Damage and population density')
    
handles, labels = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax1.legend([handles[0],handles[1],handles2[0], handles2[1]] , [labels[0],labels[1],labels2[0], labels2[1]],frameon=True, fontsize = 6., loc = (0.5,0.2))
plt.savefig('/home/insauer/projects/Anne/socio-hydrological-future/Socio-hydroligical-future/figures/Figure3.pdf',bbox_inches = 'tight', format = 'pdf')

