# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 10:45:57 2021

@author: Vegard Hartvigsen Tro
"""

#vinkler via punktmåling
#punktmålinger på 3-4 punkter
#nullpunkt på marvelmind å qualisys må være på akkurat samme plass

#regne ut rotasjon
        #har matriseregningen, men hvordan finne vinkel?

#regne ut translasjon(offset)
        #har matriseregningen, men hvordan finne offset?

#test

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


    
    
qualisys_data = pd.read_csv(r'E:/Punktmåling_1_Qualisys_6D.tsv', delimiter='\t')
qualisys_data_2 = pd.read_csv(r'E:/Punktmåling_2_Qualisys_6D.tsv', delimiter='\t')
qualisys_data_3 = pd.read_csv(r'E:/Punktmåling_3_Qualisys_6D.tsv', delimiter='\t')
qualisys_data_4 = pd.read_csv(r'E:/Punktmåling_4_Qualisys_6D.tsv', delimiter='\t')



marvelmind_data = pd.read_csv(r'E:/Punktmåling_1_Marvelmind.csv', delimiter=';')
marvelmind_data_2 = pd.read_csv(r'E:/Punktmåling_2_Marvelmind.csv', delimiter=';')
marvelmind_data_3 = pd.read_csv(r'E:/Punktmåling_3_Marvelmind.csv', delimiter=';')
marvelmind_data_4 = pd.read_csv(r'E:/Punktmåling_4_Marvelmind.csv', delimiter=';')



#-----------------------variabler og formler--------------------------------
n = 10

#Qualisys Data
qs_x, qs_y = qualisys_data.X, qualisys_data.Y  
qs_x2, qs_y2 = qualisys_data_2.X, qualisys_data_2.Y 
qs_x3, qs_y3 = qualisys_data_3.X, qualisys_data_3.Y 
qs_x4, qs_y4 = qualisys_data_4.X, qualisys_data_4.Y 

#marvelmind Data
mm_x, mm_y = marvelmind_data.X, marvelmind_data.Y 
mm_x2, mm_y2 = marvelmind_data_2.X, marvelmind_data_2.Y  
mm_x3, mm_y3 = marvelmind_data_3.X, marvelmind_data_3.Y 
mm_x4, mm_y4 = marvelmind_data_4.X, marvelmind_data_4.Y  

#OpenCV Data
#opencv_x, opencv_y = opencv_data.X, opencv_data.Y


# def importData(timestamp, x, y):
#     qs_x,q_y,timestamp = qualisys_data.X, qualisys_data.Y, qualisys_data.timestamp
    
#matematikk 

        

def calcDistance(xa, xb, ya,yb):
    distance = np.sqrt((xb-xa)**2+(yb-ya)**2)
    return distance


#statistikk

def calcMeanAccuracy(x_mean_ref,x_mean_sue, y_mean_ref,y_mean_sue):
    mean = np.sqrt(((x_mean_ref - x_mean_sue)**2)+(y_mean_ref - y_mean_sue)**2)    
    return mean

# measuresList_std = []

def standardDerivation(xref, xsue, yref, ysue):
    for i in range (0,n):
        standardDer =  np.sqrt((((xref[i] - xsue[i])**2)+(yref[i]-ysue[i])**2)/n)
        print(standardDer)
    return standardDer

#system transformasjoner

def TranslateSystem(Matrix, Tx, Ty):
    offset_matrix = [Tx,Ty]
    Matrix = Matrix + offset_matrix
    return Matrix

def RotateSystem(Matrix, Theta):

    to_rad = Theta*(np.pi/180)
    RO_1 = [[np.cos(to_rad), -np.sin(to_rad)], [np.sin(to_rad), np.cos(to_rad)]] #rotasjonsmatrise
    rotated_matrix = np.dot(Matrix, RO_1) #gange marvelmind matrise med rotasjonsmatrise
    return rotated_matrix

def ScaleSystem(Matrix, Scalefactor):
    scaleFactor = Scalefactor #fra meter til millimeter
    for i in range(0, len(Matrix)):
        Matrix[i][0] = Matrix[i][0]*scaleFactor
        Matrix[i][1] = Matrix[i][1]*scaleFactor



#regner ut mean på alle målinger

qs_mean_x, qs_mean_y = np.mean(qs_x), np.mean(qs_y) 
qs_mean_x2, qs_mean_y2 = np.mean(qs_x2), np.mean(qs_y2) 
qs_mean_x3, qs_mean_y3 = np.mean(qs_x3), np.mean(qs_y3)
qs_mean_x4, qs_mean_y4 = np.mean(qs_x4), np.mean(qs_y4)

mm_mean_x, mm_mean_y = np.mean(mm_x), np.mean(mm_y)
mm_mean_x2, mm_mean_y2 = np.mean(mm_x2), np.mean(mm_y2)
mm_mean_x3, mm_mean_y3 = np.mean(mm_x3), np.mean(mm_y3)
mm_mean_x4, mm_mean_y4 = np.mean(mm_x4), np.mean(mm_y4)





# print(qs_mean_x, qs_mean_y)
# print(qs_mean_x2,qs_mean_y2)
# print(qs_mean_x3, qs_mean_y3)
# print(qs_mean_x4, qs_mean_y3)

# print("---------")

# print(mm_mean_x, mm_mean_y)
# print(mm_mean_x2, mm_mean_y2)
# print(mm_mean_x3, mm_mean_y3)
# print(mm_mean_x4, mm_mean_y4)


#distanse mellom punktmålinger

qs_dist = calcDistance(qs_mean_x, qs_mean_x2, qs_mean_y, qs_mean_y2)
qs_dist_2_3 = calcDistance(qs_mean_x2, qs_mean_x3, qs_mean_y2, qs_mean_y3)
qs_dist_3_4 = calcDistance(qs_mean_x3, qs_mean_x4, qs_mean_y3, qs_mean_y4)
qs_dist_4_1 = calcDistance(qs_mean_x4, qs_mean_x, qs_mean_y4, qs_mean_y)
qs_dist_1_3 = calcDistance(qs_mean_x, qs_mean_x3, qs_mean_y, qs_mean_y3)

mm_dist = calcDistance(mm_mean_x, mm_mean_x2, mm_mean_y, mm_mean_y2)
mm_dist_2_3 = calcDistance(mm_mean_x2, mm_mean_x3, mm_mean_y2, mm_mean_y3)
mm_dist_3_4 = calcDistance(mm_mean_x3, mm_mean_x4, mm_mean_y3, mm_mean_y4)
mm_dist_4_1 = calcDistance(mm_mean_x4, mm_mean_x, mm_mean_y4, mm_mean_y)
mm_dist_1_3 = calcDistance(mm_mean_x, mm_mean_x3, mm_mean_y, mm_mean_y3)




print("Distanse(marvelmind 1 til 2):", mm_dist * 1000)
print("Distanse(marvelmind 2 til 3):", mm_dist_2_3 * 1000)
print("Distanse(marvelmind 3 til 4):", mm_dist_3_4 * 1000)
print("Distanse(marvelmind 4 til 1):", mm_dist_4_1 * 1000)
print("Distanse(Marvelmind 1 til 3):", mm_dist_1_3 * 1000)

print("Distanse(Qualisys 1 til 2:) ", qs_dist)
print("Distanse(Qualisys 2 til 3: ", qs_dist_2_3)
print("Distanse(Qualisys 3 til 4: ", qs_dist_3_4)
print("Distanse(Qualisys 4 til 1: ", qs_dist_4_1)
print("Distanse(Qualisys 1 til 3: )", qs_dist_1_3)




#Koordinatmatriser
# matrix_marvelmind = [[mm_mean_x,mm_mean_y], 
#           [mm_mean_x2,mm_mean_y2],
#             [mm_mean_x3,mm_mean_y3],
#           [mm_mean_x4,mm_mean_y4]]

matrix_marvelmind = [[mm_x[1],mm_y[1]], #på plass 1 for å unngå feil i data, TODO fix
          [mm_x2[1],mm_y2[1]],
            [mm_x3[1],mm_y3[1]],
          [mm_x4[1],mm_y4[1]]]

# matrix_qualisys = [[qs_mean_x,qs_mean_y], 
#           [qs_mean_x2,qs_mean_y2],
#           [qs_mean_x3,qs_mean_y3],
#           [qs_mean_x4,qs_mean_y4]]


matrix_marvelmind_test = [[mm_x[1],mm_y[1]]]

matrix_qualisys = [[qs_x[1],qs_y[1]], #på plass 1 for å unngå feil i data, TODO fix
          [qs_x2[1],qs_y2[1]],
          [qs_x3[1],qs_y3[1]],
          [qs_x4[1],qs_y4[1]]]



#Tranformasjon av koordinatsystemer
# print(matrix_marvelmind)
#Skalering
ScaleSystem(matrix_marvelmind, 1000)

#offset utregning
matrix_marvelmind = TranslateSystem(matrix_marvelmind, 0, 0)
# print(matrix_marvelmind)
print(matrix_marvelmind_test)
#Rotasjon av koordinatsystem
matrix_marvelmind_test = RotateSystem(matrix_marvelmind_test, 45)



print(matrix_marvelmind_test)


# print(matrix_marvelmind)

#regne  ut standardavvik og mean

measuresList = np.array([]) #Liste for alle enkeltmålinger
framelist = np.array([]) 


for i in range(0,n): #n er antall enkeltmålinger
    errors = np.sqrt(((qs_x2[i] - mm_x2[i])**2)+(qs_y2[i]-mm_y2[i])**2) #errors
    # print(errors)
    measuresList = np.append(measuresList, errors) #legger alle avvik av enkeltmålinger i målingslisten
    framelist = np.append(framelist, qualisys_data.Frame[i])
    

    
std = np.std(measuresList) #standardavvik på alle målinger
# measuresMean = np.mean(measuresList) #regner ut mean fra alle målinger



#plotting

# plt.hist(measuresList)

# qs_plot_1 = plt.scatter(matrix_qualisys[0][0], matrix_qualisys[0][1])
# qs_plot_2 = plt.scatter(matrix_qualisys[1][0], matrix_qualisys[1][1])
# qs_plot_3 = plt.scatter(matrix_qualisys[2][0], matrix_qualisys[2][1])
# qs_plot_4 = plt.scatter(matrix_qualisys[3][0], matrix_qualisys[3][1])

# mm_plot_1 = plt.scatter(matrix_marvelmind[0][0], matrix_marvelmind[0][1], marker = "*")
# mm_plot_2 = plt.scatter(matrix_marvelmind[1][0], matrix_marvelmind[1][1], marker = "*")
# mm_plot_3 = plt.scatter(matrix_marvelmind[2][0], matrix_marvelmind[2][1], marker = "*")
# mm_plot_4 = plt.scatter(matrix_marvelmind[3][0], matrix_marvelmind[3][1], marker = "*")

# zero = plt.scatter(0,0)

# plt.legend([qs_plot_1, qs_plot_2, qs_plot_3, qs_plot_4, mm_plot_1, mm_plot_2, mm_plot_3, mm_plot_4], ['Qualisys 1', 'Qualisys 2', 'Qualisys 3', 'Qualisys 4', 'Marvelmind 1', 'Marvelmind 2', 'Marvelmind 3', 'Marvelmind 4'])
plt.axis('equal')
# plt.show()

