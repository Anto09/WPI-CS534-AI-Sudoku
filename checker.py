#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  4 13:20:20 2014

@author: anto
"""
import matplotlib.pyplot as plt
import numpy as np
import sys

A = []
row_checker = []
col_checker = []
box_checker = []
side = 0
square_dim = 0
row_conflicts = 0
col_conflicts = 0
box_conflicts = 0
total_conflicts = 0
    
def printMatrix():
    print A, '\n'
    
def checkConfiguration():
    row_conflicts = 0
    col_conflicts = 0
    box_conflicts = 0
    total_conflicts = 0    
    
    for i in range(0,side):
        row_checker = np.zeros(side)
        col_checker = np.zeros(side)
        for j in range(0,side):
            if (A[i,j]==-1):
                continue
            if (row_checker[A[i,j]-1] == 1):
                row_conflicts += 1
            else:
                row_checker[A[i,j]-1] = 1                
            if (col_checker[A[j,i]-1] == 1):
                col_conflicts += 1
            else:
                col_checker[A[j,i]-1] = 1
    
        
    for j in range (0,side,int(square_dim)):    
        for i in range (0,side,int(square_dim)):
            box_checker = np.zeros(side)  
            for x in range (i,i+int(square_dim)):
                for y in range (j,j+int(square_dim)):
                    if (A[x,y] == -1):
                        continue
                    if (box_checker[A[x,y]-1] == 1):
                        box_conflicts += 1;
                    else: 
                        box_checker[A[x,y]-1] = 1
        
    total_conflicts = row_conflicts + col_conflicts + box_conflicts
    print row_conflicts,' ',col_conflicts,' ',box_conflicts,' ',total_conflicts
    return total_conflicts
    
options = {
    'P\n' : printMatrix,
    'C\n' : checkConfiguration,
 }
    #this is the main function where this script begins to execute
if __name__ == "__main__":
    plt.ion() # enables interactive plotting mode
    filename = sys.argv[-1]
    A = np.genfromtxt(filename, delimiter=',', dtype=int)
    side = A.shape[0]
    square_dim = np.sqrt(side)
     
    b = '';
    while (b != 'E\n'):    
        print 'Type a command.'
        print 'P to print initial Sudoku Board'
        print 'C to check for conflicts'
        print 'E to Exit'
        b =  sys.stdin.readline()
        if (b == 'P\n' or b == 'C\n'):
            options[b]()
        elif (b != 'E\n'):
            print 'Invalid Command\n'