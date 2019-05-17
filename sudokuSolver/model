#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 21:26:43 2019

@author: william
"""
import math
import numpy as np

class Cell():
    def __init__(self,posY,posX):
      self.possibleNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
      self.X = posX
      self.Y = posY
      self.section =  int(3*(math.floor(posY/3)) + math.floor(posX/3))
      self.assignedNumber = None
    
    def checkRowAndCol(self, sudukoArray, sectionNumbers):
      ## takes a numpy array containing the current suduko sheet, and a list of list with the numbers for the diffrent sections
      ## and updates the possible numbers for that cell
      x = self.X
      y = self.Y
      transpose = sudukoArray.T
      numList = []
      for number in self.possibleNumbers:
        #print(sudukoArray[y])  
        #print(transpose[x])
        if number in sudukoArray[y]:
          #print('found {} in row'.format(number))
          continue
        elif number in transpose[x]:
          #print('found {} in column'.format(number))
          continue
        elif number in sectionNumbers[self.section]:
            #print('found {} in section'.format(number))
            continue
        else:
          numList.append(number)
          
      self.possibleNumbers = numList   
    
    def checkSection(self, sectionNumbers):
        numList = []
        for number in self.possibleNumbers:
            if number not in sectionNumbers[self.section]:
                numList.append(number)
        self.possibleNumbers = numList
        
            
    
    def updatePossibleNumbers(self, sudukoArray, sectionNumbers):
        
      self.checkRowAndCol(sudukoArray, sectionNumbers)
      self.checkSection(sectionNumbers)
      
      if len(self.possibleNumbers)==1:
          #print('only one number possible: {}'.format(numList[0]))
          self.assignNumber(self.possibleNumbers[0], sectionNumbers)
          
          #self.assignNumber(numList[0],sectionNumbers[self.section])

    def assignNumber(self, number, sectionNumbers):
        self.assignedNumber = number
        self.possibleNumbers = []
        #print(sectionNumbers[self.section])
        if not (number in sectionNumbers[self.section]):
            sectionNumbers[self.section].append(number)