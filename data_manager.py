# -*- coding: utf-8 -*-
"""
Created on Fri May  7 12:59:04 2021

@author: Vegard Hartvigsen Tro

Dette scriptet behandler data som kommer inn i form av csv eller tsv filer. 
Bruker pandas for å importere og behandle data i en Dataset klasse.

"""
import pandas as pd
import numpy as np

class Dataset():
    
    def __init__(self, filename, filetype, konsept, analysetype): 
        
        self.filename = filename
        self.filetype = filetype
        self.konsept = konsept
        self.analysetype = analysetype
        self.X_arr = []
        self.Y_arr = []    
        self.ID_arr = []
        self.Timestamp_arr = []
        

        if(self.filetype == 'csv'):
            dataset = pd.read_csv(r'Analyser/'+ self.konsept+ '/'+self.analysetype + '/' + self.filename+'.'+self.filetype, delimiter = ';')
     
        if(self.filetype == 'tsv'):
            dataset = pd.read_csv(r'Analyser/'+ self.konsept+ '/'+self.analysetype + '/' + self.filename+'.'+self.filetype, delimiter = '\t')
            
        for i in range(0,len(dataset)):
            if(self.filetype == 'csv'):  
                id_important = dataset.ID[i] #Tar bare data fra mobilt beacon, som har ID 120
                if id_important == 120:      
                    self.ID_arr = np.append(self.ID_arr, dataset.ID[i])
                    self.X_arr = np.append(self.X_arr, dataset.X[i])
                    self.Y_arr = np.append(self.Y_arr, dataset.Y[i])
                    self.Timestamp_arr = np.append(self.Timestamp_arr, dataset.Timestamp[i])
            else:
                self.X_arr = np.append(self.X_arr, dataset.X[i])
                self.Y_arr = np.append(self.Y_arr, dataset.Y[i])
                self.Timestamp_arr = np.append(self.Timestamp_arr, dataset.Timestamp[i])
                
        

    