import numpy as np
import pandas as pd
import geopandas as gpd
import contextily as ctx

from Setting_the_PATH import *

# DATOS
Version = '04'

Estuarios = ['05_Rank3-RGa']#['01_Rank3-RSC', '02_Rank3-RCo', '03_Rank3-RDe', '04_Rank3-RGr', '05_Rank3-RGa']
NombreEstuario = ['RGa']#['RSC', 'RCo', 'RDe', 'RGr', 'RGa']
Lat_a_KM = 69.1

h1 = 2
h2 = 5
h3 = 16
v0 = 1.5
h0 = 5

for j in range(len(Estuarios)):
    
    # PATHS
    PathInput_01 = Path_GIS_Energia + Estuarios[j] + '/'
    PathOutput_01 = PathInput_01
    FileNameInput_01 = NombreEstuario[j] + '_VariablesHidrocineticas'
    FileNameInput_02 = NombreEstuario[j] + '_Velocidades-TSE'
    FileNameOutput_01 = FileNameInput_01 + '_v' + Version
    
    # Lectura del archivo
    data = gpd.read_file(PathInput_01 + FileNameInput_01 + '.GeoJSON')
    data_TSE = gpd.read_file(PathInput_01 + FileNameInput_02 + '.GeoJSON')
    
    data.loc[data.loc[:, 'hprom'] - (data.loc[:, 'hmax'] - data.loc[:, 'hmin']) / 2 <= h1, 'Eta_v0'] = 0
    data.loc[(data.loc[:, 'hprom'] - (data.loc[:, 'hmax'] - data.loc[:, 'hmin']) / 2 > h1) & (data.loc[:, 'hprom'] - (data.loc[:, 'hmax'] - data.loc[:, 'hmin']) / 2 < h2), 'Eta_v0'] = 1 / (h2 - h1) * (data.loc[:, 'hprom'] - (data.loc[:, 'hmax'] - data.loc[:, 'hmin']) / 2 - h1)
    data.loc[(data.loc[:, 'hprom'] - (data.loc[:, 'hmax'] - data.loc[:, 'hmin']) / 2 >= h2) & (data.loc[:, 'hprom'] - (data.loc[:, 'hmax'] - data.loc[:, 'hmin']) / 2 < h3), 'Eta_v0'] = 1
    data.loc[data.loc[:, 'hprom'] - (data.loc[:, 'hmax'] - data.loc[:, 'hmin']) / 2 >= h3, 'Eta_v0'] = 1 / data.loc[:, 'hprom'] * (h3 + (data.loc[:, 'hmax'] - data.loc[:, 'hmin']) / 2)
    
    data.loc[:, 'TSE_ndl_v0'] = data.loc[:, 'Eta_v0'] / (2 * v0**3 * h0) * ((data_TSE.loc[:, 'vel_flow']) ** 3 + (data_TSE.loc[:, 'vel_ebb']) ** 3) * data.loc[:, 'hprom']
    
    data.to_file(PathOutput_01 + FileNameOutput_01 + '.GeoJSON', driver='GeoJSON')
    
quit()
