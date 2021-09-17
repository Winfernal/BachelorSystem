# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:55:41 2021

@author: Vegard Hartvigsen Tro

Dette scriptet holder på alle funksjoner som har med matte og statistikk å gjøre. 
"""

import numpy as np



#Transformasjoner--------------------------------------------------------------------
def TranslateSystem(Matrix, Tx, Ty):
    Matrix[0][0] = Matrix[0][0] + Tx
    Matrix[0][1] = Matrix[0][1] + Ty
    
         
def RotateSystem(Matrix, Theta):
         
       to_rad = Theta*(np.pi/180)
       RO_1 = [[np.cos(to_rad), -np.sin(to_rad)], [np.sin(to_rad), np.cos(to_rad)]] #
       rotated_matrix = np.dot(Matrix, RO_1) #gange marvelmind matrise med rotasjonsmatrise
       return rotated_matrix

def RotateAllPoints(x_arr, y_arr, theta):
    new_x_arr = np.array([])
    new_y_arr = np.array([])
    #For å rotere hele systemet så tar jeg en for løkke som går igjennom alle punkter og kjører den i rotasjonsfunksjonen
    for i in range(len(x_arr)):
        new_matrix = [[x_arr[i], y_arr[i]]]
        rotation = RotateSystem(new_matrix, theta) #kjøre roteringsfunksjonen på hver enkelt posisjon i x og y arrays
        
        #appende de roterte punktene i nye x og y arrays
        new_x_arr = np.append(new_x_arr, rotation[0][0])
        new_y_arr = np.append(new_y_arr, rotation[0][1])
    new_matrix =[[new_x_arr, new_y_arr]] #ny matrise består av de to nye arrays
    
    return new_matrix


   
def ScaleSystem(Matrix, Scalefactor):
    scaleFactor = Scalefactor #fra meter til millimeter
  

    Matrix[0][0] = Matrix[0][0]*scaleFactor
    Matrix[0][1] = Matrix[0][1]*scaleFactor
    
    return Matrix



#matematikk-------------------------------------------------------------------- 
def CalcVectorLength(xa, xb, ya,yb):
    distance = np.sqrt((xb-xa)**2+(yb-ya)**2)
    return distance

def CalculateOffset(matrix_1, matrix_2):
    zero_point = matrix_1[0][0][0]
    zero_point_2 = matrix_2[0][0][0]
    
    y_max = np.nanmax(matrix_1[0][1])
    y_max_2 = np.nanmax(matrix_2[0][1]) #ignorerer nan-vedier med nanmax
    
    offset_x = zero_point_2 - zero_point
    offset_y = y_max_2 - y_max
  
    
    return offset_x, offset_y


def FindXYPoints(matrix, p1, p2):
    x_p1 = matrix[0][0][p1]
    x_p2 = matrix[0][0][p2]
    y_p1 = matrix[0][1][p1]
    y_p2 = matrix[0][1][p2]
    
    return x_p1, x_p2, y_p1, y_p2


#statistikk--------------------------------------------------------------------------

#First, the mean may be shifted from the true value. The amount of this shift is called the accuracy of the measurement. 

def CalcMeanAccuracy(x_mean_ref,x_mean_sue, y_mean_ref,y_mean_sue):
    print("Ref X Mean:",x_mean_ref, "SUE X Mean:", x_mean_sue)
    print("Ref Y Mean:", y_mean_ref,"SUE Y Mean:", y_mean_sue)
    print("Difference in X:", np.abs(x_mean_ref - x_mean_sue))
    print("Difference in Y:", np.abs(y_mean_ref - y_mean_sue))
    mean_accuracy = np.sqrt(((x_mean_ref - x_mean_sue)**2)+(y_mean_ref - y_mean_sue)**2)   
    print("Mean Accuracy of System under Evaluation: ", mean_accuracy,"mm")
    return mean_accuracy




def CalcMeanXY(matrix):
    mean_x = np.nanmean(matrix[0][0]) #mean i x
    mean_y = np.nanmean(matrix[0][1]) #mean i y
    return mean_x, mean_y



#-------------------------
    
def CalcErrors(matrix_ref, matrix_sue, N):
    # storage_array = np.array([]) #Liste for alle enkeltmålinger
    storage_array = np.array([])
    for i in range(0,N): #n er antall enkeltmålinger
        errors = np.sqrt(((matrix_ref[0][0][i] - matrix_sue[0][0][i])**2)+(matrix_ref[0][1][i]-matrix_sue[0][1][i])**2) #errors
        
        storage_array = np.append(storage_array, errors) #legger alle avvik av enkeltmålinger i målingslisten
    return storage_array



        
#Second, individual measurements may not agree well with each other, as indicated by the width of the distribution. 
#This is called the precision of the measurement, and is expressed by quoting the standard deviation, the signal-to-noise ratio, or the CV.

    
# measuresList_std = []

# def standardDerivation(xref, xsue, yref, ysue):
#     for i in range (0,n):
#         standardDer =  np.sqrt((((xref[i] - xsue[i])**2)+(yref[i]-ysue[i])**2)/n)
#         print(standardDer)
#     return standardDer




#VINKLER TRASH--------------------------------------------------------------------------
# def FindAngle(matrix, start, end):
#     #finner vinkel på ett koordinatsystemtea
    
#     points = FindXYPoints(matrix, start, end)
#     p1_x = points[0]
#     p2_x = points[1]
#     p1_y = points[2]
#     p2_y = points[3]
    
    # vector_length = CalcVectorLength(p1_x, p2_x, p1_y, p2_y)
    
    # print("vector length", vector_length)
    # div_p1 = p1_x/p2_y
    # div_p2 = p2_x/p1_y
    
    # rad = np.arccos((p1_x * p2_x + p1_y*p2_y)/(np.sqrt(((p1_x)**2)+((p1_y)**2)) *(np.sqrt(((p2_x)**2)+((p2_y)**2)))))
    
    # theta = (rad * 180)/np.pi
    # print("Theta:", theta)
    # return theta
    
# def AngleBetweenTwoVectors(matrixa, matrixb, p1_start, p1_end, p2_start, p2_end):
    
#     p_matrix_a = FindXYPoints(matrixa, p1_start, p1_end)
#     p1_x =  p_matrix_a[0]
#     p2_x =  p_matrix_a[1]
#     p1_y =  p_matrix_a[2]
#     p2_y =  p_matrix_a[3] 
#     print("p1_x: ", p1_x)
#     print("p1_y: ", p1_y)
#     print("p2_x ", p2_x)
#     print("p2_y ", p2_y)
    
    
    
#     dx = p2_x - p1_x
#     dy = p2_y - p1_y 
#     vector_length = CalcVectorLength(p1_x, p2_x, p1_y, p2_y)
#     print(vector_length)
        
#     p_matrix_b = FindXYPoints(matrixb, p2_start, p2_end)
#     p3_x =  p_matrix_b[0]
#     p4_x =  p_matrix_b[1]
#     p3_y =  p_matrix_b[2]
#     p4_y =  p_matrix_b[3] 
#     print("p3_x: ", p3_x)
#     print("p3_y ", p3_y)
#     print("p4_x ", p4_x)
#     print("p4_y: ", p4_y)
    
#     dxx = p3_x - p4_x
#     dyy = p3_y - p4_y
#     vector_length_2 = CalcVectorLength(p3_x, p4_x, p3_y, p4_y)
#     print(vector_length_2)
    
    
#     dot_product = ((dx * dxx) + (dy*dyy))
#     # print(dot_product)
#     multi_lengths = vector_length * vector_length_2
#     # print(multi_lengths)
#     divide = dot_product/multi_lengths
#     # print(divide)
    
#     #angle = arccos [(xa*xb + ya*yb)/(sqr(xa**2+ya**2)*sqr(xb**2+yb**2)]
#     # calc = ((p2_x - p1_x)*(p4_x - p3_x)+(p2_y - p1_y)*(p4_y-p3_y)) / (np.sqrt((p2_x-p1_x)**2)+(p2_y-p1_y)**2)*(np.sqrt(((p4_x-p3_x)**2)+(p4_y-p3_y)**2)) 
#     # dotProduct = 
#     rad = np.arccos(divide)
#     theta = (rad * 180)/np.pi
#     print("Theta:", theta)
#     return theta

# def FindAngle_2(matrix, matrix_1, start, end):
    #finner vinkel på ett koordinatsystem

    # points = FindXYPoints(matrix, start, end)
    # p1_x = points[0]
    # p2_x = points[1]
    # p1_y = points[2]
    # p2_y = points[3]
    
    # points_1 = FindXYPoints(matrix_1, start, end)
    # m1_p1_x = points_1[0]
    # m1_p2_x = points_1[1]
    # m1_p1_y = points_1[2]
    # m1_p2_y = points_1[3]
    
    # print("m1_p1_x: ", m1_p1_x)
    # print("m1_p2_x ", m1_p2_x)
    # print("m1_p1_y: ", m1_p1_y)
    # print("m1_p2_y ", m1_p2_y)
    
    # vector_length = CalcVectorLength(p1_x, p2_x, p1_y, p2_y)
    # vector_length_1 = CalcVectorLength(m1_p1_x, m1_p2_x, m1_p1_y, m1_p2_y)
    # print("vector length", vector_length)
    # print("vector length 1", vector_length_1)
    
    # # div_p1 = p1_x/p2_y
    # # div_p2 = p2_x/p1_y
    
    # divide = vector_length_1/vector_length
    # print(divide)
    # rad = np.cos(vector_length_1/vector_length)
  
    
    # theta = (rad * 180)/np.pi
    # print("Theta:", theta)
    # return theta


    


