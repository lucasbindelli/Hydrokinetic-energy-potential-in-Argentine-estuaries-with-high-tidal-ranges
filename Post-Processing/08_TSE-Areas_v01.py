import numpy as np
import pandas as pd
import geopandas as gpd
import contextily as ctx

from Setting_the_PATH import *

# DATOS
Version = '02'

Estuarios = ['01_Rank3-RSC', '02_Rank3-RCo', '03_Rank3-RDe', '04_Rank3-RGr', '05_Rank3-RGa']
NombreEstuario = ['RSC', 'RCo', 'RDe', 'RGr', 'RGa']

CRS = [5344, 5344, 5345, 5344, 5344]    #CRS para cada estuario. Para Río Deseado es distinto al resto.
AreasTSE = pd.DataFrame()

# PATHS
PathOutput_01 = Path_GIS_Energia
FileNameOutput_01 = 'TSE-Areas'

for j in range(len(Estuarios)):
    
    # PATHS
    PathInput_01 = Path_GIS_Energia + Estuarios[j] + '/'
    FileNameInput_01 = NombreEstuario[j] + '_VariablesHidrocineticas_v08'
    
    # Lectura del archivo
    data_TSE = gpd.read_file(PathInput_01 + FileNameInput_01 + '.GeoJSON')
    
    # Me quedo con IHE > 1
    FiltroTSE = data_TSE.loc[data_TSE.TSE_ndl_v0 > 1]
    FiltroTSE = FiltroTSE.to_crs(CRS[j])
    
    # Calculo el área de cada celda
    FiltroTSE.loc[:, 'Area'] = FiltroTSE.area
    
    # Genero la tabla
    AreasTSE.loc['TSE > 1 [Ha]', NombreEstuario[j]] = round(FiltroTSE.area.sum() / 10000, 2)       # En hectáreas
    
AreasTSE.to_csv(PathOutput_01 + FileNameOutput_01 + '_v' + Version + '.csv')
print(AreasTSE)

quit()
