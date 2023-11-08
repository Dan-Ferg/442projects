############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Daniel Ferguson"

############################################################
# Imports
import random
import math
import queue
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    board = []
    count = 1
    stopper = True
    for x in range(rows):
        temp_list = []
        for y in range(cols):
            temp_list.append(count)
            count += 1
        board.append(temp_list)
        
    board[rows-1][cols-1] = 0
    return TilePuzzle(board)

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def get_board(self):
        return self.board

    def get_0_pos(self):
        z = self.board
        for x in range(self.rows):
            for y in range(self.cols):
                if z[x][y] == 0:
                    return [x,y]

    def perform_move(self, direction):
        pos = self.get_0_pos()
        row_pos = pos[0]
        col_pos = pos[1]
        if direction == "up":
            if row_pos == 0:
                return False
            else:
                new_pos = self.board[row_pos-1][col_pos]
                self.board[row_pos-1][col_pos] = 0
                self.board[row_pos][col_pos] = new_pos
                return True
        if direction == "right":
            if col_pos == self.cols-1:
                return False
            else:
                new_pos = self.board[row_pos][col_pos+1]
                self.board[row_pos][col_pos+1] = 0
                self.board[row_pos][col_pos] = new_pos
                return True
        if direction == "down":
            if row_pos == self.rows-1:
                return False
            else:
                new_pos = self.board[row_pos+1][col_pos]
                self.board[row_pos+1][col_pos] = 0
                self.board[row_pos][col_pos] = new_pos
                return True
        if direction == "left":
            if col_pos == 0:
                return False
            else:
                new_pos = self.board[row_pos][col_pos-1]
                self.board[row_pos][col_pos-1] = 0
                self.board[row_pos][col_pos] = new_pos
                return True
        return False

    def scramble(self, num_moves):
        options = ["up","right","down","left"]
        for x in range(num_moves):
            self.perform_move(random.choice(options))
        return

    def is_solved(self):
        tester = create_tile_puzzle(self.rows,self.cols)
        if self.board == tester.get_board():
            return True
        return False

    def copy(self):
        new_copy = []
        for x in range(self.rows):
            new_list = []
            for y in range(self.cols):
                new_list.append(self.board[x][y])
            new_copy.append(new_list)
        return TilePuzzle(new_copy)

    def successors(self):
        moves = ["up","down","right","left"]
        for x in moves:
            self_copy = self.copy()
            if (self_copy.perform_move(x)) != False:
                yield (x,self_copy)

    # Required
    def iddfs_helper(self,limit,moves):
        working_with = []
        answer_list = []

        for x in range(len(moves)):
            if len(moves[x][2])==limit:
                working_with.append(moves[x])
        for y in range(len(working_with)):
            if working_with[y][1].is_solved():
                answer_list.append(working_with[y][2])

        if answer_list == []:
            return None
        elif len(answer_list)==1:
            return answer_list[0]
        else:
            return answer_list
 
    def find_solutions_iddfs(self):
        if self.is_solved():
            yield []
        limit = 1
        explored_moves= []
        for (moves,new_p) in self.successors():
            explored_moves.append([moves,new_p,[moves]])

        while True:
            if limit == 1:
                answer = self.iddfs_helper(limit,explored_moves)
            else:
                next_explored_moves = []
                condition = len(explored_moves)
                for x in range(condition):
                    instance = explored_moves.pop()
                    last_move = []
                    
                    for y in range(len(instance[2])):
                        last_move.append(instance[2][y])
                        
                    for (move,new_p) in instance[1].successors():
                        move_list = []
                        for z in range(len(last_move)):
                            move_list.append(last_move[z])
                        move_list.append(move)
                        next_explored_moves.append([move,new_p,move_list])
                        
                explored_moves = next_explored_moves

                answer = self.iddfs_helper(limit,explored_moves)

            if (answer != None):
                yield answer
            limit +=1

    # Required
    def find_solution_a_star(self):
        pqueue = queue.PriorityQueue()
        visited = []
        pcount=1


        for (move,new_p) in self.successors():
            priority = self.heuristic(new_p)+1
            pqueue.put((priority,pcount,[new_p,[move]]))
            pcount+=1
            visited.append(new_p.get_board())

        while pqueue:
            instance = pqueue.get()
            instance_puzzle = instance[2][0]

            if instance_puzzle.is_solved():
                return instance[2][1]
            else:
                last_move =[]
                for x in range(len(instance[2][1])):
                    last_move.append(instance[2][1][x])

                for (move,new_p) in instance_puzzle.successors():
                    if new_p.get_board() not in visited:
                        instance_moves = []
                        for y in range(len(last_move)):
                            instance_moves.append(last_move[y])
                        instance_moves.append(move)

                        priority = self.heuristic(new_p)+len(instance[2][1])
                        pqueue.put((priority,pcount,[new_p,instance_moves]))
                        pcount+=1
                        visited.append(new_p.get_board())


    def heuristic(self,puzzle):
        distances_to_sum =[]
        rows = puzzle.rows
        cols = puzzle.cols
        right_board = create_tile_puzzle(rows,cols)
        condition = rows*cols

        for x in range(1,condition):
            xy1 = puzzle.get_pos(x,puzzle)
            xy2 = right_board.get_pos(x,right_board)
            man_dist = abs(xy1[0]-xy2[0])+abs(xy1[1]-xy2[1])
            distances_to_sum.append(man_dist)
        total = 0
        for y in range(len(distances_to_sum)):
            total+=distances_to_sum[y]
        return total


    def get_pos(self,number,puzzle):
        for x in range(puzzle.rows):
            for y in range(puzzle.cols):
                if puzzle.board[x][y] == number:
                    return [x,y]


