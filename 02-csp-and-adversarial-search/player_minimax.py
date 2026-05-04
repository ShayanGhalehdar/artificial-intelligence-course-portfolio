from Board import BoardUtility
import random
import copy
import numpy as np
import sys

sys.setrecursionlimit(5000000)

### IMPORTANT ###

#   Each move with depth 1 takes 1 second
#   Each move with depth 2 takes almost 10 seconds
#   Each move with depth 3 takes more than a minute to run
#   I do not recommend depths equal or greater than 3

### IMPORTANT ###

class Player:
    def __init__(self, player_piece):
        self.piece = player_piece

    def play(self, board):
        return 0


class RandomPlayer(Player):
    def play(self, board):
        return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]


class HumanPlayer(Player):
    def play(self, board):
        move = input("row, col, region, rotation\n")
        move = move.split()
        print(move)
        return [[int(move[0]), int(move[1])], int(move[2]), move[3]]


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=5):
        self.player_piece = player_piece
        if player_piece == 1:
            self.opp_piece = 2
        else:
            self.opp_piece = 1
        self.depth = depth
    
    def make_move(game_board, row, col, region, rotation, piece):
        
        assert game_board[row][col] == 0
        game_board[row][col] = piece
        BoardUtility.rotate_region(game_board, region, rotation)
    
    def negative_score(seq: list[int], opp_piece: int):
        score=0
        if len(seq)==5:
            if seq.count(opp_piece)==5:
                score= -500000
            elif seq.count(opp_piece)==4:
                score= -10000
            elif seq.count(opp_piece)==3:
                score= -1000     
                
        elif len(seq)==6:
            if seq[0:5].count(opp_piece)==5:
                score= -500000
            elif seq[1:6].count(opp_piece)==5:
                score= -500000
            elif seq[0:5].count(opp_piece)==4:
                score= -20000
            elif seq[1:6].count(opp_piece)==4:
                score= -20000
            elif seq[0:5].count(opp_piece)==3:
                score= -1000
            elif seq[1:6].count(opp_piece)==3:
                score= -1000
        
        return score
    
    def positive_score(seq: list[int], player_piece: int):
        score=0
        if len(seq)==5:
            if seq.count(player_piece)==5:
                score= 1000000
            elif seq.count(player_piece)==4:
                score= 2000
            elif seq.count(player_piece)==3:
                score= 200
            elif seq.count(player_piece)==2:
                score= 10
            elif seq.count(player_piece)==1:
                score= 1
                
        elif len(seq)==6:
            
            if seq[0:5].count(player_piece)==5:
                score= 1000000
            elif seq[1:6].count(player_piece)==5:
                score= 1000000
            elif seq[0:5].count(player_piece)==4:
                score= 30000
            elif seq[1:6].count(player_piece)==4:
                score= 30000
            elif seq[0:5].count(player_piece)==3:
                score= 2000
            elif seq[1:6].count(player_piece)==3:
                score= 2000
            elif seq[0:5].count(player_piece)==2:
                score= 200
            elif seq[1:6].count(player_piece)==2:
                score= 200
            elif seq[0:5].count(player_piece)==1:
                score= 10
            elif seq[1:6].count(player_piece)==1:
                score= 10
        
        return score
    
    def evaluate(self, board):
        valid = BoardUtility.get_valid_locations(board)
        score=0
        
        for i in range(6):
            if (self.player_piece in board[i][1:5]) or (board[i][0]==self.player_piece and board[i][5]==self.player_piece):
                continue
            else:
                if board[i][0]==self.player_piece:
                    score = score + MiniMaxPlayer.negative_score(board[i][1:6], self.opp_piece)
                elif board[i][5]==self.player_piece:
                    score = score + MiniMaxPlayer.negative_score(board[i][0:5], self.opp_piece)
                else:
                    score = score + MiniMaxPlayer.negative_score(board[i], self.opp_piece)
        
        transposed_board = np.array(board).T.tolist()
        for i in range(6):
            if (self.player_piece in transposed_board[i][1:5]) or (transposed_board[i][0]==self.player_piece and transposed_board[i][5]==self.player_piece):
                continue
            else:
                if transposed_board[i][0]==self.player_piece:
                    score = score + MiniMaxPlayer.negative_score(transposed_board[i][1:6], self.opp_piece)
                elif transposed_board[i][5]==self.player_piece:
                    score = score + MiniMaxPlayer.negative_score(transposed_board[i][0:5], self.opp_piece)
                else:
                    score = score + MiniMaxPlayer.negative_score(transposed_board[i], self.opp_piece)
                
        seq = []
        seq.append([board[0][0],board[1][1],board[2][2],board[3][3],board[4][4],board[5][5]])
        seq.append([board[0][5],board[1][4],board[2][3],board[3][2],board[4][1],board[5][0]])
        
        for i in range(len(seq)):
            if (self.player_piece in seq[i][1:5]) or (seq[i][0] == self.player_piece and seq[i][5] == self.player_piece):
                continue
            else:
                if seq[i][0] == self.player_piece:
                    score = score + MiniMaxPlayer.negative_score(seq[i][1:6], self.opp_piece)
                elif seq[i][5] == self.player_piece:
                    score = score + MiniMaxPlayer.negative_score(seq[i][0:5], self.opp_piece)
                else:
                    score = score + MiniMaxPlayer.negative_score(seq[i], self.opp_piece)
                    
        for i in range(len(seq)):
            if (self.opp_piece in seq[i][1:5]) or (seq[i][0] == self.opp_piece and seq[i][5] == self.opp_piece):
                continue
            else:
                if seq[i][0] == self.opp_piece:
                    score = score + MiniMaxPlayer.positive_score(seq[i][1:6], self.player_piece)
                elif seq[i][5] == self.opp_piece:
                    score = score + MiniMaxPlayer.positive_score(seq[i][0:5], self.player_piece)
                else:
                    score = score + MiniMaxPlayer.positive_score(seq[i], self.player_piece)
        
        seq = []
        seq.append([board[0][1],board[1][2],board[2][3],board[3][4],board[4][5]])
        seq.append([board[1][0],board[2][1],board[3][2],board[4][3],board[5][4]])
        seq.append([board[0][4],board[1][3],board[2][2],board[3][1],board[4][0]])
        seq.append([board[1][5],board[2][4],board[3][3],board[4][2],board[5][1]])
        
        for i in range(len(seq)):
            if self.player_piece in seq[i]:
                continue
            else:
                score = score + MiniMaxPlayer.negative_score(seq[i], self.opp_piece)
        for i in range(len(seq)):
            if self.opp_piece in seq[i]:
                continue
            else:
                score = score + MiniMaxPlayer.positive_score(seq[i], self.player_piece)
        
        for i in range(6):
            if (self.opp_piece in board[i][1:5]) or (board[i][0]==self.opp_piece and board[i][5]==self.opp_piece):
                continue
            else:
                if board[i][0]==self.opp_piece:
                    score = score + MiniMaxPlayer.positive_score(board[i][1:6], self.player_piece)
                elif board[i][5]==self.opp_piece:
                    score = score + MiniMaxPlayer.positive_score(board[i][0:5], self.player_piece)
                else:
                    score = score + MiniMaxPlayer.positive_score(board[i], self.player_piece)
                    
        transposed_board = np.array(board).T.tolist()
        for i in range(6):
            if (self.opp_piece in transposed_board[i][1:5]) or (transposed_board[i][0]==self.opp_piece and transposed_board[i][5]==self.opp_piece):
                continue
            else:
                if transposed_board[i][0]==self.opp_piece:
                    score = score + MiniMaxPlayer.positive_score(transposed_board[i][1:6], self.player_piece)
                elif transposed_board[i][5]==self.opp_piece:
                    score = score + MiniMaxPlayer.positive_score(transposed_board[i][0:5], self.player_piece)
                else:
                    score = score + MiniMaxPlayer.positive_score(transposed_board[i], self.player_piece)

        
        return score
    
    
    def temp_play(self, temp_board, depth_tracker, valid_locations, max_score):
        
        original_board = copy.deepcopy(temp_board)
        for i in reversed(range(self.depth)):
            if depth_tracker[i][2] == "clockwise":
                depth_tracker[i][2] = "anticlockwise"
                MiniMaxPlayer.make_move(temp_board[i],depth_tracker[i][0][0],depth_tracker[i][0][1],depth_tracker[i][1],depth_tracker[i][2],self.player_piece)
                
                if i!=self.depth-1:
                    for j in range(i+1,self.depth):
                        valid_locations[j]=BoardUtility.get_valid_locations(temp_board[j-1])

                        depth_tracker[j][1]=0
                        depth_tracker[j][2] = "clockwise"
                        depth_tracker[j][0][0] = valid_locations[j][0][0]
                        depth_tracker[j][0][1] = valid_locations[j][0][1]
                        del valid_locations[j][0]
                        temp_board[j]=copy.deepcopy(temp_board[j-1])
                        original_board[j]=copy.deepcopy(temp_board[j-1])
                        MiniMaxPlayer.make_move(temp_board[j],depth_tracker[j][0][0],depth_tracker[j][0][1],depth_tracker[j][1],depth_tracker[j][2],self.player_piece)

                
                score = MiniMaxPlayer.evaluate(self,temp_board[i])
                if score>max_score:
                    max_score = copy.deepcopy(score)
                    self.best_move = copy.deepcopy(depth_tracker[0])
                    
                MiniMaxPlayer.temp_play(self, original_board, depth_tracker, valid_locations,max_score)
                
            else:
                if depth_tracker[i][1] !=4:
                    depth_tracker[i][1]=depth_tracker[i][1]+1
                    depth_tracker[i][2] = "clockwise"
                    MiniMaxPlayer.make_move(temp_board[i],depth_tracker[i][0][0],depth_tracker[i][0][1],depth_tracker[i][1],depth_tracker[i][2],self.player_piece)
                    
                    if i!=self.depth-1:
                        for j in range(i+1,self.depth):
                            valid_locations[j]=BoardUtility.get_valid_locations(temp_board[j-1])

                            depth_tracker[j][1]=0
                            depth_tracker[j][2] = "clockwise"
                            depth_tracker[j][0][0] = valid_locations[j][0][0]
                            depth_tracker[j][0][1] = valid_locations[j][0][1]
                            del valid_locations[j][0]
                            temp_board[j]=copy.deepcopy(temp_board[j-1])
                            original_board[j]=copy.deepcopy(temp_board[j-1])
                            MiniMaxPlayer.make_move(temp_board[j],depth_tracker[j][0][0],depth_tracker[j][0][1],depth_tracker[j][1],depth_tracker[j][2],self.player_piece)

                    score = MiniMaxPlayer.evaluate(self,temp_board[i])
                    if score>max_score:
                        max_score = copy.deepcopy(score)
                        self.best_move = copy.deepcopy(depth_tracker[0]) 
                    
                    MiniMaxPlayer.temp_play(self, original_board, depth_tracker, valid_locations,max_score)
                else:
                    if len(valid_locations[i])!=0:
                        depth_tracker[i][1]=0
                        depth_tracker[i][2] = "clockwise"
                        del valid_locations[i][0]
                        if len(valid_locations[i])==0:
                            if i==0:
                                
                                return self.best_move
                                break
                            continue
                        depth_tracker[i][0][0] = valid_locations[i][0][0]
                        depth_tracker[i][0][1] = valid_locations[i][0][1]
                        MiniMaxPlayer.make_move(temp_board[i],depth_tracker[i][0][0],depth_tracker[i][0][1],depth_tracker[i][1],depth_tracker[i][2],self.player_piece)
                        
                        if i!=self.depth-1:
                            for j in range(i+1,self.depth):
                                valid_locations[j]=BoardUtility.get_valid_locations(temp_board[j-1])

                                depth_tracker[j][1]=0
                                depth_tracker[j][2] = "clockwise"
                                depth_tracker[j][0][0] = valid_locations[j][0][0]
                                depth_tracker[j][0][1] = valid_locations[j][0][1]
                                del valid_locations[j][0]
                                temp_board[j]=copy.deepcopy(temp_board[j-1])
                                original_board[j]=copy.deepcopy(temp_board[j-1])
                                MiniMaxPlayer.make_move(temp_board[j],depth_tracker[j][0][0],depth_tracker[j][0][1],depth_tracker[j][1],depth_tracker[j][2],self.player_piece)
                        
                        score = MiniMaxPlayer.evaluate(self,temp_board[i])
                        if score>max_score:
                            max_score = copy.deepcopy(score)
                            self.best_move = copy.deepcopy(depth_tracker[0])

                            
                        MiniMaxPlayer.temp_play(self, original_board, depth_tracker, valid_locations,max_score)
                    else:
                        continue
                                             
        return self.best_move
    
    
    def play(self, board):
        
        depth_tracker = [[[None,None],None,None] for i in range(self.depth)]
        temp_board = copy.deepcopy(board.tolist())
        valid_locations = []
        original_board = []
        
        for i in range(self.depth):
            original_board.append(copy.deepcopy(temp_board))
            valid_locations.append(BoardUtility.get_valid_locations(temp_board))
            depth_tracker[i] = [BoardUtility.get_valid_locations(temp_board)[0], 1, "clockwise"]
            if i%2==0:
                piece = self.player_piece
            else:
                piece = self.opp_piece
            MiniMaxPlayer.make_move(temp_board,depth_tracker[i][0][0],depth_tracker[i][0][1],depth_tracker[i][1],depth_tracker[i][2],piece)
        

        #for i in range(6):
        #    print(original_board[i])
