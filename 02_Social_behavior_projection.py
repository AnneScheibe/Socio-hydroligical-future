"""
Created on Okt 2018

@author: Anne Scheibe

Subject: The script is used to calculate the social behavior and is called a socio-hydrological model.

Based on: Di Baldassarre, G., Viglione, A., Carr, G., Kuil, L., Yan, K., Brandimarte, L., & Bloschl, G.
(2015). Debates-perspectives on socio-hydrology: Capturing feedbacks between physical
and social processes. Water Resources Research, 51 (6), 4770-4781.

"""


import math
import pandas as pd

####################################################################################
# Definition of paramters
####################################################################################

basedir = "C:/Users/scheibe/Desktop/master_thesis_scheibe_anne"

####################################################################################
# Definition of constants
####################################################################################
F_initial = 0          # Initial value for relative flood damage F (Hydrology); output: range between 0 and 1
D_initial = 0.1        # Initial value for population density D (Demography); output: range between 0 and 1
H_initial = 0.         # Initial value for flood protection level {height of levees} H (Technology)
M_initial = 0.         # Initial value for societal memory of flood M (Society)

#W_initial = 1.        # Initial value for natural high water level --> should be an empirical list [...] "which are typically a
# sequence of impulses with different magnitudes and nonregular time arrivals" (Di Baldassarre et al 2015); unit: m 

#alpha_H = 10.         # Constant related to relationship between flood water levels to relative damage (Hydrology) 
                       # unit: [m] - Di Baldassarre et al (2015)
xi_H = 0.2             # Contant proportion of flood level enhancement due to presence of levees (Hydrology) - Di Baldassarre et al (2015)
rho_D = 0.03           # Constant maximum relative growthe rate (Demographs) unit:none - Di Baldassarre et al (2015)
alpha_D = 5.           # Constant ratio preparedness/ awareness (Demography) unit: none - Di Baldassarre et al (2015)
epsilon_T = 1.1        # Constant Safety factor for levee heightening (Technologogy) - unit: none - Di Baldassarre et al (2015)
kappa_T = 2e-05        # Constant protection level decay rate (Technology) unit: none - Di Baldassarre et al (2015)
#my_s = 0.06            # Constant memory loss rate (Society) unit: none - Di Baldassarre et al (2015) 

delta_t = 1.           # Size of time step --> important for defintion of "dimension of time"

####################################################################################
# Equations over time of Demography, Technology, Society  tide_serie_0995 
####################################################################################

s_values = [0.06]# 0.015,0.03,0.12,0.24]
alpha_Hs = [4.5]#,5,6,7,8,9,10,12,15]

surges = ['stationary', 'non_stationary']
rcps = ['26', '45', '60', '85']

for my_s in s_values:
  
    for alpha_H in alpha_Hs:

        for surge in surges:      
            for rcp in rcps:
                
                tide_series_file = "output/tide_series_rcp{}_{}.csv".format(rcp, surge)
                print(tide_series_file)
                tide_series = pd.read_csv(tide_series_file, index_col=0)
            
                time_range = tide_series.index.values
       
                for society in ['techno', 'green']:
                    print(society)
                    
                    output_D = pd.DataFrame(index=time_range)
                    output_M = pd.DataFrame(index=time_range)
                    output_L = pd.DataFrame(index=time_range)
                    output_H = pd.DataFrame(index=time_range)
                    output_P = pd.DataFrame(index=time_range)
                    output_W = pd.DataFrame(index=time_range)
                    output_F = pd.DataFrame(index=time_range)
                    
                    #for run_id in ["q99", "median", "q01"]: (edited) 
                    for run_id in tide_series.columns:
                        #print(run_id)
                        
                        # Defines a list with the length of time_range # All values are set as the initial value
                        D = [D_initial for t in range(len(time_range))]     
                        M = [M_initial for t in range(len(time_range))]
                        # Initial value for Loss L - Di Baldassarre et al (2015) calculates the loss as a product of flood damage and demography 
                        L = [0 for t in range(len(time_range))]             
                        H = [H_initial for t in range(len(time_range))] 
                        # Initial value of levee heightening P
                        P = [0 for t in range(len(time_range))]             
                        # water level (without flood enhancement due to levee)
                        W = [0 for t in range(len(time_range))]            
                        F = [F_initial for t in range(len(time_range))]        
                        
                        # time serice of flood height for 1850 to 2100
                        W =  tide_series[run_id].values 
                        
                        for time in range(len(time_range)):
                        
                            if W[time] + xi_H * H[time] > H[time]: # if water level (+ flood enhancement due to levee) exeeds levee height...
                                # ... then there is a damage > 0
                                F[time] = 1 - math.exp(- (W[time] + xi_H * H[time]) / [alpha_H])  
                             
        
                                if society is 'techno':
                                    P[time] = epsilon_T * (W[time] + xi_H * H[time] - H[time])
                                elif society is 'green': #green society
                                    P[time] = 0.
                            else:
                                # ... otherwise there is no damage
                                F[time] = 0.  # time +1
                                P[time] = 0.
                                    
                            L[time] = F[time] * D[time]    
                            
                            if time < len(time_range) -1: #last value does not drop to "0".
                                D[time + 1] = D[time] + delta_t * rho_D * (1 - D[time] * (1 + delta_t * alpha_D * M[time])) - delta_t * L[time]
                        
                                # levee height changes due to depreteation and possible protection increase
                                H[time + 1] = H[time] + delta_t * (P[time] - kappa_T * H[time])
                            
                                M[time + 1] = M[time] + delta_t * (L[time] - my_s * M[time]) 
                                #print(M)
                                
                        output_D[run_id] = D
                        output_M[run_id] = M
                        output_L[run_id] = L
                        output_H[run_id] = H
                        output_P[run_id] = P
                        output_W[run_id] = W
                        output_F[run_id] = F
        
                    output_D_filename = "output/output_D_{}_rcp{}_{}_alphaH{}_mu_{}.csv".format(
                            society,rcp, surge, alpha_H, my_s)
                    output_D.to_csv(output_D_filename, header=True)
                    
                    output_M_filename = "output/output_M_{}_rcp{}_{}_alphaH{}_mu_{}.csv".format(
                            society,rcp, surge, alpha_H, my_s)
                    output_M.to_csv(output_M_filename, header=True)
                    
                    output_L_filename = "output/output_L_{}_rcp{}_{}_alphaH{}_mu_{}.csv".format(
                            society,rcp, surge, alpha_H, my_s)
                    output_L.to_csv(output_L_filename, header=True)
                    
                    output_H_filename = "output/output_H_{}_rcp{}_{}_alphaH{}_mu_{}.csv".format(
                            society,rcp, surge, alpha_H, my_s)
                    output_H.to_csv(output_H_filename, header=True)
                    
                    output_P_filename = "output/output_P_{}_rcp{}_{}_alphaH{}_mu_{}.csv".format(
                            society,rcp, surge, alpha_H, my_s)
                    output_P.to_csv(output_P_filename, header=True)
                    
                    output_W_filename = "output/output_W_{}_rcp{}_{}_alphaH{}_mu_{}.csv".format(
                            society,rcp, surge, alpha_H, my_s)
                    output_W.to_csv(output_W_filename, header=True)
                    
                    output_F_filename = "output/output_F_{}_rcp{}_{}_alphaH{}_mu_{}.csv".format(
                            society,rcp, surge, alpha_H, my_s)
                    output_F.to_csv(output_F_filename, header=True)
                    