############################################################
# Section 2: Grid Navigation
############################################################

def find_path(start, goal, scene):
    poss_move_list = ["up","down","left","right","up-left","up-right","down-left","down-right"]
    translate_move = {"up":(-1,0),"down":(1,0),"left":(0,-1),"right":(0,1),"up-left":(-1,-1),"up-right":(-1,1)}
    translate_move["down-left"] = (1,-1)
    translate_move["down-right"] = (1,1)
    heuristic_path_init = euc_path(start,goal,[])
    where_at = start
    move_list = [start]
    visited = [start]
    frontier = queue.PriorityQueue()
    pcount = 1

    if scene[goal[0]][goal[1]]==True or scene[start[0]][start[1]]==True:
        return None

    if can_move(heuristic_path_init[0],scene):
        move_list.append(heuristic_path_init[0])
        visited.append(heuristic_path_init[0])
        frontier.put((0,pcount,move_list))
        pcount+=1
    else:
        for x in poss_move_list:
            direction_move = translate_move[x]
            the_move = (where_at[0]+direction_move[0],where_at[1]+direction_move[1])
            if (can_move(the_move,scene)):
                move_list = [start]
                move_list.append(the_move)
                visited.append(the_move)
                possible = euc_path(the_move,goal,[])
                frontier.put((len(possible),pcount,move_list))
                pcount+=1

    while frontier.empty()==False:
        instance = frontier.get()
        if instance[2][-1]==goal:
            return instance[2]

        heuristic_path = euc_path(instance[2][-1],goal,[])

        if can_move(heuristic_path[0],scene):
            if heuristic_path[0] not in visited:
                move_list_copy = copy_move_list(instance[2])
                move_list_copy.append(heuristic_path[0])
                frontier.put((len(heuristic_path),pcount,move_list_copy))
                pcount+=1
        else:
            for y in poss_move_list:
                direction_move = translate_move[y]
                move_list_copy = copy_move_list(instance[2])
                the_move = (move_list_copy[-1][0]+direction_move[0],move_list_copy[-1][1]+direction_move[1])
                if (can_move(the_move,scene)):
                    if the_move not in visited:
                        move_list_copy = copy_move_list(move_list_copy)
                        move_list_copy.append(the_move)
                        visited.append(the_move)
                        possible = euc_path(the_move,goal,[])
                        frontier.put((len(possible),pcount,move_list_copy))
                        pcount+=1
    return None

def copy_move_list(move_list):
    copy = []
    for x in move_list:
        copy.append(x)
    return copy

def can_move(move,scene):
    if move[0]<0 or move[1]<0 or move[1]>len(scene[0])-1 or move[0]>len(scene)-1:
        return False
    elif scene[move[0]][move[1]] == True:
        return False
    else:
        return True


def euc_path(start,goal,move_list):
    if start==goal:
        return move_list

    start_x = start[0]
    start_y = start[1]
    goal_x = goal[0]
    goal_y=goal[1]

    if start_x>goal_x and start_y>goal_y:
        move_list.append((start_x-1,start_y-1))
        return euc_path((start_x-1,start_y-1),goal,move_list)
    if start_x>goal_x and start_y<goal_y:
        move_list.append((start_x-1,start_y+1))
        return euc_path((start_x-1,start_y+1),goal,move_list)
    if start_x<goal_x and start_y<goal_y:
        move_list.append((start_x+1,start_y+1))
        return euc_path((start_x+1,start_y+1),goal,move_list)
    if start_x<goal_x and start_y>goal_y:
        move_list.append((start_x+1,start_y-1))
        return euc_path((start_x+1,start_y-1),goal,move_list)

    if start_x>goal_x and start_y==goal_y:
        move_list.append((start_x-1,start_y))
        return euc_path((start_x-1,start_y),goal,move_list)
    if start_x<goal_x and start_y==goal_y:
        move_list.append((start_x+1,start_y))
        return euc_path((start_x+1,start_y),goal,move_list)
    if start_y>goal_y and start_x==goal_x:
        move_list.append((start_x,start_y-1))
        return euc_path((start_x,start_y-1),goal,move_list)
    if start_y<goal_y and start_x==goal_x:
        move_list.append((start_x,start_y+1))
        return euc_path((start_x,start_y+1),goal,move_list)
