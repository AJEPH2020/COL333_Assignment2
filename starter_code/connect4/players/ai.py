import random
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer

import time
import copy



class AIPlayer:



    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        # Do the rest of your implementation here

        # # print('initializing')




    # '''gives the next possible state by performing an valid action on the copy of current state '''
    def move_state(self, player_no: int, state: Tuple[np.array, Dict[int, Integer]], action: Tuple[int, bool]) -> Tuple[np.array, Dict[int, Integer]]:

        # '''if the action is standard, changing the last 0 from top to the players number '''
        if (action[1] == 0): 

            arr = state[0]
            n = len(arr)

            for i in reversed(range(n)):
                if (arr[i][action[0]] == 0):
                    arr[i][action[0]] = player_no
                    break

            return (arr,state[1])
        
        # ''' if the action is PopOut, shifting all values in the column down by one place and adding a 0 on the top '''
        else:

            arr = state[0]
            n = len(arr)

            last = 0
            for i in range(n):
                temp = last
                last = arr[i][action[0]]
                arr[i][action[0]] = temp

            dic = state[1]
            dic[player_no].decrement # ''' decreasing the popOuts left for this player '''

            return (arr,dic)



    def dfs_alphabeta(self, state: Tuple[np.array, Dict[int, Integer]], max_min: bool, depth: int, alpha: int, beta: int) -> Tuple[Tuple[int, bool],int]:

        # ''' max state '''
        if (max_min == 1):

            if (self.player_number == 1): # ''' finding the player number of the opponent'''
                opponent = 2
            else:
                opponent = 1


            valid_actions = get_valid_actions(self.player_number, state) # ''' valid actions for current player '''

            if (depth == 0 or len(valid_actions)==0): # ''' if depth or a EndGame state reaches '''

                # ''' counting the node as leaf node with value = difference of score b/w both players wrt current player '''
                pts = get_pts(self.player_number,state[0]) - get_pts(opponent,state[0])
                return ((0,0),pts)


            mx = -2147483648
            mx_index = 0

            for i in range(len(valid_actions)):
                action = valid_actions[i]

                copy_state = (state[0].copy(), dict(state[1]))
                copy_state = self.move_state(self.player_number, copy_state, action)


                x = (self.dfs_alphabeta(copy_state, 0, depth-1, alpha, beta))[1]

                if (x > mx): # maximizing score (current)
                    mx = x
                    mx_index = i

                if(mx >= beta): # pruning
                    return (valid_actions[mx_index],mx)
                    
                alpha = max(alpha,mx)
                
            return (valid_actions[mx_index],mx)


        # ''' min state '''
        else:

            if (self.player_number == 1): # ''' finding the player number of the opponent'''
                opponent = 2
            else:
                opponent = 1


            valid_actions = get_valid_actions(opponent, state) # ''' valid actions for the opponent '''

            if (depth == 0 or len(valid_actions)==0): # ''' if depth or a EndGame state reaches '''

                # ''' counting the node as leaf node with value = difference of score b/w both players wrt current player '''
                pts = get_pts(self.player_number,state[0]) - get_pts(opponent,state[0])
                return ((0,0),pts)


            mn = 2147483648
            mn_index = 0

            for i in range(len(valid_actions)):
                action = valid_actions[i]

                copy_state = (state[0].copy(), dict(state[1]))
                copy_state = self.move_state(opponent, copy_state, action)


                x = (self.dfs_alphabeta(copy_state, 1, depth-1, alpha, beta))[1]

                if (x < mn): # minimizing score (opponent)
                    mn = x
                    mn_index = i

                if(mn <= alpha): # pruning
                    return (valid_actions[mn_index],mn)
                    
                beta = min(beta,mn)
            
            return (valid_actions[mn_index],mn)

    

    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move
        This will play against either itself or a human player
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here

        # depth = 2 # adjust with time & size(if possible) (b/w 3 & 4 most probably)


        # start_time_intelligent = time.time()


        if (self.time < 7):
            depth = 3
        elif (self.time < 15):
            depth = 4
        else:
            depth = 5
        
        
        if(len(state[0][0]) <= 8):
            depth += 1
        if(len(state[0][0]) <= 6):
            depth += 1
        if(len(state[0][0]) <= 4):
            depth += 2
        if(len(state[0][0]) <= 2):
            depth += 3


        ans = (self.dfs_alphabeta(state, 1, depth,-2147483648,2147483648))[0]
 
        return ans

        # raise NotImplementedError('Whoops I don\'t know what to do')



    # ----------------------------------------------------------------------------------------------------------------



    def dfs_expectimax(self, state: Tuple[np.array, Dict[int, Integer]], max_min: bool, depth: int) -> Tuple[Tuple[int, bool],int]:

        # ''' max state '''
        if (max_min == 1):

            if (self.player_number == 1):
                opponent = 2
            else:
                opponent = 1


            valid_actions = get_valid_actions(self.player_number, state)

            if (depth == 0 or len(valid_actions)==0):

                pts = get_pts(self.player_number,state[0]) - get_pts(opponent,state[0])
                return ((0,0),pts)


            mx = -2147483648
            mx_index = 0


            for i in range(len(valid_actions)):
                action = valid_actions[i]

                copy_state = (state[0].copy(), dict(state[1]))
                copy_state = self.move_state(self.player_number, copy_state, action)


                x = (self.dfs_expectimax(copy_state, 0, depth-1))[1]

                if (x > mx):
                    mx = x
                    mx_index = i
                
            return (valid_actions[mx_index],mx)


        # ''' avg state '''
        else:

            if (self.player_number == 1):
                opponent = 2
            else:
                opponent = 1


            valid_actions = get_valid_actions(opponent, state)

            if (depth == 0 or len(valid_actions)==0):

                pts = get_pts(self.player_number,state[0]) - get_pts(opponent,state[0])
                return ((0,0),pts)


            sm = 0

            for i in range(len(valid_actions)):
                action = valid_actions[i]

                copy_state = (state[0].copy(), dict(state[1]))
                copy_state = self.move_state(opponent, copy_state, action)


                x = (self.dfs_expectimax(copy_state, 1, depth-1))[1]

                sm += x
            
            ans = sm/len(valid_actions)
                
            return ((0,0),ans)



    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move based on
        the Expecti max algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here


        # depth = 3 # adjust with time & size(if possible) (b/w 3 & 4 most probably)

        depth = 3

        if(len(state[0][0]) <= 6):
            depth += 1
        if(len(state[0][0]) <= 4):
            depth += 1
        if(len(state[0][0]) <= 2):
            depth += 2
        
        
        ans = (self.dfs_expectimax(state, 1, depth))[0]

        return ans

        # raise NotImplementedError('Whoops I don\'t know what to do')
