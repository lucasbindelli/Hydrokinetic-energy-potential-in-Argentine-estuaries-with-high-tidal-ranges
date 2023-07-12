import numpy as np
import pandas as pd
import geopandas as gpd
import contextily as ctx
import math

from Setting_the_PATH import *

# DATOS
Version = '03'

Estuarios = ['01_Rank3-RSC', '02_Rank3-RCo', '03_Rank3-RDe', '04_Rank3-RGr', '05_Rank3-RGa']
NombreEstuario = ['RSC', 'RCo', 'RDe', 'RGr', 'RGa']
CRS = [5344, 5344, 5345, 5344, 5344]    #CRS para cada estuario. Para Río Deseado es distinto al resto.
Scores = pd.DataFrame()

for j in range(len(Estuarios)):
    
    # PATHS
    PathInput_01 = Path_GIS_Energia + Estuarios[j] + '/'
    PathOutput_01 = Path_GIS_Energia
    FileNameInput_01 = NombreEstuario[j] + '_VariablesHidrocineticas_v10'
    FileNameOutput_01 = 'NREL-Scores'
    
    # Lectura del archivo
    data = gpd.read_file(PathInput_01 + FileNameInput_01 + '.GeoJSON')
    data = data.to_crs(CRS[j])
    data.loc[:, 'Area'] = data.area
    
    # print(data.loc[data.loc[:, 'potenciamed'] >= 500, 'Area'].sum() / 1000000)
    # quit()
    Scores.loc['NREL_mean-01 [-]', NombreEstuario[j]] = round(data.loc[data.loc[:, 'potenciamed'] >= 500, 'NREL'].mean(), 2)
    Scores.loc['NREL_Area-01 [km2]', NombreEstuario[j]] = round(data.loc[data.loc[:, 'potenciamed'] >= 500, 'Area'].sum() / 1000000, 2)
    Scores.loc['NREL_mean-02 [-]', NombreEstuario[j]] = round(data.loc[(data.loc[:, 'potenciamed'] >= 500) & (data.loc[:, 'NREL'] > 0), 'NREL'].mean(), 2)
    Scores.loc['NREL_Area-02 [km2]', NombreEstuario[j]] = round(data.loc[(data.loc[:, 'potenciamed'] >= 500) & (data.loc[:, 'NREL'] > 0), 'Area'].sum() / 1000000, 2)
    Scores.loc['NREL_max [-]', NombreEstuario[j]] = round(data.loc[:, 'NREL'].max(), 2)
    
# Guardado del archivo
Scores.to_csv(PathOutput_01 + FileNameOutput_01 + '_v' + Version + '.csv')
    
quit()
