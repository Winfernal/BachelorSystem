# -*- coding: utf-8 -*-
"""
Created on Sun May  9 13:40:26 2021

@author: Vegard Hartvigsen Tro



I dette scriptet henter man inn data fra systemer man har tatt punktmålinger på, 
for og så finne en vinkel mellom systemene som man bruker for å kalibrere systemene mot hverandre i Main.
"""



import data_manager
import mathstat_manager as ms
import numpy as np
import matplotlib.pyplot as plt


scaleFactor = 0 

#data importering av punktmålinger
konsept = "OpenCV_Laptop" #Marvelmind, OpenCV_Laptop, OpenCV_Jetson
analysetype = "kalibrering" #Bare kalibrering her


ref_point_data = 0
ref_point_data_1 = 0
sue_point_data = 0 
sue_point_data_1 = 0

if(konsept == "Marvelmind"):
    ref_point_data = data_manager.Dataset("mm_"+analysetype+"_qs", "tsv", konsept, analysetype)
    ref_point_data_1 = data_manager.Dataset("mm_"+analysetype+"_qs_1", "tsv", konsept, analysetype)
    sue_point_data = data_manager.Dataset("mm_"+analysetype, "csv", konsept, analysetype)
    sue_point_data_1 = data_manager.Dataset("mm_"+analysetype+"_1", "csv", konsept, analysetype)
    scaleFactor = 1000
elif(konsept == "OpenCV_Jetson"):
    ref_point_data = data_manager.Dataset("qs_jetson_"+analysetype, "tsv", konsept, analysetype)
    ref_point_data_1 = data_manager.Dataset("qs_jetson_"+analysetype+"_1","tsv", konsept, analysetype)
    sue_point_data = data_manager.Dataset("jetson_"+analysetype, "csv", konsept, analysetype)
    sue_point_data_1 = data_manager.Dataset("jetson_"+analysetype+"_1", "csv", konsept, analysetype)
    scaleFactor = 10
elif(konsept == "OpenCV_Laptop"):
    ref_point_data = data_manager.Dataset("qs_laptop_"+analysetype, "tsv", konsept, analysetype)
    ref_point_data_1 = data_manager.Dataset("qs_laptop_"+analysetype+"_1", "tsv", konsept, analysetype)
    sue_point_data = data_manager.Dataset("laptop_"+analysetype, "csv", konsept, analysetype)
    sue_point_data_1 = data_manager.Dataset("laptop_"+analysetype+"_1", "csv", konsept, analysetype)
    scaleFactor = 10





#For kalibrering av koordinatsystemer
ref_point_1, ref_point_2 = [[ref_point_data.X_arr, ref_point_data.Y_arr]],[[ref_point_data_1.X_arr, ref_point_data_1.Y_arr]]
sue_point_1, sue_point_2 = [[sue_point_data.X_arr, sue_point_data.Y_arr]], [[sue_point_data_1.X_arr, sue_point_data_1.Y_arr]]


#skalering av punktdata; mm = 1000, jetson = 10, opencv = 10
sue_point_1, sue_point_2  = ms.ScaleSystem(sue_point_1, scaleFactor), ms.ScaleSystem(sue_point_2, scaleFactor)

#mean av alle punktmålingene
ref_p1_mean = ms.CalcMeanXY(ref_point_1)
ref_p2_mean = ms.CalcMeanXY((ref_point_2))

sue_p1_mean = ms.CalcMeanXY(sue_point_1)
sue_p2_mean = ms.CalcMeanXY(sue_point_2)


