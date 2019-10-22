import trainingData
import numpy as np
import math


testing = trainingData.TestingCases()


def create_array_from_string(string):
    n = int(math.sqrt(len(string)))
    arr = np.zeros((n,n))
    for idx, letter in enumerate(string):
        x = idx % n
        y = (idx - x) // n
        if letter != '.':
            arr[y][x] = int(letter)
    return arr

r = create_array_from_string(testing.expert['start'][0])

def find_empty_cell(grid):

    for idxy, y in enumerate(grid):
        for idxx, x in enumerate(y):
            if x == 0:
                return (idxx, idxy)

    return False

def valid_for_col(grid, col, number):
    return number not in [int(t[col]) for t in grid]

def valid_for_row(grid, row, number):
    return number not in [int(t) for t in grid[row]]

def valid_for_box(grid, position, number):
    (x,y) = position
    n = grid.shape[0]
    grid_x = x // 3
    grid_y = y // 3
    box = grid[grid_y*3:(grid_y+1)*3, grid_x*3:(grid_x+1)*3]
    return number not in box

def valid_pos(grid, position, number):
    (row, col) = position
    return valid_for_col(grid, col, number) and valid_for_row(grid, row, number) and valid_for_box(grid, position, number)

def find_next_valid_number(grid, position):
    (x,y) = position
    start_number = grid[y][x]
    for number in range(start+1,9):
        if valid_pos(grid, position, number):
            return number
    
    return False