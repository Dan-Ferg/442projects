############################################################
# CMPSC442: Homework 7
############################################################

student_name = "Daniel Ferguson"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import os


############################################################
# Section 1: Sudoku
############################################################

def sudoku_cells():
    cell_list=[]
    for x in range(9):
        for y in range(9):
            cell_list.append((x,y))
    return cell_list

def sudoku_arcs():
    lst = []
    
    for (x,y) in sudoku_cells():
        for row in range(9):
            if row != x:
                lst.append(((x,y),(row,y)))
                
        for col in range(9):
            if col != y:
                lst.append(((x,y),(x,col)))
        
        xdisplace = x%3
        ydisplace = y%3
        
        if xdisplace==0 and ydisplace==0:
            lst.append(((x,y),(x+1,y+1)))
            lst.append(((x,y),(x+1,y+2)))
            lst.append(((x,y),(x+2,y+1)))
            lst.append(((x,y),(x+2,y+2)))
            continue
            
        if xdisplace==1 and ydisplace==0:
            lst.append(((x,y),(x-1,y+1)))
            lst.append(((x,y),(x-1,y+2)))
            lst.append(((x,y),(x+1,y+1)))
            lst.append(((x,y),(x+1,y+2)))
            continue
        
        if xdisplace==2 and ydisplace==0:
            lst.append(((x,y),(x-1,y+1)))
            lst.append(((x,y),(x-1,y+2)))
            lst.append(((x,y),(x-2,y+1)))
            lst.append(((x,y),(x-2,y+2)))
            continue
        
        if xdisplace==0 and ydisplace==1:
            lst.append(((x,y),(x+1,y-1)))
            lst.append(((x,y),(x+1,y+1)))
            lst.append(((x,y),(x+2,y-1)))
            lst.append(((x,y),(x+2,y+1)))
            continue
        
        if xdisplace==1 and ydisplace==1:
            lst.append(((x,y),(x-1,y-1)))
            lst.append(((x,y),(x-1,y+1)))
            lst.append(((x,y),(x+1,y-1)))
            lst.append(((x,y),(x+1,y+1)))
            continue
        
        if xdisplace==2 and ydisplace==1:
            lst.append(((x,y),(x-1,y-1)))
            lst.append(((x,y),(x-1,y+1)))
            lst.append(((x,y),(x-2,y-1)))
            lst.append(((x,y),(x-2,y+1)))
            continue
        
        if xdisplace==0 and ydisplace==2:
            lst.append(((x,y),(x+1,y-1)))
            lst.append(((x,y),(x+1,y-2)))
            lst.append(((x,y),(x+2,y-1)))
            lst.append(((x,y),(x+2,y-2)))
            continue
        
        if xdisplace==1 and ydisplace==2:
            lst.append(((x,y),(x-1,y-1)))
            lst.append(((x,y),(x-1,y-2)))
            lst.append(((x,y),(x+1,y-1)))
            lst.append(((x,y),(x+1,y-2)))
            continue
        
        if xdisplace==2 and ydisplace==2:
            lst.append(((x,y),(x-1,y-1)))
            lst.append(((x,y),(x-1,y-2)))
            lst.append(((x,y),(x-2,y-1)))
            lst.append(((x,y),(x-2,y-2)))
            continue
        
    return lst

def read_board(path):
    board_dic = {}
    
    fd = os.open(path,os.O_RDONLY)
    fo = os.fdopen(fd)
    
    x=0
    for line in fo:
        y = 0
        for val in line.strip('\n'):
            if val=='*':
                board_dic[(x,y)] = set([1,2,3,4,5,6,7,8,9])
            else:
                board_dic[(x,y)] = set([int(val)])
            y+=1
        x+=1
    
    return board_dic

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board
        self.ARCS = ARCS
        self.CELLS = CELLS

    def get_values(self, cell):
        return self.board[cell]
    
    def get_neighbors(self, cell):
        n = {((cell[0],j), cell) for j in range(9)}
        n |= {((j, cell[1]), cell) for j in range(9)}
        dic = {i:0 if i<3 else 3 if i<6 else 6 for i in range(9)}
        pos = (dic[cell[0]],dic[cell[1]])
        n |= {((pos[0]+i,pos[1]+j), cell) for i in range(3) for j in range(3)}
        n.remove((cell,cell))
        return n

    def remove_inconsistent_values(self, cell1, cell2):
        if (cell1,cell2) not in self.ARCS:
            return False
        if len(self.get_values(cell2))==1 and len(self.get_values(cell2)&self.get_values(cell1)):
            self.board[cell1] = self.get_values(cell1) - self.get_values(cell2)
            return True
        return False
                
    def infer_ac3(self):
        arcs = set(self.ARCS)
        while arcs:
            arc = arcs.pop()
            if self.remove_inconsistent_values(arc[0],arc[1]):
                if len(self.get_values(arc[0]))==0:
                    return False
                arcs |= self.get_neighbors(arc[0])
        return True