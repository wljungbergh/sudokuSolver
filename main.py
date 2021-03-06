#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 15:27:46 2019

@author: william
"""

import math
import numpy as np
from PIL import Image, ImageDraw
import time

import trainingData as td

startTime = time.time()

def create_sudoku():
    img = Image.new('RGB',(300,300),color='white')
    size = img.size[0]
    drawImg = ImageDraw.Draw(img)
    for i in range(1,10):
        if i%3 == 0:
            lineWidth = 3
        else:
            lineWidth = 1
        drawImg.line((i*size/9,0, i*size/9,300), fill='black',width = lineWidth)
        drawImg.line((0,i*size/9, 300, i*size/9), fill='black',width = lineWidth)
    return img

def fill_sudoku(img,sudokuArray):    
    drawImg = ImageDraw.Draw(img)
    size = img.size[0]/9
    for i in range(sudokuArray.shape[0]):
        for j in range(sudokuArray.shape[1]):
            xCoord = i * size + size/2
            yCoord = j * size + size/2
            number = sudokuArray[j][i]
            if number != None:
                drawImg.text((xCoord,yCoord) ,str(number), fill = 'black')
                
def merge_img(img1, img2):
    im  = Image.new('RGB',(630,300))
    im.paste(img1, (0,0))
    im.paste(img2, (330,0))
    
    im.show()
    
def create_grid(sudokuArray):
    cellArray = []
    sectionNumbers = [ [] for t in range(9)]
    for i in range(sudokuArray.shape[0]):
        cellArray.append([])
        for j in range(sudokuArray.shape[1]):
            cellArray[i].append(Cell(i,j))
            if sudokuArray[i][j] != None:
                cellArray[i][j].assignNumber(sudokuArray[i][j],sectionNumbers)
            
    return cellArray,sectionNumbers


def getArray(cellArray):
    array = []
    for i in range(len(cellArray)):
        array.append([])
        for j in range(len(cellArray[i])):
            array[i].append(cellArray[i][j].assignedNumber)
            #print(x[i][j].assignedNumber)
    return np.array(array)

def solve_sudoku(sudokuArray):
    solvedSudoku, secNumbers = create_grid(sudokuArray)
    for a in range(500):
        print('lap {}...............................'.format(a))
        for i in range(9):
            for j in range(9):
                if solvedSudoku[i][j].assignedNumber == None:
                    solvedSudoku[i][j].updatePossibleNumbers(getArray(solvedSudoku),secNumbers)
    return solvedSudoku
def createArrayFromString(string):
    ## Takes an 72 character string, with numbers and . represent No Number
    array = []
    for i in range(9):
        tempArr = []
        subStr = string[9*i:9*(i+1)]
        for char in subStr:
            if char == ".":
                char = None
            tempArr.append(char)
        array.append(tempArr)
    return array
    

x = solve_sudoku(expertSudoku)
start = create_sudoku()
fill_sudoku(start, trainingSudoku)

sol = create_sudoku()
fill_sudoku(sol,trainingSudokuSolution)

merge_img(start,sol)
                
done = create_sudoku()
fill_sudoku(done,getArray(x))

merge_img(done,sol)

endTime = time.time()

print(endTime - startTime)