import numpy as np
import pandas as pd
import geopandas as gpd
import contextily as ctx
import math

from Setting_the_PATH import *

# DATOS
Version = '13'

Estuarios = ['01_Rank3-RSC', '02_Rank3-RCo', '03_Rank3-RDe', '04_Rank3-RGr', '05_Rank3-RGa']
NombreEstuario = ['RSC', 'RCo', 'RDe', 'RGr', 'RGa']

for j in range(len(Estuarios)):
    
    # PATHS
    PathInput_01 = Path_GIS_Energia + Estuarios[j] + '/'
    PathOutput_01 = PathInput_01
    FileNameInput_01 = NombreEstuario[j] + '_VariablesHidrocineticas_v10'
    FileNameOutput_01 = NombreEstuario[j] + '_VariablesHidrocineticas'
    
    # Lectura del archivo
    data = gpd.read_file(PathInput_01 + FileNameInput_01 + '.GeoJSON')
    
    data.loc[(data.loc[:, 'hmin'] >= 0) & (data.loc[:, 'hmin'] < 20), 'Tamaño'] = 'Chico'
    data.loc[(data.loc[:, 'hmin'] >= 20) & (data.loc[:, 'hmin'] < 50), 'Tamaño'] = 'Grande'
    
    data.loc[(data.loc[:, 'potenciamed'] >= 500) & (data.loc[:, 'potenciamed'] < 1000), 'Destino'] = 'Testeo'
    data.loc[data.loc[:, 'potenciamed'] >= 1000, 'Destino'] = 'Operativo'
    
    data.loc[(data.loc[:, 'Tamaño'] == 'Chico') & (data.loc[:, 'Destino'] == 'Testeo'), 'RUI'] = 1
    data.loc[(data.loc[:, 'Tamaño'] == 'Chico') & (data.loc[:, 'Destino'] == 'Operativo'), 'RUI'] = 2
    data.loc[(data.loc[:, 'Tamaño'] == 'Grande') & (data.loc[:, 'Destino'] == 'Testeo'), 'RUI'] = 3
    data.loc[(data.loc[:, 'Tamaño'] == 'Grande') & (data.loc[:, 'Destino'] == 'Operativo'), 'RUI'] = 4
    
    data.to_file(PathOutput_01 + FileNameOutput_01 + '_v' + Version + '.GeoJSON', driver='GeoJSON')
    
quit()