import math

#player value
opponent, AI =  False, True

"""
checks whether the lastIndex due to the player move is its mancala index
parameters: 1- player:opponent or AI
            2- lastIndex:last move performed by player
returns: true if it is the player mancala index , false if not      
"""
def isMancalaIndex(player,lastIndex):
    if(player == AI):
        if(lastIndex ==6):  return True
        else: return False
    elif(player == opponent):
        if(lastIndex ==13): return True
        else: return False
    else:
        print("error from isMancalaIndex !!!!!!!!")
        return

"""
checks for the condition of stealing : the laststone is placed in an empty pocket belonging to the same player 
and the opposite pocket of the other player is non-empty
parameters: 1- board:mancala board
            2- lastIndex:last move performed by player
            3- player:opponent or AI
returns: true if condition of stealing is met otherwise false

"""
def isSteal(board,lastIndex,player):
    oppositeIndex = 12 -lastIndex
    #check that last index of pocket belong to player
    isBelong = belongToPlayer(player,lastIndex)
    if(isBelong):
        #if we place the last stone in an empty pocket o the player
        #and the opposite index (pocket opposite of other player) is not empty
        #condition of stealing
        if((board[lastIndex]==1) and (board[oppositeIndex]!=0)): return True
        else: return False
    else: return False

"""
find the last stone index due to move performed by player
parameters : 1- board:mancala board
             2- pocket_index : pocket played by player
returns : the last position due to this move
"""
def lastStoneIndex(board,pocket_index):
    #initializing i
    i=0
    #no of stones inside pocket
    Nstones = board[pocket_index]
    if(pocket_index >= 7):
        #opponent pockets
        #skip index = 6 (AI store) 
        passByMancala = 0
        for i in range(pocket_index+1,Nstones+pocket_index+1):
            if((i%14) == 6) :#AI store
                passByMancala +=1
        while(passByMancala>0):
            i = (i+1)%14
            if((i%14) != 6) :#AI store
                passByMancala -=1
        lastIndex = i%14
    elif(pocket_index < 6):
        #AI pockets
        #skip index = 13 (OPPONENT store) 
        passByMancala = 0
        for i in range(pocket_index+1,Nstones+pocket_index+1):
            if((i%14) == 13) :#OPPONENT store
                passByMancala +=1
        while(passByMancala>0):
            i = (i+1)%14
            if((i%14) != 13) :#OPPONENT store
                passByMancala -=1
        lastIndex = i%14
    else:
        print("error from lastStoneIndex !!!!!!!!")
        return

    return lastIndex

"""
update mancala if the condition of steal is met
parameters: 1-board:mancala board
            2-pocket_index : pocket played by player
returns: the updated board
"""
def updateBoardWithSteal(board,pocket_index):
    lastIndex = lastStoneIndex(board,pocket_index)
    oppositeIndex = 12 -lastIndex
    #AI will steal
    if(pocket_index<6):
        board[6]+=(board[oppositeIndex]+1)
        board[lastIndex] =0
        board[oppositeIndex] =0
    #opponent will steal
    elif(pocket_index>=7):
        board[13]+=(board[oppositeIndex]+1)
        board[lastIndex] =0
        board[oppositeIndex] =0
    else:
        print("error of updateBoardWithSteal !!!!!")
        return


"""
update board due to move and including if condition of stealing is met
parameters: 1-board:mancala board
            2-pocket_index : pocket played by player
returns: the updated board
"""
def updateBoard(board,pocket_index,mode):
    prevBoard = copy.deepcopy(board)
    #initializing i
    i=0
    #no of stones inside pocket
    Nstones = board[pocket_index]
    if(pocket_index >= 7):
        #opponent pockets
        #skip index = 6 (AI store) 
        passByMancala = 0
        for i in range(pocket_index+1,Nstones+pocket_index+1):
            if((i%14) == 6) :#AI store
                passByMancala +=1
            else:
                board[(i%14)]+=1
        while(passByMancala>0):
            i = (i+1)%14
            if((i%14) != 6) :#AI store
                board[i]+=1
                passByMancala -=1
        lastIndex = i%14
        playAgain = isMancalaIndex(opponent,lastIndex)
        if(mode_dict[mode]=="withStealMode"):
            #last stone not placed in the mancala
            if(not(playAgain)):
                #we check that last stone might be placed in an empty pocket of the opponent
                #opponent should steal
                if(isSteal(board,lastIndex,pocket_index,opponent)):#go prevBoard
                    updateBoardWithSteal(board,pocket_index)
                    #even if last stone is placed in same pocket played
                    #opponent will steal
                    if(pocket_index == lastIndex):
                        board[pocket_index] += Nstones                    
    elif(pocket_index < 6):
        #AI pockets
        #skip index = 13 (OPPONENT store) 
        passByMancala = 0
        for i in range(pocket_index+1,Nstones+pocket_index+1):
            if((i%14) == 13) :#OPPONENT store
                passByMancala +=1
            else:
                board[(i%14)]+=1
        while(passByMancala>0):
            i = (i+1)%14
            if((i%14) != 13) :#OPPONENT store
                board[i]+=1
                passByMancala -=1
        lastIndex = i%14
        playAgain = isMancalaIndex(AI,lastIndex)
        if(mode_dict[mode]=="withStealMode"):
            #last stone not placed in the mancala
            if(not(playAgain)):
                #we check that last stone might be placed in an empty pocket of the AI
                #AI should steal
                if(isSteal(board,lastIndex,pocket_index,AI)):
                    updateBoardWithSteal(board,pocket_index)
                    #even if last stone is placed in same pocket played
                    #AI will steal
                    if(pocket_index == lastIndex):
                        board[pocket_index] += Nstones
    else:
        print("error from upadateBoard !!!!!!!!")
        return
    #empty the current pocket
    board[pocket_index] -= Nstones
    return playAgain