def CalibrationAngle3(sue_p1x, sue_p1y, sue_p2x, sue_p2y): #Finner en kalibreringsvinkel mellom ref og sue basert på pythagoras teorem
    #qualisys
    qs_vector = ms.CalcVectorLength(ref_p1_mean[0], ref_p2_mean[0], ref_p1_mean[1], ref_p2_mean[1])
    qs_dx = ref_p2_mean[0] - ref_p1_mean[0]
  
    angle_qs = np.arccos(qs_dx/qs_vector)
    theta_qs = (angle_qs * 180)/np.pi
    print("Theta Ref:", theta_qs)
    
    sue_vector = ms.CalcVectorLength(sue_p1x, sue_p2x, sue_p1y, sue_p2y)
    sue_dx = sue_p2x - sue_p1x
  
    angle_sue = np.arccos(sue_dx/sue_vector)    
    theta_sue = (angle_sue * 180)/np.pi
    print("Theta Sue:", theta_sue)
    
    angle_sum = theta_qs - theta_sue 
    print("Kalibreringsvinkel:", angle_sum, "grader")
     
    return angle_sum

    
    
def GetAngle():
  angle = CalibrationAngle3(sue_p1_mean[0], sue_p1_mean[1], sue_p2_mean[0], sue_p2_mean[1]) 
  
  return angle

angle = GetAngle()

# GetAngle()

# ref_plot1 = plt.scatter(ref_p1_mean[0], ref_p1_mean[1], marker = '*')
# ref_plot2 = plt.scatter(ref_p2_mean[0], ref_p2_mean[1], marker = '1')


# sue_plot1 = plt.scatter(sue_p1_mean[0], sue_p1_mean[1], marker = '+')
# sue_plot2 = plt.scatter(sue_p2_mean[0], sue_p2_mean[1], marker = '+')


# plt.legend([ref_plot1, ref_plot2, sue_plot1, sue_plot2], ['ref_plot1', 'ref_plot2', 'sue_plot1', 'sue_plot2', ''])


# plt.axis('equal')


















#------------------------------------------------------------------------------trash
#regne ut vinkel

# def CalibrationAngle(ref_p1x, ref_p1y, ref_p2x, ref_p2y, sue_p2x, sue_p2y):
    
#     vector_length_ref_p1p2 = ms.CalcVectorLength(ref_p1x, ref_p2x, ref_p1y, ref_p2y)
#     vector_length_sue_p1suep2 = ms.CalcVectorLength(ref_p1x, sue_p2x, ref_p1y, sue_p2y)
#     vector_length_sue_p2qs3sue = ms.CalcVectorLength(ref_p2x, sue_p2x, ref_p2y, sue_p2y)
    
#     # print(vector_length_ref_p1p2, vector_length_sue_p1suep2, vector_length_sue_p2qs3sue)
#     dot_product = (ref_p2x * sue_p2x  + ref_p2y*sue_p2y)
#     # print(dot_product)
#     multi_lengths = vector_length_ref_p1p2 * vector_length_sue_p1suep2
    
#     divide = dot_product/multi_lengths
#     print(divide)

#     rad = np.arccos(divide) 
 
#     theta = (rad * 180)/np.pi
#     # print("Angle is: ", theta)
#     angle = 180-theta
#     # print("Calibration angle is:", angle)

#     return angle

# def CalibrationAngle2(ref_p2x, ref_p2y, sue_p1x, sue_p1y, sue_p2x, sue_p2y):
    
#     # vector_length_ref_p1p2 = ms.CalcVectorLength(ref_p1x, ref_p2x, ref_p1y, ref_p2y)
    
    
    
    
#     c = ms.CalcVectorLength(ref_p2x, sue_p2x, ref_p2y, sue_p2y)
#     b = ms.CalcVectorLength(sue_p1x, sue_p2x, sue_p1y, sue_p2y)
#     a = ms.CalcVectorLength(ref_p2x, sue_p1x, ref_p2y, sue_p1y)
    
#     print(a, b, c)
  
#     sum = ((b)**2+(c)**2-(a)**2)
#     divide = sum/(2*(b*c))
#     rad = np.arccos(divide)
 
#     theta = (rad * 180)/np.pi
#     print("Angle is: ", theta)
#     angle = 180-theta
#     print("Calibration angle is:", angle)

#     return angle




