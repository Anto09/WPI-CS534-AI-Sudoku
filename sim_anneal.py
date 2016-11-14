# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 21:46:21 2014

@author: anto
"""

#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import copy

A = []
column_lists = []
side = 0
square_dim = 0
    
def printMatrix():
    print A, '\n'
    
def checkConfiguration(board):
    row_conflicts = 0
    col_conflicts = 0
    box_conflicts = 0
    total_conflicts = 0    
    
    for i in range(0,side):
        row_checker = np.zeros(side)
        col_checker = np.zeros(side)
        for j in range(0,side):
            if (board[i,j]==-1):
                continue
            if (row_checker[board[i,j]-1] == 1):
                row_conflicts += 1
            else:
                row_checker[board[i,j]-1] = 1                
            if (col_checker[board[j,i]-1] == 1):
                col_conflicts += 1
            else:
                col_checker[board[j,i]-1] = 1
    
        
    for j in range (0,side,int(square_dim)):    
        for i in range (0,side,int(square_dim)):
            box_checker = np.zeros(side)  
            for x in range (i,i+int(square_dim)):
                for y in range (j,j+int(square_dim)):
                    if (board[x,y] == -1):
                        continue
                    if (box_checker[board[x,y]-1] == 1):
                        box_conflicts += 1;
                    else: 
                        box_checker[board[x,y]-1] = 1
        
    total_conflicts = row_conflicts + col_conflicts + box_conflicts
    return total_conflicts

def checkMissing(state):
    row_missing = 0
    box_missing = 0
    
    for i in range(0,side):
        row_check = np.zeros(side)
        r_m = -side
        for j in range (0,side):  
            if (row_check[state[i,j]-1] != 0):
                r_m+=1
            else:
                row_check[state[i,j]-1] = 1
        row_missing += r_m
        
    for j in range (0,side,int(square_dim)):    
        for i in range (0,side,int(square_dim)):
            box_check = np.zeros(side)
            b_m = -side
            for x in range (i,i+int(square_dim)):
                for y in range (j,j+int(square_dim)):            
                    if (box_check[state[x,y]-1] != 0):
                        b_m+=1
                    else:
                        box_check[state[x,y]-1] = 1
            box_missing += b_m
    return row_missing + box_missing
    
    
def solveColumns(state):
    for i in range(0,side):
        temp_list = copy.deepcopy(column_lists[i])
        for j in range(0,side):
            if (state.item(j,i)==-1):
                r = np.random.randint(0,len(temp_list))
                state[j,i] = temp_list.pop(r)+1
    return
    
def swapItems(state):
    randCol1 = np.random.randint(0,side)
    randColList1 = copy.deepcopy(column_lists[randCol1])
    
    if (len(randColList1) > 0):
        randRow1 = randColList1.pop(np.random.randint(0,len(randColList1)))
        if (len(randColList1) > 0):
            randRow2 = randColList1.pop(np.random.randint(0,len(randColList1)))    
            
            tempItem1 = state.item(randRow1,randCol1)    
            tempItem2 = state.item(randRow2,randCol1)    
                
            state[randRow2,randCol1] = tempItem1
            state[randRow1,randCol1] = tempItem2       
    
temp = 0.
t_max = 300.
cur_time = 0.
energy = 0.

def Energy(state):    
    return checkMissing(state)
    
def Neighbour(state):
    swapped = copy.deepcopy(state)
    swapItems(swapped)
    return swapped
    
def Prob(cur_energy, new_energy, temp): 
    negDiff = np.exp((cur_energy - new_energy)/temp)
    randomSamp = np.random.random_sample()
    #print negDiff,' ',randomSamp
    
    return negDiff > randomSamp 
        
def simulatedAnnealing():
    
    global A
    global cur_time
    global temp
    global t_max    
    
    state = copy.copy(A)
    solveColumns(state)
    s_best = copy.copy(state)
    energy = Energy(s_best);    
    e_best = np.inf;    
    e_prevBest = 0
    temp = 0.5
    cur_time = 0.
    count = 0
  
    while (cur_time<t_max): #and energy > e_max):            
        if (energy == -(side**2)*2):
            break
        
        start_time = time.time()
        s_new = Neighbour(state)
        e_new = Energy(s_new)
        
        if (e_new == -(side**2)*2):
            if (checkConfiguration(s_new) == 0):
                e_best = e_new
                state = s_new
                s_best = copy.deepcopy(state)
                break;
        
        if (Prob(float(energy), float(e_new), temp)):
            state = s_new
            energy = e_new
        
        if (energy < e_best):
            e_prevBest = energy
            e_best = energy
            s_best = copy.copy(state)
    
        if (count%50000 == 0):
            if (np.absolute(e_best - e_prevBest) <= 1):
                state = copy.copy(A)
                solveColumns(state)

            '''
            print 'Iteration: ',count
            print 'Current board: '
            print state
            print 'Current score: ',energy            
            '''

        temp = temp * 0.99999999
        count += 1
        cur_time = cur_time + (time.time() - start_time)
    
    if (checkConfiguration(s_best) == 0):
        print 'Final board: ',
        print s_best
        print 'Final score: ',e_best
    else:
        print 'Solution not found'
    print 'Runtime: ',cur_time
    
    return s_best
    
options = {
    'P\n' : printMatrix,
    'S\n' : simulatedAnnealing,
 }
#this is the main function where this script begins to execute
if __name__ == "__main__":
    plt.ion() # enables interactive plotting mode
    filename = sys.argv[-1]
    A = np.genfromtxt(filename, delimiter=',', dtype=int)
    side = A.shape[0]
    square_dim = np.sqrt(side)
    
    for i in range (0,side):
        cur_list = list(xrange(side))
        column_lists.append(cur_list)
        for j in range (0,side):
            if (A.item(j,i) > -1 and cur_list.count(A.item(j,i)-1) > 0):
                cur_list.pop(cur_list.index(A.item(j,i)-1))
        #print cur_list
    b = '';
    while (b != 'E\n'):    
        print 'Type a command.'
        print 'P to print initial Sudoku Board'
        print 'S to perform Simulated Annealing'
        print 'E to Exit'
        b =  sys.stdin.readline()
        if (b == 'P\n' or b == 'S\n'):
            options[b]()
        elif (b != 'E\n'):
            print 'Invalid Command\n'
  