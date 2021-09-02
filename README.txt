script: 
01_tide_sample 

The script is used to sample the water level projection.

Based on code published at https://github.com/scrim-network/BRICK and from Jun.-Prof. Dr. Nicole Glanemann.
Based on: 
Keller, K., & Srikrishnan, V. A. (2019, submitted). Ice sheet observations provide economic value 
of information for coastal ood risk management. Risk Analysis.

Garner, G. G., & Keller, K. (2018). Using direct policy search to identify robust strategies
in adapting to uncertain sea-level rise and storm surge. Environmental Modelling &
Software, 107 , 96-104.


script:
02_full_run

The script is used to calculate the social behavior and is called a socio-hydrological model.

Based on: Di Baldassarre, G., Viglione, A., Carr, G., Kuil, L., Yan, K., Brandimarte, L., & Bloschl, G.
(2015). Debates-perspectives on socio-hydrology: Capturing feedbacks between physical
and social processes. Water Resources Research, 51 (6), 4770-4781.

script:
03_seleted_distributions

The script is used to perform statistical calculations for the social behavior projections from 
script 02_full_run. The historical time series is calibrated and no water levels above 5 m are taken into account. 
For each variable, society, RCP, surge and per parameters alpha_H and my_s, a seperate dataframe is saved. 
This dataframe includes statistical quantities calculated for the total data length of 10,000 SOWs. 



script:
03a_stat_distribution

The script is used to perform a statistical summary for the social behavior projections from 
script 02_full_run. 

script:
04_plot_probability_distribution

The script is used to perform figures for the output of the social behavior projections from 
script 02_full_run. 

script:
05_plot_heatmap

The script is used to perform heatmaps for the output of the social behavior projections from 
script 02_full_run. 