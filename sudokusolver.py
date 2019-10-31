import trainingData
import numpy as np
import math


def create_array_from_string(string):
    n = int(math.sqrt(len(string)))
    arr = np.zeros((n,n), dtype='int')
    for idx, letter in enumerate(string):
        x = idx % n
        y = (idx - x) // n
        if letter != '.':
            arr[y][x] = int(letter)
    return arr

def create_string_from_array(grid):
    string = ''
    for y in grid:
        for x in y:
            string += str(x)

    return string

def find_empty_cell(grid):
    n = grid.shape[0]
    flat = grid.flatten()
    try:
        idx = np.where(flat == 0)[0][0]
        idxx = idx % n
        idxy =  idx // n
        return (idxx, idxy)

    except:
        return False

def print_grid(grid):
    string = create_string_from_array(grid)
    printed_string = ''
    for i in range(9):
        x = i*9
        printed_string += string[x:x+3] + '|' + string[x+3:x+6] + '|' + string[x+6:x+9] + '\n'
        printed_string += '----------- \n'
    
    print(printed_string)

def valid_for_col(grid, col, number):
    return number not in grid[:, col]

def valid_for_row(grid, row, number):
    return number not in grid[row]

def valid_for_box(grid, position, number):
    (x,y) = position
    n = grid.shape[0]
    grid_x = x // 3
    grid_y = y // 3
    box = grid[grid_y*3:(grid_y+1)*3, grid_x*3:(grid_x+1)*3]
    return number not in box

def valid_pos(grid, position, number):
    (col, row) = position
    return valid_for_row(grid, row, number) and valid_for_col(grid, col, number) and valid_for_box(grid, position, number)

def find_next_valid_number(grid, position):
    (x,y) = position
    start_number = grid[y][x]

    for number in range(start_number+1,10):
        if valid_pos(grid, position, number):
            return number
    
    return False

def is_solved(grid):
    return not find_empty_cell(grid)

def solve_sudoku(grid):
    backtrack = False
    filled_cells = []
    iterations = 0
    while not is_solved(grid):
        iterations += 1

        if not backtrack:
            pos = find_empty_cell(grid)
        else:
            if filled_cells: 
                pos = filled_cells.pop()
            else:
                print("Solution couldn't be found!")
                return False
        
        number = find_next_valid_number(grid, pos)
        if number:
            grid[pos[1]][pos[0]] = number
            filled_cells.append(pos)
            backtrack = False
        else:
            grid[pos[1]][pos[0]] = 0
            backtrack = True
    print(f'Number of iterations: {iterations}')
    return grid

if __name__ == '__main__':
    testing = trainingData.TestingCases()
    r = create_array_from_string(testing.expert['start'][0])
    solved = solve_sudoku(r)
    print(solved)
   

