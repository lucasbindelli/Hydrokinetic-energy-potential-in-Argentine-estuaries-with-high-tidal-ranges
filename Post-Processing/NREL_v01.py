import numpy as np
import pandas as pd
import geopandas as gpd
import contextily as ctx
import math

from Setting_the_PATH import *

# DATOS
Version = '10'

Estuarios = ['01_Rank3-RSC', '02_Rank3-RCo', '03_Rank3-RDe', '04_Rank3-RGr', '05_Rank3-RGa']
NombreEstuario = ['RSC', 'RCo', 'RDe', 'RGr', 'RGa']

# import matplotlib.pyplot as plt
# import math
# mercado = np.arange(0, 1000, 0.1)
# S_m = np.zeros(shape=(10000,1))
# Base = 10
# for m in mercado:
    # if m < 0.300:
        # S_m[int(m*10)] = 0
    # elif m >= 0.300 and m < 300:
        # S_m[int(m*10)] = 10 + (math.log(m,Base) - math.log(300,Base)) / (math.log(300000,Base) - math.log(300,Base)) * 10
    # elif m >= 300:
        # S_m[int(m*10)] = 10
    # else:
        # S_m[int(m*10)] = 0
# fig, ax = plt.subplots()
# plt.plot(mercado, S_m)
# ax.set_xscale('log')
# plt.show()
# quit()

wi = 1/5

for j in range(len(Estuarios)):
    
    # PATHS
    PathInput_01 = Path_GIS_Energia + Estuarios[j] + '/'
    PathOutput_01 = PathInput_01
    FileNameInput_01 = NombreEstuario[j] + '_VariablesHidrocineticas_v08'
    # FileNameInput_02 = NombreEstuario[j] + '_Potencias-NREL'
    FileNameOutput_01 = NombreEstuario[j] + '_VariablesHidrocineticas'
    
    # Lectura del archivo
    data = gpd.read_file(PathInput_01 + FileNameInput_01 + '.GeoJSON')
    
    
    # Profundidad
    data.loc[data.loc[:, 'hprom'] < 5, 'S_h'] = 0
    data.loc[(data.loc[:, 'hprom'] >= 5) & (data.loc[:, 'hprom'] < 20), 'S_h'] = (data.loc[:, 'hprom'] - 5) / (20 - 5) * 10
    data.loc[(data.loc[:, 'hprom'] >= 20) & (data.loc[:, 'hprom'] < 60), 'S_h'] = 10
    data.loc[(data.loc[:, 'hprom'] >= 60) & (data.loc[:, 'hprom'] < 150), 'S_h'] = 10 - (data.loc[:, 'hprom'] - 60) / (150 - 60) * 10 
    data.loc[data.loc[:, 'hprom'] >= 150, 'S_h'] = 0
    
    # if h < 5:
        # S_h[h] = 0
    # elif h >=5 and h < 20:
        # S_h[h] = (h - 5) / (20 - 5) * 10
    # elif h >= 20 and h < 60:
        # S_h[h] = 10
    # elif h >= 60 and h < 150:
        # S_h[h] = 10 - (h - 60) / (150 - 60) * 10 
    # else:
        # S_h[h] = 0

    # Densidad de potencia
    data.loc[data.loc[:, 'potenciamed'] / 1000 < 0.5, 'S_TMD'] = 0
    data.loc[(data.loc[:, 'potenciamed'] / 1000 >= 0.5) & (data.loc[:, 'potenciamed'] / 1000 < 2), 'S_TMD'] = (data.loc[:, 'potenciamed'] / 1000 - 0.0) / (2 - 0.0) * 10
    data.loc[data.loc[:, 'potenciamed'] / 1000 >= 2, 'S_TMD'] = 10
    
    # if TMD/10 < 0.5:
        # S_TMD[TMD] = 0
    # elif TMD/10 >= 0.5 and TMD/10 < 2:
        # S_TMD[TMD] = (TMD/10 - 0.0) / (2 - 0.0) * 10
    # elif TMD/10 >= 2:
        # S_TMD[TMD] = 10
    # else:
        # S_TMD[TMD] = 0
    
    # Recurso Mareomotriz
    gamma = 0.22
    rho = 1024
    g = 9.81
    a = [11.5, 12, 6, 8, 12.5]
    Qmax = [111090, 27307, 17108, 6888, 184157]

    P = gamma * rho * g * a[j] * Qmax[j]
    
    m = P   # Tamaño del mercado limitado por el recurso, no por la demanda
    Base = 10
    
    if m < 0.300:
        S_m = 0
    elif m >= 0.300 and m < 300:
        S_m = 10 + (math.log(m,Base) - math.log(300,Base)) / (math.log(300000,Base) - math.log(300,Base)) * 10
    elif m >= 300:
        S_m = 10
    else:
        S_m = 0

    # Distancia
    # d = [16.500, 16.500, 16.500, 16.500, 16.500]
    d = [0.500, 22.000, 0.500, 0.500, 0.500]
    if d[j] < 1:
        S_d = 10
    elif d[j] >= 1 and d[j] < 20:
        S_d = 10 - (d[j] - 1) / (20 - 1) * 10
    else:
        S_d = 0

    # Transporte
    t = 104
    if t < 60:
        S_t = 10
    elif t >= 60 and t < 500:
        S_t = 10 - (t - 60) / (500 - 60) * 10
    else:
        S_t = 0
    
    
    # data.loc[:, 'TSE_ndl_v0'] = data.loc[:, 'Eta_v0'] / (2 * v0**3 * h0) * ((data_TSE.loc[:, 'vel_flow']) ** 3 + (data_TSE.loc[:, 'vel_ebb']) ** 3) * data.loc[:, 'hprom']
    data.loc[:, 'NREL'] = (data.loc[:, 'S_h']**wi) * (data.loc[:, 'S_TMD']**wi) * (S_m**wi) * (S_d**wi) * (S_t**wi)
    
    data.to_file(PathOutput_01 + FileNameOutput_01 + '_v' + Version + '.GeoJSON', driver='GeoJSON')
    
quit()
