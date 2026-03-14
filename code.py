from random import choice, sample
from collections import defaultdict
from os import system
import copy
import heapq
import time

class EIGHT_PUZZLE:
    __BOARD_SIZE = 3
    __DEFAULT_GOAL_STATE = [['1', '2', '3'],
                            ['4', '5', '6'],
                            ['7', '8', '_']]
    __random_pieces = ['1', '2', '3', '4', '5', '6', '7', '8', '_']

    def __init__(self, board = None, goal = None):
        self.board = board if board else self.generate_random_state()
        self.goal_state = goal if goal else self.__DEFAULT_GOAL_STATE
        self.visited_list = set()
        self.move_tracker = defaultdict(tuple)

    def convert_to_tuple(self, state):
        return tuple(tuple(row) for row in state)
        
    def is_visited(self, state):
        if not isinstance(state, tuple):
            state = self.convert_to_tuple(state)
        return False if state not in self.visited_list else True

    def add_to_visited_list(self, state):
        if not isinstance(state, tuple):
            state = self.convert_to_tuple(state)
        self.visited_list.add(state)

    def generate_random_state(self):
        random_sample = sample( self.__random_pieces, len( self.__random_pieces ) )
        return [ random_sample[i * 3:  3 * i + 3] for i in range( self.__BOARD_SIZE ) ]
    
    def get_under_score_pos(self, board):
        for i, row in enumerate( board ): 
            if '_' in row: return ( i, row.index( '_' ) )
        return None, None
    
    def get_heuristic_score(self, board):
        return sum( 1 for i in range( self.__BOARD_SIZE ) 
                    for j in range( self.__BOARD_SIZE ) 
                    if board[i][j] != '_' and board[i][j] != self.goal_state[i][j] )

    def reached_goal_state(self, board):
        return all( board[i][j] == self.goal_state[i][j] 
                    for j in range( self.__BOARD_SIZE ) 
                    for i in range( self.__BOARD_SIZE ) )

    def get_valid_neighbors(self, row, col):
        valid_nei = []
        if row + 1 < self.__BOARD_SIZE: valid_nei.append((row + 1, col))
        if col + 1 < self.__BOARD_SIZE: valid_nei.append((row, col + 1))
        if row - 1 > -1: valid_nei.append((row - 1, col))
        if col - 1 > -1: valid_nei.append((row, col - 1))
        return valid_nei
    
    def get_next_possible_states(self, board):
        srow, scol = self.get_under_score_pos(board)
        neighbhors = self.get_valid_neighbors(srow, scol)
        possible_states = []
        
        for row, col in neighbhors:
            new_board = copy.deepcopy(board)
            new_board[row][col], new_board[srow][scol] = new_board[srow][scol], new_board[row][col]
       
            if not self.is_visited(new_board):
                possible_states.append(new_board)
    
        return possible_states

    # A START ALGORITHM
    def play( self ):
        current_hscore = self.get_heuristic_score( self.board )
        priority_queue = [(current_hscore, 0, self.board, None)]
    
        while priority_queue != []:
            fscore, gscore, current_state, parent = heapq.heappop( priority_queue )

            if self.is_visited( current_state ): continue

            next_pos_states = self.get_next_possible_states(current_state)
            
            for next_state in next_pos_states:
                score = self.get_heuristic_score(next_state) + gscore + 1
                heapq.heappush( priority_queue, (score, gscore + 1, next_state, current_state) )

            self.add_to_visited_list( current_state )
            
            parent = None if parent is None else self.convert_to_tuple(parent)
            child = self.convert_to_tuple(current_state)
            
            self.move_tracker[child] = parent;
            self.board = current_state

            if self.reached_goal_state( current_state ): break

        if not self.reached_goal_state( self.board ):
            print("Cannot solve this puzzle")
        else:
            path = self.get_path()
            self.simulate_path(path)

    def get_path(self):
        path, current = [self.board], self.board
        current_set = self.convert_to_tuple( current )
    
        while cpath := self.move_tracker.get( current_set, None ):
            path.append( cpath )
            current_set = cpath
        
        return path

    def simulate_path(self, path):
        for cpath in path[::-1]:
            system("clear")
            EIGHT_PUZZLE.print_state( cpath )
            time.sleep(0.5)

        print(f"{len( path ) - 1} Moves To Solve ")

    @staticmethod
    def print_state( board ):
        for row in board: 
            for col in row:
                print(col, end = " ")
            print()

if __name__ == "__main__":
    test = EIGHT_PUZZLE()
    board = copy.deepcopy( test.board )
    EIGHT_PUZZLE.print_state( test.board )

    test.play()
    EIGHT_PUZZLE.print_state( board )