#         for i in range(len(original_board)):
#             for j in range(6):
#                 print(original_board[i][j])
#             print("")
        
        max_score=-10000
        move = copy.deepcopy(depth_tracker[0])
        best = MiniMaxPlayer.temp_play(self, original_board, depth_tracker,valid_locations, max_score)
        
        row = best[0][0]
        col = best[0][1]
        region = best[1]
        rotation = best[2]
        # Todo: implement minimax algorithm
        #print(MiniMaxPlayer.evaluate(self,board))
        return [[row, col], region, rotation]



class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.1):
        self.player_piece = player_piece
        if player_piece == 1:
            self.opp_piece = 2
        else:
            self.opp_piece = 1
        self.depth = depth
        self.prob_stochastic = prob_stochastic

    def make_move(game_board, row, col, region, rotation, piece):
        
        assert game_board[row][col] == 0
        game_board[row][col] = piece
        BoardUtility.rotate_region(game_board, region, rotation)
    
    def negative_score(seq: list[int], opp_piece: int):
        score=0
        if len(seq)==5:
            if seq.count(opp_piece)==5:
                score= -500000
            elif seq.count(opp_piece)==4:
                score= -10000
            elif seq.count(opp_piece)==3:
                score= -1000     
                
        elif len(seq)==6:
            if seq[0:5].count(opp_piece)==5:
                score= -300000
            elif seq[1:6].count(opp_piece)==5:
                score= -300000
            elif seq[0:5].count(opp_piece)==4:
                score= -20000
            elif seq[1:6].count(opp_piece)==4:
                score= -20000
            elif seq[0:5].count(opp_piece)==3:
                score= -1000
            elif seq[1:6].count(opp_piece)==3:
                score= -1000
        
        return score
    
    def positive_score(seq: list[int], player_piece: int):
        score=0
        if len(seq)==5:
            if seq.count(player_piece)==5:
                score= 1000000
            elif seq.count(player_piece)==4:
                score= 100000
            elif seq.count(player_piece)==3:
                score= 20000
            elif seq.count(player_piece)==2:
                score= 100
            elif seq.count(player_piece)==1:
                score= 1
                
        elif len(seq)==6:
            
            if seq[0:5].count(player_piece)==5:
                score= 1000000
            elif seq[1:6].count(player_piece)==5:
                score= 1000000
            elif seq[0:5].count(player_piece)==4:
                score= 100000
            elif seq[1:6].count(player_piece)==4:
                score= 100000
            elif seq[0:5].count(player_piece)==3:
                score= 20000
            elif seq[1:6].count(player_piece)==3:
                score= 20000
            elif seq[0:5].count(player_piece)==2:
                score= 200
            elif seq[1:6].count(player_piece)==2:
                score= 200
            elif seq[0:5].count(player_piece)==1:
                score= 10
            elif seq[1:6].count(player_piece)==1:
                score= 10
        
        return score
    
    def evaluate(self, board):
        valid = BoardUtility.get_valid_locations(board)
        score=0
        
        for i in range(6):
            if (self.player_piece in board[i][1:5]) or (board[i][0]==self.player_piece and board[i][5]==self.player_piece):
                continue
            else:
                if board[i][0]==self.player_piece:
                    score = score + MiniMaxPlayer.negative_score(board[i][1:6], self.opp_piece)
                elif board[i][5]==self.player_piece:
                    score = score + MiniMaxPlayer.negative_score(board[i][0:5], self.opp_piece)
                else:
                    score = score + MiniMaxPlayer.negative_score(board[i], self.opp_piece)
        
        transposed_board = np.array(board).T.tolist()
        for i in range(6):
            if (self.player_piece in transposed_board[i][1:5]) or (transposed_board[i][0]==self.player_piece and transposed_board[i][5]==self.player_piece):
                continue
            else:
                if transposed_board[i][0]==self.player_piece:
                    score = score + MiniMaxPlayer.negative_score(transposed_board[i][1:6], self.opp_piece)
                elif transposed_board[i][5]==self.player_piece:
                    score = score + MiniMaxPlayer.negative_score(transposed_board[i][0:5], self.opp_piece)
                else:
                    score = score + MiniMaxPlayer.negative_score(transposed_board[i], self.opp_piece)
                
        seq = []
        seq.append([board[0][0],board[1][1],board[2][2],board[3][3],board[4][4],board[5][5]])
        seq.append([board[0][5],board[1][4],board[2][3],board[3][2],board[4][1],board[5][0]])
        
        for i in range(len(seq)):
            if (self.player_piece in seq[i][1:5]) or (seq[i][0] == self.player_piece and seq[i][5] == self.player_piece):
                continue
            else:
                if seq[i][0] == self.player_piece:
                    score = score + MiniMaxPlayer.negative_score(seq[i][1:6], self.opp_piece)
                elif seq[i][5] == self.player_piece:
                    score = score + MiniMaxPlayer.negative_score(seq[i][0:5], self.opp_piece)
                else:
                    score = score + MiniMaxPlayer.negative_score(seq[i], self.opp_piece)
                    
        for i in range(len(seq)):
            if (self.opp_piece in seq[i][1:5]) or (seq[i][0] == self.opp_piece and seq[i][5] == self.opp_piece):
                continue
            else:
                if seq[i][0] == self.opp_piece:
                    score = score + MiniMaxPlayer.positive_score(seq[i][1:6], self.player_piece)
                elif seq[i][5] == self.opp_piece:
                    score = score + MiniMaxPlayer.positive_score(seq[i][0:5], self.player_piece)
                else:
                    score = score + MiniMaxPlayer.positive_score(seq[i], self.player_piece)
        
        seq = []
        seq.append([board[0][1],board[1][2],board[2][3],board[3][4],board[4][5]])
        seq.append([board[1][0],board[2][1],board[3][2],board[4][3],board[5][4]])
        seq.append([board[0][4],board[1][3],board[2][2],board[3][1],board[4][0]])
        seq.append([board[1][5],board[2][4],board[3][3],board[4][2],board[5][1]])
        
        for i in range(len(seq)):
            if self.player_piece in seq[i]:
                continue
            else:
                score = score + MiniMaxPlayer.negative_score(seq[i], self.opp_piece)
        for i in range(len(seq)):
            if self.opp_piece in seq[i]:
                continue
            else:
                score = score + MiniMaxPlayer.positive_score(seq[i], self.player_piece)
        
        for i in range(6):
            if (self.opp_piece in board[i][1:5]) or (board[i][0]==self.opp_piece and board[i][5]==self.opp_piece):
                continue
            else:
                if board[i][0]==self.opp_piece:
                    score = score + MiniMaxPlayer.positive_score(board[i][1:6], self.player_piece)
                elif board[i][5]==self.opp_piece:
                    score = score + MiniMaxPlayer.positive_score(board[i][0:5], self.player_piece)
                else:
                    score = score + MiniMaxPlayer.positive_score(board[i], self.player_piece)
                    
        transposed_board = np.array(board).T.tolist()
        for i in range(6):
            if (self.opp_piece in transposed_board[i][1:5]) or (transposed_board[i][0]==self.opp_piece and transposed_board[i][5]==self.opp_piece):
                continue
            else:
                if transposed_board[i][0]==self.opp_piece:
                    score = score + MiniMaxPlayer.positive_score(transposed_board[i][1:6], self.player_piece)
                elif transposed_board[i][5]==self.opp_piece:
                    score = score + MiniMaxPlayer.positive_score(transposed_board[i][0:5], self.player_piece)
                else:
                    score = score + MiniMaxPlayer.positive_score(transposed_board[i], self.player_piece)

        
        return score
    
    
    def temp_play(self, temp_board, depth_tracker, valid_locations, max_score):
        
        original_board = copy.deepcopy(temp_board)
        for i in reversed(range(self.depth)):
            if depth_tracker[i][2] == "clockwise":
                depth_tracker[i][2] = "anticlockwise"
                MiniMaxPlayer.make_move(temp_board[i],depth_tracker[i][0][0],depth_tracker[i][0][1],depth_tracker[i][1],depth_tracker[i][2],self.player_piece)
                
                if i!=self.depth-1:
                    for j in range(i+1,self.depth):
                        valid_locations[j]=BoardUtility.get_valid_locations(temp_board[j-1])

                        depth_tracker[j][1]=0
                        depth_tracker[j][2] = "clockwise"
                        depth_tracker[j][0][0] = valid_locations[j][0][0]
                        depth_tracker[j][0][1] = valid_locations[j][0][1]
                        del valid_locations[j][0]
                        temp_board[j]=copy.deepcopy(temp_board[j-1])
                        original_board[j]=copy.deepcopy(temp_board[j-1])
                        MiniMaxPlayer.make_move(temp_board[j],depth_tracker[j][0][0],depth_tracker[j][0][1],depth_tracker[j][1],depth_tracker[j][2],self.player_piece)

                
                score = MiniMaxPlayer.evaluate(self,temp_board[i])
                if score>max_score:
                    max_score = copy.deepcopy(score)
                    self.best_move = copy.deepcopy(depth_tracker[0])
                    
                MiniMaxPlayer.temp_play(self, original_board, depth_tracker, valid_locations,max_score)
                
            else:
                if depth_tracker[i][1] !=4:
                    depth_tracker[i][1]=depth_tracker[i][1]+1
                    depth_tracker[i][2] = "clockwise"
                    MiniMaxPlayer.make_move(temp_board[i],depth_tracker[i][0][0],depth_tracker[i][0][1],depth_tracker[i][1],depth_tracker[i][2],self.player_piece)
                    
                    if i!=self.depth-1:
                        for j in range(i+1,self.depth):
                            valid_locations[j]=BoardUtility.get_valid_locations(temp_board[j-1])

                            depth_tracker[j][1]=0
                            depth_tracker[j][2] = "clockwise"
                            depth_tracker[j][0][0] = valid_locations[j][0][0]
                            depth_tracker[j][0][1] = valid_locations[j][0][1]
                            del valid_locations[j][0]
                            temp_board[j]=copy.deepcopy(temp_board[j-1])
                            original_board[j]=copy.deepcopy(temp_board[j-1])
                            MiniMaxPlayer.make_move(temp_board[j],depth_tracker[j][0][0],depth_tracker[j][0][1],depth_tracker[j][1],depth_tracker[j][2],self.player_piece)

                    score = MiniMaxPlayer.evaluate(self,temp_board[i])
                    if score>max_score:
                        max_score = copy.deepcopy(score)
                        self.best_move = copy.deepcopy(depth_tracker[0]) 
                    
                    MiniMaxPlayer.temp_play(self, original_board, depth_tracker, valid_locations,max_score)
                else:
                    if len(valid_locations[i])!=0:
                        depth_tracker[i][1]=0
                        depth_tracker[i][2] = "clockwise"
                        del valid_locations[i][0]
                        if len(valid_locations[i])==0:
                            if i==0:
                                
                                return self.best_move
                                break
                            continue
                        depth_tracker[i][0][0] = valid_locations[i][0][0]
                        depth_tracker[i][0][1] = valid_locations[i][0][1]
                        MiniMaxPlayer.make_move(temp_board[i],depth_tracker[i][0][0],depth_tracker[i][0][1],depth_tracker[i][1],depth_tracker[i][2],self.player_piece)
                        
                        if i!=self.depth-1:
                            for j in range(i+1,self.depth):
                                valid_locations[j]=BoardUtility.get_valid_locations(temp_board[j-1])

                                depth_tracker[j][1]=0
                                depth_tracker[j][2] = "clockwise"
                                depth_tracker[j][0][0] = valid_locations[j][0][0]
                                depth_tracker[j][0][1] = valid_locations[j][0][1]
                                del valid_locations[j][0]
                                temp_board[j]=copy.deepcopy(temp_board[j-1])
                                original_board[j]=copy.deepcopy(temp_board[j-1])
                                MiniMaxPlayer.make_move(temp_board[j],depth_tracker[j][0][0],depth_tracker[j][0][1],depth_tracker[j][1],depth_tracker[j][2],self.player_piece)
                        
                        score = MiniMaxPlayer.evaluate(self,temp_board[i])
                        if score>max_score:
                            max_score = copy.deepcopy(score)
                            self.best_move = copy.deepcopy(depth_tracker[0])

                            
                        MiniMaxPlayer.temp_play(self, original_board, depth_tracker, valid_locations,max_score)
                    else:
                        continue
                                             
        return self.best_move
    
    
    def play(self, board):
        
        depth_tracker = [[[None,None],None,None] for i in range(self.depth)]
        temp_board = copy.deepcopy(board.tolist())
        valid_locations = []
        original_board = []
        
        for i in range(self.depth):
            original_board.append(copy.deepcopy(temp_board))
            valid_locations.append(BoardUtility.get_valid_locations(temp_board))
            depth_tracker[i] = [BoardUtility.get_valid_locations(temp_board)[0], 1, "clockwise"]
            if i%2==0:
                piece = self.player_piece
            else:
                piece = self.opp_piece
            MiniMaxPlayer.make_move(temp_board,depth_tracker[i][0][0],depth_tracker[i][0][1],depth_tracker[i][1],depth_tracker[i][2],piece)
        

        max_score=-10000
        move = copy.deepcopy(depth_tracker[0])
        
        r = random.random()
        if r>self.prob_stochastic:
            best = MiniMaxPlayer.temp_play(self, original_board, depth_tracker,valid_locations, max_score)
            row = best[0][0]
            col = best[0][1]
            region = best[1]
            rotation = best[2]
        else:
            [row,col] = random.choice(BoardUtility.get_valid_locations(board))
            region = random.choice([1, 2, 3, 4])
            rotation = random.choice(["clockwise", "anticlockwise"])
            
            
        # Todo: implement minimax algorithm
        #print(MiniMaxPlayer.evaluate(self,board))
        return [[row, col], region, rotation]
