# -*- coding: utf-8 -*-
"""
Created on Fri May  7 12:57:56 2021

@author: Vegard Hartvigsen Tro



Script som har som formål å sammenligne flere posisjoneringssystemer opp mot hverandre.

Når begrepet SUE nevnes her, menes (System under Evaluering) og Ref er referansesystem.

#TODO----------
#P95, 95% confidence interval måling, lese lese
#regne ut skaleringsfaktor?     
#Matematisk regne ut kontinuerlig offset og rotasjon dersom mobile beacons ikke ligger oppå hverandre
"""

#Imports
import data_manager
import mathstat_manager as ms
import calibration as cal
import matplotlib.pyplot as plt
import numpy as np



# Importere posisjoneringsdata via Pandas og data_manager.py scriptet og gjøre de til matriser
konsept = "OpenCV_Laptop" #Marvelmind, OpenCV_Laptop, OpenCV_Jetson
analysetype = "runde" #punkter, runde, stille

sue_data = 0
ref_data = 0
scaleFactor = 1000


if(konsept == "Marvelmind"):    
    sue_data = data_manager.Dataset("mm_"+analysetype, "csv", konsept, analysetype)
    ref_data = data_manager.Dataset("qs_mm_"+analysetype, "tsv", konsept, analysetype)
    scaleFactor = 1000
elif(konsept == "OpenCV_Jetson"):
    sue_data = data_manager.Dataset("jetson_"+analysetype, "csv", konsept, analysetype)
    ref_data = data_manager.Dataset("qs_jetson_"+analysetype, "tsv", konsept, analysetype)
    scaleFactor = 10
elif(konsept == "OpenCV_Laptop"):
    sue_data = data_manager.Dataset("laptop_"+analysetype, "csv", konsept, analysetype)
    ref_data = data_manager.Dataset("qs_laptop_"+analysetype, "tsv", konsept, analysetype)
    scaleFactor = 10



# Timestamp matching
sue_timed_array_x = []
sue_timed_array_y = []
for i in range(0, len(sue_data.X_arr)):
    ref_timestamp = ref_data.Timestamp_arr[0]
    sue_timestamp = sue_data.Timestamp_arr[i]
    
    
    if(sue_timestamp > ref_timestamp):
        sue_timed_array_x = np.append(sue_timed_array_x, sue_data.X_arr[i])
        sue_timed_array_y = np.append(sue_timed_array_y, sue_data.Y_arr[i])
      
  
sue_matrix = [[sue_timed_array_x, sue_timed_array_y]]
ref_matrix = [[ref_data.X_arr, ref_data.Y_arr]]
print(konsept, "Measurements:", len(sue_matrix[0][0]))
print("Ref Measurements:", len(ref_matrix[0][0]))


#Data transformasjon-----------------------------------------------------
#skalerer systemet
sue_matrix = ms.ScaleSystem(sue_matrix, scaleFactor)

#rotering av koordinatsystem
#offset/translasjon
angle = cal.GetAngle()
#legge forskjellen vinkel inn i roteringsfunksjonen slik at de har lik vinkel
if(konsept == "Marvelmind"):
    angle = -angle
    
sue_matrix = ms.RotateAllPoints(np.array(sue_matrix[0][0]), np.array(sue_matrix[0][1]),angle)

offset = ms.CalculateOffset(sue_matrix, ref_matrix)

ms.TranslateSystem(sue_matrix,offset[0], offset[1]) #setter inn x offset og y offset i translasjons funksjonen


#statistikk--------------------------------------------------------------------
#finner presisjon ved å sammenligne begge systemer
#regner først ut mean på x og y verdier på referanse system og SUE (system under evaluation)
sue_mean = ms.CalcMeanXY(sue_matrix)
ref_mean = ms.CalcMeanXY(ref_matrix)

#regner ut nøyaktighet 
mean_accuracy = ms.CalcMeanAccuracy(ref_mean[0], sue_mean[0], ref_mean[1], sue_mean[1])
# derivations = s 

#plotting------------------------------------------------------------------------
sue_plot = plt.scatter(sue_matrix[0][0], sue_matrix[0][1])
reference_plot = plt.scatter(ref_matrix[0][0], ref_matrix[0][1])
#
plt.legend([reference_plot, sue_plot], ['Qualisys', konsept])
plt.axis('equal')