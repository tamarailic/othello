class State(object):

    #'B' is for black and 'W' is for white

    def __init__(self):
        self.board=[]
        #initializing an empty board
        for i in range(8):
            self.board.append([None,None,None,None,None,None,None,None])

        self.board[3][3]='W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'

        self.black_points = 2
        self.white_points = 2
        self.black_valid_moves=self.valid_moves('B')
        self.white_valid_moves=self.valid_moves('W')
        self.is_end=False
        self.nones=60

    def __str__(self):
        output='  |0|1|2|3|4|5|6|7|\n'
        i=0
        for row in self.board:
            output += '|' + str(i)
            for spot in row:
                if spot==None:
                    output+='|_'
                else:
                    output+='|'+spot
            output+='|\n'
            i+=1
        output+='White:'+str(self.white_points)+'\n'
        output += 'Black:' + str(self.black_points) + '\n'
        return output

    #returns, if there is, dictionary of possible moves
    def valid_moves(self,player_color):
        moves={}
        move_num = 1
        for i in range(8):
            for j in range(8):
                if self.board[i][j]!=None:
                    continue
                else:
                    neighbors=self.find_neighbors(i,j)
                    if neighbors==[]:
                        continue
                    else:
                        for neighbor in neighbors:
                            if self.board[neighbor[0]][neighbor[1]]==player_color:
                                continue #if neighbor is the same color then we continue the search on to the next one
                            else:
                               if self.is_possible_move(i,j,neighbor[0],neighbor[1],player_color):
                                   if [i,j] not in moves.values():
                                       moves[move_num]=[i,j]
                                       move_num+=1

        return moves

    def set_valid_moves(self):
        self.black_valid_moves = self.valid_moves('B')
        self.white_valid_moves = self.valid_moves('W')
        if self.black_valid_moves=={} and self.white_valid_moves=={}:#only if both players have no moves left to play game ends
            self.is_end=True

    def get_valid_moves(self,player_color):
        if player_color=='B':
            return self.black_valid_moves
        else:
            return self.white_valid_moves

    def opposite_player(self,player_color):
        if player_color=='B':
            return 'W'
        else:return 'B'

     #checks if a given position has a taken spot around it
    def find_neighbors(self,y_coordinate,x_coordinate):
        neighbors=[]
        for i in range(max(0,(y_coordinate-1)),min((y_coordinate+2),8)):#checking indexes so we don't go out of board
            for j in range(max(0, (x_coordinate - 1)), min((x_coordinate + 2), 8)):
                if self.board[i][j]!=None:
                    neighbors.append([i,j])
        return neighbors

    def is_possible_move(self,y_coordinate,x_coordinate,y_neighbor,x_neighbor,player_color):
        y_direction=y_neighbor-y_coordinate #determines in which direction we will check following spots on board
        x_direction=x_neighbor-x_coordinate
        y_current=y_neighbor
        x_current=x_neighbor

        while 0<=y_current<=7 and 0<=x_current<=7:
            if self.board[y_current][x_current]==None:
                return False
            if self.board[y_current][x_current]==player_color:#if we find same color it's a valid spot
                return True
            y_current+=y_direction
            x_current+=x_direction

        return False

    def spots_to_change(self,y_direction,x_direction,y_current,x_current,player_color):
        spots=[]

        while 0 <= y_current <= 7 and 0 <=x_current <= 7:
            if self.board[y_current][x_current]==None: #if on the other side of that direction there is no current players spot then just return from the function
                return
            if self.board[y_current][x_current] == player_color:
                return self.change_spots(spots,player_color)
            spots.append([y_current,x_current])
            y_current += y_direction
            x_current += x_direction

    def change_spots(self,array_of_spots,player_color):
        for spot in array_of_spots:
            self.board[spot[0]][spot[1]]=player_color

    # fliping colors on board after one player makes a valid move
    def flip_board(self,spot_coordinates,player_color):
        for neighbor in self.find_neighbors(spot_coordinates[0],spot_coordinates[1]):
            delta_x=neighbor[0]-spot_coordinates[0]
            delta_y=neighbor[1]-spot_coordinates[1]
            self.spots_to_change(delta_x,delta_y,neighbor[0],neighbor[1],player_color)
        self.board[spot_coordinates[0]][spot_coordinates[1]] = player_color
        self.set_score()
        self.nones-=1
        self.set_valid_moves()

    def set_score(self):
        self.black_points=0
        self.white_points=0
        for row in self.board:
            for spot in row:
                if spot=='B':
                    self.black_points+=1
                elif spot=='W':
                    self.white_points+=1
                else:
                    continue


