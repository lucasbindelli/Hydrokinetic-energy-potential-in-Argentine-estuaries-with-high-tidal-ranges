import numpy as np
import pandas as pd
import geopandas as gpd
import contextily as ctx

from Setting_the_PATH import *

# DATOS
Version = '08'

Estuarios = ['01_Rank3-RSC', '02_Rank3-RCo', '03_Rank3-RDe', '04_Rank3-RGr', '05_Rank3-RGa']
NombreEstuario = ['RSC', 'RCo', 'RDe', 'RGr', 'RGa']
NombreReferencias = ['01_RSC', '02_RCo', '03_RDe', '04_RGr', '05_RGa']
CRS = ['PSGR07f2', 'PSGR07f2', 'PSGR07f3', 'PSGR07f2', 'PSGR07f2']
# Lat_a_KM = 69.1

HEref = 0.2
href = 50
lref = 7500
Cfarm_gref = 1.5 * href**3 + 34624.31 * href + 196.96 * lref + 22500

l = [6500, 3700, 5700, 2800, 10600]

Ugp = 0.9


for j in range(len(Estuarios)):
    
    # PATHS
    PathInput_01 = Path_GIS_Energia + Estuarios[j] + '/'
    PathInput_02 = Path_GIS_RefGeograficas + NombreReferencias[j] + '/'
    PathOutput_01 = PathInput_01
    
    FileNameInput_01 = NombreEstuario[j] + '_VariablesHidrocineticas'
    FileNameInput_02 = NombreEstuario[j] + '_Potencias-IHE'
    FileNameInput_03 = NombreEstuario[j] + '_CanalDeAccesoAlPuerto_' + CRS[j] + '_POL_v01'
    FileNameOutput_01 = FileNameInput_01 + '_v' + Version
    
    # Lectura del archivo
    data = gpd.read_file(PathInput_01 + FileNameInput_01 + '_v04' + '.GeoJSON')
    data_IHE = gpd.read_file(PathInput_01 + FileNameInput_02 + '.GeoJSON')
    
    data.loc[:, 'Cfarm_g'] = 1.5 * data.loc[:, 'hprom']**3 + 34624.31 * data.loc[:, 'hprom'] + 196.96 * l[j] + 22500
    data.loc[:, 'Cgp'] = 1 - data.loc[:, 'Cfarm_g'] / Cfarm_gref
    
    data_IHE.loc[:, 'Coef_Ugp'] = 0.9
    
    if j == 0 or j == 2 or j == 4:
        
        CanalDeAcceso = gpd.read_file(PathInput_02 + FileNameInput_03 + '.gpkg')
        CanalDeAcceso = CanalDeAcceso.to_crs(4326)
        
        # Anulo las celdas que caen dentro de los canales de acceso a los puertos
        DatosFiltrados = gpd.tools.sjoin(data_IHE, CanalDeAcceso, predicate='intersects', how='left')   # predicate = 'within'
        DatosFiltrados.loc[DatosFiltrados.loc[:, 'index_right'] == 0, 'Coef_Ugp'] = 0
        
    else:
        DatosFiltrados = data_IHE
        
    data.loc[:, 'IHE_v0'] = (data_IHE.loc[:, 'potenciamed'] / 1000 * data.loc[:, 'Cgp'] * DatosFiltrados.loc[:, 'Coef_Ugp']) / HEref
    
    data.to_file(PathOutput_01 + FileNameOutput_01 + '.GeoJSON', driver='GeoJSON')
    
quit()
# DatosFiltrados = DatosFiltrados.dropna(how='any')
    
    
# TENGO QUE VER COMO ENCONTRAR LOS VALORES QUE NO SON NAN PARA PONER QUE UGP = 0
print(DatosFiltrados)#.loc[25000:25400].to_string())
quit()