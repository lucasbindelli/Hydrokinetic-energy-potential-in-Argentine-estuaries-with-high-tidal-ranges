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
AreasRUI = pd.DataFrame()

# PATHS
PathOutput_01 = Path_GIS_Energia
FileNameOutput_01 = 'RUI-Areas'

RUI_Index = [1, 2, 3, 4]

for j in range(len(Estuarios)):
    
    # PATHS
    PathInput_01 = Path_GIS_Energia + Estuarios[j] + '/'
    FileNameInput_01 = NombreEstuario[j] + '_VariablesHidrocineticas_v13'
    
    # Lectura del archivo
    data = gpd.read_file(PathInput_01 + FileNameInput_01 + '.GeoJSON')
    
    for i in range(len(RUI_Index)):
        # Me quedo con RUI = 1, 2, 3, 4
        FiltroRUI = data.loc[data.RUI == RUI_Index[i]]
        FiltroRUI = FiltroRUI.to_crs(CRS[j])
        
        # Calculo el área de cada celda
        FiltroRUI.loc[:, 'Area'] = FiltroRUI.area
    
        # Genero la tabla
        AreasRUI.loc['RUI = ' + str(RUI_Index[i]) + ' [Ha]', NombreEstuario[j]] = round(FiltroRUI.area.sum() / 10000, 2)       # En hectáreas
    
AreasRUI.to_csv(PathOutput_01 + FileNameOutput_01 + '_v' + Version + '.csv')
print(AreasRUI)

quit()
