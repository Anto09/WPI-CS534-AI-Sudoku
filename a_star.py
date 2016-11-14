#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  4 13:13:15 2014

@author: anto
"""


import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import copy
from Queue import Queue
from heapq import heappush, heappop
#this is the main function where this script begins to execute

class PriorityQueue(Queue):
    
    def _init(self, maxsize):
        self.maxsize = maxsize
        self.queue = []
        
    def _put(self, item):
        return heappush(self.queue, item)

    def _get(self):
        return heappop(self.queue)

side = 0
square_dim = 0.
A = []
max_slots = 0
priority_queue = PriorityQueue()
cur_time = 0.
start_time = 0.
t_max = 300.
        
class Board:
    cells = []    
    open_cells_indices = []
    open_cells = []
    closed_cells = []
    
    def __init__(self,cells):
        self.cells = cells
    
class Cell:    
    i = -1
    j = -1    
    possibleVal = np.ones(side)
    isOpen = 1
    value = -1
    assignment = -1

    def __init__(self,i,j,assignment):
        self.i = i
        self.j = j
        self.assignment = assignment
        self.possibleVal = np.ones(side, dtype=np.int)
        
    def Reset(self):
        del self.possibleVal
        self.possibleVal = np.ones(side, dtype=np.int)
    
    def Open(self):
        self.isOpen = 1
        
    def Close(self):
        self.isOpen = 0
        
    def Assign(self,assignment):
        self.assignment = assignment            
          
def printMatrix():
    print A, '\n'
    
def CheckConfiguration(board):
    row_conflicts = 0
    col_conflicts = 0
    box_conflicts = 0
    total_conflicts = 0    
    
    for i in range(0,side):
        row_checker = np.zeros(side)
        col_checker = np.zeros(side)
        for j in range(0,side):
            if (board.cells[i,j].assignment==-1):
                continue
            if (row_checker[board.cells[i,j].assignment-1] == 1):
                row_conflicts += 1
            else:
                row_checker[board.cells[i,j].assignment-1] = 1                
            if (col_checker[board.cells[j,i].assignment-1] == 1):
                col_conflicts += 1
            else:
                col_checker[board.cells[j,i].assignment-1] = 1
    
        
    for j in range (0,side,int(square_dim)):    
        for i in range (0,side,int(square_dim)):
            box_checker = np.zeros(side)  
            for x in range (i,i+int(square_dim)):
                for y in range (j,j+int(square_dim)):
                    if (board.cells[x,y].assignment == -1):
                        continue
                    if (box_checker[board.cells[x,y].assignment-1] == 1):
                        box_conflicts += 1;
                    else: 
                        box_checker[board.cells[x,y].assignment-1] = 1
        
    total_conflicts = row_conflicts + col_conflicts + box_conflicts
    return total_conflicts
    
def H(cell, board):
    row = cell.i
    col = cell.j

    s_d = int(square_dim)
    
    left = row - row%s_d
    top = col - col%s_d
    
    for i in range(0,side):
        if (board.cells[i,col].isOpen == 0):
            cell.possibleVal[board.cells[i,col].assignment-1] = 0
    for j in range(0,side):
        if (board.cells[row,j].isOpen == 0):
            cell.possibleVal[board.cells[row,j].assignment-1] = 0
    for i in range (left, left + int(square_dim)):
        for j in range (top, top + int(square_dim)):
            if (board.cells[i,j].isOpen == 0):            
                cell.possibleVal[board.cells[i,j].assignment-1] = 0
    
    return int(sum(cell.possibleVal))
    
def G(cell, board):
    row = cell.i
    col = cell.j
    
    s_d = int(square_dim)
    
    left = row - row%s_d
    top = col - col%s_d
    right = left + int(square_dim) - 1 
    bot = top + int(square_dim) -1 
    
    open_count = 0    
    
    for i in range(left, left + int(square_dim)):
        for j in range (top, top + int(square_dim)):
            if (board.cells[i,j].isOpen == 1):            
                open_count+=1
    for i in range(0,top):
        if (board.cells[i,col].isOpen == 1):
            open_count+=1
    for i in range(bot+1, side):
        if (board.cells[i,col].isOpen == 1):
            open_count+=1
    for i in range(0,left):
        if (board.cells[row,i].isOpen == 1):
            open_count+=1
    for i in range(right+1,side):
        if (board.cells[row,i].isOpen == 1):
            open_count+=1
            
    return int(open_count)-1



def ScoreBoard(board):
    for cell in board.open_cells:
        g = G(cell,board)
        h = H(cell,board)
        cell.value = h+g

def CheckEmpty(board):
    return len(board.open_cells) == 0

def Astar(board, pq):
    global cur_time
    global start_time
    
    if (cur_time >= t_max):        
        return None
    
    if (len(pq.queue) == 0):
       cur_time = time.clock() - start_time  
       if (CheckEmpty(board)):
           return board
       else:
           return None
            
    else:
        final = None        
        while (len(pq.queue) > 0):
            current_cell = pq.get()[1]
            current_cell.Close()
            
            new_board = copy.copy(board)
            new_board.cells = copy.copy(board.cells)
            new_board.open_cells = copy.copy(board.open_cells)
            new_board.closed_cells = copy.copy(board.closed_cells)
            
            new_board.open_cells.remove(current_cell)
            new_board.closed_cells.append(current_cell)
            
            for i in range (0,side):    
                if (current_cell.possibleVal[i] > 0):
                    current_cell.possibleVal[i] = 0
                    temp_pq = PriorityQueue()
                    temp_pq.queue = copy.copy(pq.queue)
                    temp_queue = []
                    
                    current_cell.Assign(i+1)
                    while (len(temp_pq.queue) > 0):
                        temp_queue.append(temp_pq.get()[1])
                    for j in range (0,len(temp_queue)):
                        temp_queue[j].Reset()
                        temp_queue[j].value = H(temp_queue[j], new_board) + G(temp_queue[j], new_board)
                    while (len(temp_queue) > 0):
                        new_cell = temp_queue.pop()
                        temp_pq.put((new_cell.value,new_cell))
                    del temp_queue
                        
                    ans = Astar(new_board,temp_pq)
                    if (ans != None):# and CheckEmpty(ans)):
                        final = ans
                        del temp_pq                        
                        return ans
            if (final == None):
                current_cell.Open()
            del new_board                     
            cur_time = time.clock() - start_time
        return final

def Solve():
    global priority_queue
    global cur_time
    global start_time
    
    priority_queue = PriorityQueue()
    
    start_board_cells = np.empty((side,side), dtype=object)
    start_board = Board(start_board_cells)
    
    #print start_board    
    for i in range(0,side):
        for j in range(0,side):
            cell = Cell(i,j,A[i,j])
            if (A[i,j] > -1):
                cell.Close()
                start_board.closed_cells.append(cell)
            else:
                start_board.open_cells_indices.append((i,j))
                start_board.open_cells.append(cell)
            start_board.cells[i,j] = cell
                 
    ScoreBoard(start_board)
    
    for cell in start_board.open_cells:
        priority_queue.put((cell.value,cell))
    #print start_board
    
    cur_time = 0.    
    start_time = time.clock()
    final = Astar(start_board,copy.copy(priority_queue))
    cur_time = time.clock() - start_time
    
    if (final == None):
        print 'Solution not found'
    else:
        final_board_cells = np.empty((side,side), dtype=int)
        for i in range(0,side):
            for j in range(0,side):
                final_board_cells[i,j] =  final.cells[i,j].assignment
        print final_board_cells
    print 'RunTime: ',cur_time
    
    sys.exit()
    
options = {
    'P\n' : printMatrix,
    'S\n' : Solve,
 }
 
if __name__ == "__main__":
    plt.ion() # enables interactive plotting mode
    filename = sys.argv[-1]
    A = np.genfromtxt(filename, delimiter=',', dtype=int)
    side = A.shape[0]
    square_dim = np.sqrt(side)
    max_slots = (side-1) + (side-1) + (side-1)**2
    
    b = '';
    while (b != 'E\n'):    
        print 'Type a command.'
        print 'P to print initial Sudoku Board'
        print 'S to perform A* Search'
        print 'E to Exit'
        b =  sys.stdin.readline()
        if (b == 'P\n' or b == 'S\n'):
            options[b]()
        elif (b != 'E\n'):
            print 'Invalid Command\n'