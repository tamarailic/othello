from board import State
from copy import deepcopy
from random import randint
from game_tree import GameTree,GameTreeNode
import time
from visited_tables import VisitedTables

class Game(object):
    #white is minimizer
    #black is maximizer
    def __init__(self):
        self.current_state=State()
        self.current_player='B'
        self.hashing_object=Zobrist_Hash()
        self.game_tree=GameTree(GameTreeNode(self.current_state))
        self.visited_tables=VisitedTables()
        self.ai_depth=4
        self.visits=0

    def play(self):
        while not self.current_state.is_end:
            print(self.current_state)
            if self.current_player=='B':
                choices=self.current_state.black_valid_moves
                if choices=={}:
                    print('You have no available moves.')
                    self.change_player_turn()
                else:
                    for choice in choices:
                        print(str(choice)+') Position x:'+str(choices[choice][1])+' y:'+str(choices[choice][0]))
                    while True:
                        try:
                            answer=input('Your choice: ')
                            self.make_move(self.current_state,choices[int(answer)],self.current_player)
                            self.change_player_turn()
                            break
                        except:
                            print('Choose one of the given options.')
            else:
                if self.current_state.white_valid_moves=={}:
                    self.change_player_turn()
                    print('No available moves.')
                    continue
                else:
                    start=time.time()
                    min,y,x=self.min(self.ai_depth, -100000000000, 100000000000,self.game_tree.root)
                    duration=time.time() - start
                    print('Visited hashmap ',str(self.visits))
                    self.visits=0
                    print('Depth ', str(self.ai_depth))
                    self.adjust_depth(duration)
                    print('Size of hashmap ',str(self.visited_tables.size))
                    print('Time it took to make a move:', str(duration))
                    self.make_move(self.current_state,[y,x], self.current_player)
                    self.change_player_turn()

        print(self.current_state)
        print('Game over.')

    def adjust_depth(self,time):
        if self.current_state.nones<20:
            self.ai_depth=6
        elif time>2.5:
            self.ai_depth-=1
        elif self.ai_depth<4 and time<0.1:
            self.ai_depth+=1

    def change_player_turn(self):
        if self.current_player=='B':
            self.current_player ='W'
        else:
            self.current_player='B'

    def make_move(self,board,position,player_color):
        board.flip_board(position,player_color)
        return board

    def heuristic_function(self,current_state):
        x_directions=[-1, -1, 0, 1, 1, 1, 0, -1]
        y_directions=[0, 1, 1, 1, 0, -1, -1, -1]

        value_table=[[20, -3, 11, 8, 8, 11, -3, 20],
                     [-3, -7, -4, 1, 1, -4, -7, -3],
                     [11, -4, 2, 2, 2, 2, -4, 11],
                     [8, 1, 2, -3, -3, 2, 1, 8],
                     [8, 1, 2, -3, -3, 2, 1, 8],
                     [11, -4, 2, 2, 2, 2, -4, 11],
                     [-3, -7, -4, 1, 1, -4, -7, -3],
                     [20, -3, 11, 8, 8, 11, -3, 20]]
        player_points=0
        opp_player_points=0
        player_front_spots=0
        opp_player_front_spots=0
        difference=0
        player_color='B'
        opp_player='W'
        board=current_state.board
        for i in range(8):
            for j in range(8):
                if board[i][j]==player_color:
                    difference+=value_table[i][j]
                    player_points+=1
                elif board[i][j]==opp_player:
                    difference-=value_table[i][j]
                    opp_player_points+=1
                if board[i][j]!=None:
                    for k in range(8):
                        y=i+y_directions[k]
                        x=j+x_directions[k]
                        if x>=0 and x<8 and y>=0 and y<8 and board[y][x]==None:
                            if board[i][j]==player_color:
                                player_front_spots+=1
                            else:
                                opp_player_front_spots+=1
                                break

        #coin parity
        if player_points > opp_player_points:
            points = (100.0 * player_points) / (player_points + opp_player_points)
        elif player_points < opp_player_points:
            points = -(100.0 * opp_player_points) / (player_points + opp_player_points)
        else:
            points = 0

        #front spots
        if player_front_spots > opp_player_front_spots:
            fronts = -(100.0 * player_front_spots) / (player_front_spots + opp_player_front_spots)
        elif player_front_spots < opp_player_front_spots:
            fronts = (100.0 * opp_player_front_spots) / (player_front_spots + opp_player_front_spots)
        else:
            fronts = 0

        #corners occupied
        player_points = 0
        opp_player_points = 0
        if board[0][0] == player_color:
            player_points+=1
        elif board[0][0] == opp_player:
            opp_player_points+=1
        if board[0][7] == player_color:
            player_points += 1
        elif board[0][7] == opp_player:
            opp_player_points += 1
        if board[7][0] == player_color:
            player_points+=1
        elif board[7][0] == opp_player:
            opp_player_points+=1
        if board[7][7] == player_color:
            player_points+=1
        elif board[7][7] == opp_player:
            opp_player_points+=1
        corners = 25 * (player_points - opp_player_points)

        #closness to corners
        player_points = 0
        opp_player_points = 0
        if board[0][0] == None:
            if board[0][1] == player_color:
                player_points+=1
            elif board[0][1] == opp_player:
                opp_player_points+=1
            if board[1][1] == player_color:
                player_points += 1
            elif board[1][1] == opp_player:
                opp_player_points += 1
            if board[1][0] == player_color:
                player_points+=1
            elif board[1][0] == opp_player:
                opp_player_points+=1

        if board[0][7] == None:
            if board[0][6] == player_color:
                player_points+=1
            elif board[0][6] == opp_player:
                opp_player_points+=1
            if board[1][6] == player_color:
                player_points += 1
            elif board[1][6] == opp_player:
                opp_player_points += 1
            if board[1][7] == player_color:
                player_points+=1
            elif board[1][7] == opp_player:
                opp_player_points+=1

        if board[7][0] == None:
            if board[7][1] == player_color:
                player_points+=1
            elif board[7][1] == opp_player:
                opp_player_points+=1
            if board[6][1] == player_color:
                player_points += 1
            elif board[6][1] == opp_player:
                opp_player_points += 1
            if board[6][0] == player_color:
                player_points+=1
            elif board[6][0] == opp_player:
                opp_player_points+=1

        if board[7][7] == None:
            if board[6][7] == player_color:
                player_points+=1
            elif board[6][7] == opp_player:
                opp_player_points+=1
            if board[6][6] == player_color:
                player_points += 1
            elif board[6][6] == opp_player:
                opp_player_points += 1
            if board[7][6] == player_color:
                player_points+=1
            elif board[7][6] == opp_player:
                opp_player_points+=1
        closeness = -12.5 * (player_points - opp_player_points)

        #mobility
        player_points = len(current_state.get_valid_moves(player_color))
        opp_player_points = len(current_state.get_valid_moves(opp_player))
        if player_points > opp_player_points:
            mobility = (100.0 * player_points) / (player_points + opp_player_points)
        elif player_points < opp_player_points:
            mobility = -(100.0 * opp_player_points) / (player_points + opp_player_points)
        else:
            mobility = 0

        score = (10 * points) + (801.724 * corners) + (382.026 * closeness) + (78.922 * mobility) + (74.396 * fronts) + (10 * difference)
        return score


    def min(self,depth,alpha,beta,node):
        min = 100000000000

        y_min = None
        x_min = None

        if node.board.is_end or depth == 0:
            return self.heuristic_function(node.board), 0, 0

        else:
            for possible_board in self.get_possible_boards(node.board,'W'):
                child = GameTreeNode(possible_board[0])
                node.add_child(child)
                index = self.hashing_object.hash(node.board)
                if index in self.visited_tables:
                    child.value=self.visited_tables[index]
                    self.visits+=1
                else:
                    child.value=self.max(depth-1,alpha,beta,child)[0]
                child.y_coordinate, child.x_coordinate=possible_board[1],possible_board[2]
                if depth!=self.ai_depth:
                    self.save_possible_board(child.board,[child.value,(self.ai_depth-depth)])

                if child.value < min:
                    min = child.value
                    y_min = child.y_coordinate
                    x_min = child.x_coordinate

                if min<beta:
                    beta=min

                if min<=alpha:
                    return min,y_min,x_min

        return min, y_min, x_min

    #alpha is min guaranteed  for max player to have
    def max(self,depth,alpha,beta,node):

        max = -100000000000

        y_max = None
        x_max = None

        if node.board.is_end or depth == 0:
            return self.heuristic_function(node.board), 0, 0

        for possible_board in self.get_possible_boards(node.board,'B'):
            child = GameTreeNode(possible_board[0])
            node.add_child(child)
            index = self.hashing_object.hash(node.board)
            if index in self.visited_tables:
                child.value=self.visited_tables[index]
                self.visits += 1
            else:
                child.value= self.min(depth - 1, alpha, beta,child)[0]
            child.y_coordinate, child.x_coordinate = possible_board[1], possible_board[2]
            if depth != self.ai_depth:
                self.save_possible_board(child.board, [child.value, (self.ai_depth-depth)])

            if child.value > max:
                max = child.value
                y_max = child.y_coordinate
                x_max = child.x_coordinate

            if max>alpha:
                alpha=max

            if alpha>=beta:
                return max,y_max,x_max

        return max, y_max, x_max

    def get_possible_boards(self,board,player_color):
        boards=[]
        for move in board.get_valid_moves(player_color).values():
            temp_board = deepcopy(board)
            new_board = self.make_move(temp_board, move, player_color)
            boards.append([new_board,move[0],move[1]])
        return boards

    def save_possible_board(self,board,values):
        key=self.hashing_object.hash(board)
        self.visited_tables[key]=values

class Zobrist_Hash(object):

    def __init__(self):
        self.tabel=self.initialize_zobrist_table()

    def initialize_zobrist_table(self):
        return [[[randint(1,2**64-1)for i in range(2)] for j in range(8)] for k in range(8)]

    def hash(self,board):
        hash_value=0
        for i in range(8):
            for j in range(8):
                if board.board[i][j]!=None:
                    random_num=self.indexing_random_num(board.board[i][j])
                    hash_value^=self.tabel[i][j][random_num]

        return hash_value

    def indexing_random_num(self,player_color):
        if player_color=='B':
            return 0
        else:
            return 1

if __name__ == '__main__':
    Game().play()
