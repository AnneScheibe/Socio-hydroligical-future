"""
Created on Okt 2018

@author: Anne Scheibe

Subject: The script is used to sample the water level projection.

Based on code published at https://github.com/scrim-network/BRICK and from Jun.-Prof. Dr. Nicole Glanemann.
Based on: 
Keller, K., & Srikrishnan, V. A. (2019, submitted). Ice sheet observations provide economic value 
of information for coastal ood risk management. Risk Analysis.

Garner, G. G., & Keller, K. (2018). Using direct policy search to identify robust strategies
in adapting to uncertain sea-level rise and storm surge. Environmental Modelling &
Software, 107 , 96-104.

"""
import pandas as pd
import xarray as xr
import scipy.stats

#################################################################################################
# Parameter for sea levels
#################################################################################################

n_years=300
sl_window= 30 
first_year = 2017
num_sows = 10000
#surge_stationary = True
#dps_information == 'remote'
dps_information = 'local'



basedir = "C:/Users/scheibe/Documents/GitHub/Socio-hydroligical-future"

#################################################################################################
# generate sea levels
#################################################################################################
# "We use a states-of-the-world (SOWs) approach about SLR and storm surge to introduce uncertainty 
# to the SLR adaptation model and provide coverage of tail-area events." (Garner, G. G., & 
# Keller, K. (2018). Using direct policy search to identify robust strategies in adapting to 
# uncertain sea-level rise and storm surge. Environmental Modelling & Software, 107, 96-104.)

# generate synthetic tidal records from mean sea level simulations and surge distributions.
# surge distributions can be stationary or not; temperature simulations must be included if
# they are stationary. We only consider a non-stationary location parameter for now.
def synth_tidal_records(mean_sea_levels,  # numpy array of mean sea levels for a particular SOW
                        GEV_params, # tuple of GEV parameters, (loc, scale, shape). if non-stationary, loc is the coefficient of temp.
                        surge_stationary=True,  # is the surge distribution stationary?
                        temp=None):  # pass a numpy array of global mean temperatures if the surge distribution is non-stationary.

    if surge_stationary:
        # scipy.stats.genextreme has a different sign convention than R for GEV shape parameters
        ann_max_surge = scipy.stats.genextreme.rvs(c=-GEV_params['shape'], loc=GEV_params['loc'], scale=GEV_params['scale'],
                                                   size=len(mean_sea_levels))
    else:
        ann_max_surge = scipy.stats.genextreme.rvs(c=-GEV_params['shape'], loc=(GEV_params['loc1'] * temp)+GEV_params['loc0'],
                                                   scale=GEV_params['scale'],size=len(mean_sea_levels))
    return mean_sea_levels + ann_max_surge/1000

# function to use for pandas apply on each SOW for generating synthetic tidal records.
def apply_synth_tidal(SOW,
                     surge_stationary=True):

    if surge_stationary:
        return synth_tidal_records(SOW.LocalSeaLevel, SOW.SurgeParams, surge_stationary)
    else:
        return synth_tidal_records(SOW.LocalSeaLevel, SOW.SurgeParams, surge_stationary, SOW.Temperature)

for surge_stationary in [True, False]:
    
    if surge_stationary:
        surge = "stationary"

    else:
        surge = "non_stationary"
    print(surge, surge_stationary)
 
   # for rcp in ["26"]:
    for rcp in ["26", "45", "60", "85"]:
        print("RCP{}".format(rcp))

        tide_series_output_file = "output/tide_series_rcp{}_{}.csv".format(rcp, surge)
        print(tide_series_output_file)
        tide_series_output_path = "{}/{}".format(basedir, tide_series_output_file)
        
        # read in mean sea level projection files
        sea_level_files = ["{}/{}".format(
                basedir, "data/BRICK_LSL_NED_RCP{}.nc".format(rcp)
                )]
        print(sea_level_files)
      
        # read in mean sea level projection files
        sea_level_projections =  [xr.open_dataset(file, engine='netcdf4').to_dataframe() for file in sea_level_files]
          
        # normalize mean sea levels and temperatures and ice_variables to the reference year (the first year of the simulation)
        tidal_variables = ['LocalSeaLevel']
        if not surge_stationary:
            tidal_variables += ['Temperature']
        if dps_information == 'remote':
            ice_variables = ['AIS', 'GIS']
        else:
            ice_variables = None
            
        for slr in sea_level_projections:
            for tidal_var in tidal_variables:
                slr[tidal_var] = slr[tidal_var] - slr[tidal_var].xs(first_year, level='time_proj')
        
        
        # convert files to a list of pandas dataframes
        sea_level_proj_unstack = [proj.unstack(level=1) for proj in sea_level_projections]
        # concatenate into a single ensemble
        sea_level_ens_unstack = pd.concat(sea_level_proj_unstack, ignore_index=True)
        sea_level_ensemble = sea_level_ens_unstack.stack()
       
        # sample SOWs (.sample - Return a random sample of items from an axis of object.; replace : bool, default False - 
        # Sample with or without replacement.)
        sea_level_samples = sea_level_ensemble.unstack().sample(num_sows, replace=True).reset_index(drop=True).stack()
    
        # import surge distributions
        if surge_stationary:
            surge_file ='data/Delfzijl_gev_stationary.csv'
            surge_fit = pd.read_csv(surge_file, names=['loc', 'scale', 'shape'], usecols=[1, 2, 3], skiprows=1)
            # sample surge SOWs
            surge_samples = surge_fit.sample(num_sows, replace=True).reset_index(drop=True)
            # for each SOW, generate tide gauge series
            tide_samples = pd.concat([sea_level_samples['LocalSeaLevel'].unstack('time_proj'), surge_samples], axis=1,
                                         keys=['LocalSeaLevel', 'SurgeParams'])
        else:
            surge_file ='data/Delfzijl_gev_nonstationary.csv'
            surge_fit = pd.read_csv(surge_file, names=['loc0', 'loc1', 'scale', 'shape'],
                                        usecols=[1, 2, 3, 4], skiprows=1)
            surge_samples = surge_fit.sample(num_sows, replace=True).reset_index(drop=True)
            tide_samples = pd.concat([sea_level_samples['LocalSeaLevel'].unstack('time_proj'),
                                          sea_level_samples['Temperature'].unstack('time_proj'),
                                          surge_samples], axis=1, keys=['LocalSeaLevel', 'Temperature', 'SurgeParams'])
        
        #generate synthetic tidal records from mean sea level simulations and surge distributions
        if surge_stationary:
            tide_series = tide_samples.apply(apply_synth_tidal, surge_stationary=True, axis=1)
        else:
            tide_series = tide_samples.apply(apply_synth_tidal, surge_stationary=False, axis=1) 
        
        tide_series = tide_series.T
        tide_series.index = tide_series.index.astype(int)
        print(tide_series.tail())
        if dps_information == 'remote':
            ice_series = sea_level_samples['AIS'] + sea_level_samples['GIS']
        else:
            ice_series = None
            
        tide_series.to_csv(tide_series_output_path)
        print(tide_series_output_path) 


    
