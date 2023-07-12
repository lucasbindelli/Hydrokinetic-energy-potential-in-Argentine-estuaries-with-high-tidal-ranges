# -*- coding: utf-8 -*-
import json
from netCDF4 import Dataset
import numpy as np

# Parametros ------------------------------------------------------------
fileName = "trim-Rank3.nc"

with Dataset(fileName, mode='r') as ds:
    xcor = ds.variables['XCOR'][:]
    ycor = ds.variables['YCOR'][:]

    xcc = ds.variables['XZ'][:]
    ycc = ds.variables['YZ'][:]
    m, n = xcor.shape

    alfas = ds.variables['ALFAS'][:]
    print(m, n)

    g = ds.variables['GRAVITY'][0]
    print(g)

    times = ds.variables['time'][:]
    print(times)

    baticc = ds.variables['DPS0'][:]

    puntos = []
    for i in range(n):
        for j in range(m):
            x, y = xcor[j, i], ycor[j, i]
            if x > 0 and y > 0:
                puntos.append((x, y))

    s1 = ds.variables['S1']
    u1 = ds.variables['U1']
    v1 = ds.variables['V1']

    # energiaxm = np.zeros(shape=(m, n))
    # energiaxm2 = np.zeros(shape=(m, n))
    velprom = np.zeros(shape=(m, n))
    # hprom = np.zeros(shape=(m, n))
    # hmin = np.zeros(shape=(m, n))
    velumbral = np.zeros(shape=(m, n))
    velmax = np.zeros(shape=(m, n))
    # energiaxm2xyr = np.zeros(shape=(m, n))
    potenciamed = np.zeros(shape=(m, n))
    potenciamax = np.zeros(shape=(m, n))
    # hmax = np.zeros(shape=(m, n))

    # for i in range(0, m):
        # for j in range(0, n):
            # hmin[i, j] = 1000

    for k in range(len(times)):
        text = "Procesando %d / %d, %.2f%%" % (k + 1, len(times), 100 * float(k + 1) / len(times))
        print(text)

        # Interpolar la velocidad al centro de celda
        ucc = (u1[k][0][:-1, :-1] + u1[k][0][1:, 1:]) / 2
        vcc = (v1[k][0][:-1, :-1] + v1[k][0][1:, 1:]) / 2
        velcc = (ucc**2 + vcc**2)**0.5
        velcc2 = np.ndarray(shape=(m, n))
        velcc2[1:, 1:] = velcc

        # Eliminar las velocidades menores a 1 m/s
        velcc[(velcc < 0.7) | (velcc > 3.1)] = 0.0

        # # Tirante
        # hcc = (s1[k][1:, 1:] + baticc[1:, 1:])
        # hcc2 = np.ndarray(shape=(m, n))
        # hcc2[1:, 1:] = hcc

        # # Caudal especifico
        # qcc = hcc * velcc
        # qcc2 = np.ndarray(shape=(m, n))
        # qcc2[1:, 1:] = qcc

        # Potencia
        Cp = 1
        potencia = Cp * 0.5 * 1024 * velcc**3
        potencia2 = np.ndarray(shape=(m, n))
        potencia2[1:, 1:] = potencia

        # hmin = np.minimum(hmin, hcc2)
        velmax = np.maximum(velmax, velcc2)
        velumbral[velcc2 > 1.0] += 1.0
        # Potencia en W
        potenciamax = np.maximum(potenciamax, potencia2)
        # hmax = np.maximum(hmax, hcc2)

        if k == 0 or k == len(times) - 1:
            # energiaxm2 += potencia2
            # energiaxm += potencia2 * hcc2
            velprom += velcc2
            # hprom += hcc2
            potenciamed += potencia2
        else:
            # energiaxm2 += 2 * potencia2
            # energiaxm += 2 * potencia2 * hcc2
            velprom += 2 * velcc2
            # hprom += 2 * hcc2
            potenciamed += 2 * potencia2

    # Energía en KWh/año/m
    # energiaxm2 *= 0.5 * (times[1] - times[0]) / 1000 / 3600
    # energiaxm *= 0.5 * (times[1] - times[0]) / 1000 / 3600
    velprom *= 0.5 * (times[1] - times[0]) / (times[-1] - times[0])
    # hprom *= 0.5 * (times[1] - times[0]) / (times[-1] - times[0])
    velumbral *= 1.0 / len(times)
    # energiaxm2xyr = energiaxm2 * 365.25 / 90
    potenciamed *= 0.5 * (times[1] - times[0]) / (times[-1] - times[0]) #/ 1000

    collection = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}},
        "features": []
    }
    for i in range(1, m):
        for j in range(1, n):
            x1, y1 = xcor[i - 1, j - 1], ycor[i - 1, j - 1]
            x2, y2 = xcor[i + 0, j - 1], ycor[i + 0, j - 1]
            x3, y3 = xcor[i + 0, j + 0], ycor[i + 0, j + 0]
            x4, y4 = xcor[i - 1, j + 0], ycor[i - 1, j + 0]

            xc, yc = xcc[i + 0, j + 0], ycc[i + 0, j + 0]
            # print(x1, y1)
            if x1 == 0 or y1 == 0:
                continue
            if x2 == 0 or y2 == 0:
                continue
            if x3 == 0 or y3 == 0:
                continue
            if x4 == 0 or y4 == 0:
                continue
            if xc <= -400 or yc <= -400:
                continue
            if x1 <= -400 or y1 <= -400:
                continue
            if x2 <= -400 or y2 <= -400:
                continue
            if x3 <= -400 or y3 <= -400:
                continue
            if x4 <= -400 or y4 <= -400:
                continue
            feature = {
                "type": "Feature",
                "properties": {
                    # "energiaxm2": float(energiaxm2[i, j]),
                    # "energiaxm": float(energiaxm2[i, j]),
                    "velprom": float(velprom[i, j]),
                    "velumbr": float(velumbral[i, j]),
                    "velmax": float(velmax[i, j]),
                    # "hmin": float(hmin[i, j]),
                    # "hprom": float(hprom[i, j]),
                    "m": int(i + 1),
                    "n": int(j + 1),
                    # "energiaxm2xyr": float(energiaxm2xyr[i, j]),
                    "potenciamax": float(potenciamax[i, j]),
                    "potenciamed": float(potenciamed[i, j]),
                    # "hmax": float(hmax[i, j])
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[float(x1), float(y1), ], [float(x2), float(y2), ], [float(x3), float(y3), ], [float(x4), float(y4), ]]]
                }
            }
            # print(feature)
            collection["features"].append(feature)
    with open("Potencias-IHE.GeoJSON", "w") as f:
        json.dump(collection, f)
