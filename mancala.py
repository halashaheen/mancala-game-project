import math
import copy
import pickle

#player value
opponent, AI =  False, True

def printMancala(mancala_board):
    """
    parameters: the current mancala board you want to print
    it prints the mancala in a good way to see how the current state of the mancala is
    returns: None
    """
     
    #visulaization of mancala board 
    print('  Opp   pckt12  pckt11  pckt10  pckt9   pckt8   pckt7 ')
    print('------- ------- ------- ------- ------- ------- ------- -------')
    print('|     | |  %2d | |  %2d | |  %2d | |  %2d | |  %2d | |  %2d | |     |'%(mancala_board[12],mancala_board[11],mancala_board[10],mancala_board[9],mancala_board[8],mancala_board[7]))
    print('| %2d  | ------- ------- ------- ------- ------- ------- | %2d  |'%(mancala_board[13],mancala_board[6]))
    print('|     | ------- ------- ------- ------- ------- ------- |     |')
    print('|     | |  %2d | |  %2d | |  %2d | |  %2d | |  %2d | |  %2d | |     |'%(mancala_board[0],mancala_board[1],mancala_board[2],mancala_board[3],mancala_board[4],mancala_board[5]))
    print('------- ------- ------- ------- ------- ------- ------- -------')
    print('         pckt0    pckt1   pckt2  pckt3   pckt4   pckt5     AI  ')
    print()


def evaluate(board):
    """
    parameters: mancala current board
    it returns the difference of the number of stones in the AI's mancala and opponent's mancala, +ve means AI is the winner , -ve means AI is the loser
    return: the score (AI's mancala number of stones - opponent's mancala number of stones)
    """
    return board[6]-board[13]


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

"""
display image when the opponent loses
parameters: none
returns:none
"""
def Loser():
    print(" \|/ ____ \|/")       
    print("  @~/ ,. \~@ ")      
    print("./_( \__/ )_\.")      
    print("    \__U_/   ")
    print("")

"""
display image when the opponent wins
parameters: none
returns:none
"""
def winner():
    print("  _________ ")
    print("@/         \@")
    print("\|  /\ /\  |/")
    print(" |    -    |")
    print(" |  \___/  |")
    print(" \_________/")
    print()

"""
check whether the pocket is empty or not
parameters: 1- board:mancala board
            2- pocket_index : the index of the pocket
returns: true if the pocket at that index is empty or not 

"""
def isPocketEmpty(board,pocket_index):
    if(board[pocket_index] ==0):
        return True
    else : return False

"""
check whether the all mancala pocket are empty or not
parameters: 1- board:mancala board
            2- player:opponent or AI
returns: true if the all pockets are empty or not 

"""
def AllPocketsEmpty(board,player):
    if(player == AI):
        for i in range(6):
            if(not(isPocketEmpty(board,i))):
                return False
        return True
    elif(player == opponent):
        for i in range(7,13):
            if(not(isPocketEmpty(board,i))):
                return False
        return True
    else :
        print("player entered is not defined !!!")
        return

#stopping condition
#returns whether stop condition is true or false
#modified board in case of stop condition is true

"""
returns whether stop condition is true or false
parameters: 1- board:mancala board
            2- player:opponent or AI
returns: true if the stop played condition is met otherwise false

"""
def stopPlay(board,player):
    #AI pockets are all empty
    if(player == AI):
        for i in range(6):
            if(board[i]!=0):
                return board,False
        #modify Mancala from opponent side
        for j in range(7,13):
            board[13] += board[j]
            board[j]=0
        return board,True
    #opponent pockets are all empty
    elif(player == opponent):
        for i in range(7,13):
            if(board[i]!=0):
                return board,False
        #modify Mancala from AI side
        for j in range(6):
            board[6] += board[j]
            board[j]=0
        return board,True
    else:
        print("error from stopPlay !!!!")
        return
        
"""
perform the opponent move based on the choosen pocket
parameters: 1- board:mancala board
            2- mode:with/without stealing
            3- endOfGame:boolean represents whether the game ends or not
returns: the updated board after opponent move

"""

def oppMove(board,mode,endOfGame):
    board,StopPlayOpponent = stopPlay(board,opponent)
    if(not(StopPlayOpponent)):#and (not(StopPlayAI)) ) 
        print(bcolors.blue+"*****************************opponent turn**************************************")
        print("please enter the pocket number you want to move its stones")
        print("ALLOWED POCKET NUMBER : 7,8,9,10,11,12")
        print("pocket no = ",end="")
        pocket_no = int(input())
        print(bcolors.RESET)
        #checking validity of input pocket number
        if(pocket_no <= 6 or pocket_no >= 13):
            print(bcolors.red+"INVALID POCKET NUMBER !!!!!" + bcolors.RESET)
            oppMove(board,mode,False)
        #check if pocket is empty
        elif(isPocketEmpty(board,pocket_no)):
            print( bcolors.red+"POCKET IS EMPTY !!!, choose a non-empty pocket"+ bcolors.RESET)
            oppMove(board,mode,False)
        else:
            boardBeforeUpdate = copy.deepcopy(board)
            playAgain = updateBoard(board,pocket_no,mode)
            if(mode_dict[mode]=="withStealMode"):
                printSteal(boardBeforeUpdate,board,pocket_no)
            printMancala(board)
            board,StopPlayOpponent = stopPlay(board,opponent)
            end = endGame(board)
            if(StopPlayOpponent and not(endOfGame)):#remove if((StopPlayOpponent or StopPlayAI) and not(end)):
                print(bcolors.purple+"*****************************END OF GAME****************************************"+bcolors.RESET)
                printMancala(board)
                printWinner(board)
                endOfGame = True
            #last stone is placed inside the player's mancala 
            #the player will take another turn
            if(playAgain):
                oppMove(board,mode,endOfGame)
            return
    else:
        if(not(endOfGame)):
            print(bcolors.purple+"*****************************END OF GAME****************************************"+bcolors.RESET)
            printMancala(board)
            printWinner(board)
            endOfGame = True
        else:
            return
            
def playAgain(board,pocket_index):
    """
    parameters: mancala board, the played pocket index
    this function checks if the last stone is placed in the player's mancala so he should play again
    retrun: True if he should play again, false if not
    """
    if(pocket_index >= 7):
        #opponent pockets
        if(13-pocket_index == board[pocket_index]):
            return True
        else: return False
    elif(pocket_index < 6):
        #AI pockets
        if(6-pocket_index == board[pocket_index]):
            return True
        else: return False
    else: 
        print("error from playAgain !!!!!!!!")
        return

def minimax(board,mode,depth,depthMax,player,alpha,beta):
    """
    paramters: mancala board, mode of the game, depth of the tree, player: true if AI false if opponent, alpha and beta parameters
    this is the main function of the whole game, it returns the best score that AI can acheive by making a certain move, it searches the tree to a certain depth
    determined based on the level of the game, it uses alpha beta pruning to cut off the unnecessary branches to make the search faster
    return: best score
    """
    #check stop condition for AI
    _,StopPlayAI = stopPlay(board,AI)
    #check stop condition for  opponent
    _,StopPlayOpp = stopPlay(board,opponent)

    depthLimit = False
    if(depth>=depthMax): depthLimit = True

    #check the result of game
    if(StopPlayAI or StopPlayOpp or depthLimit):
        # return evaluateWrtDepth(board,player,depth)  #hard level evaluation function
        return evaluateWrtDepth(board,player)
    else:
        #AI turn
        if(player == AI):
            #saving our board before any moves
            prevBoard = copy.deepcopy(board)
            bestScore = -1000
            #loop over AI possible moves
            for i in range(6):
                if(not(isPocketEmpty(board,i))):
                    #move
                    playAgain = updateBoard(board,i,mode)
                    if(playAgain):
                        score = minimax(board,mode,depth+1,depthMax,AI,alpha,beta)
                        #undo
                        board=copy.deepcopy(prevBoard) 
                        #evaluate best move
                        if (score > bestScore):
                            bestScore = score
                            #alpha update
                            if(alpha < bestScore):
                                alpha = bestScore
                            # Alpha Beta Pruning 
                            if beta <= alpha: 
                                break
                    else:
                        score = minimax(board,mode,depth+1,depthMax,opponent,alpha,beta)
                        #undo
                        board=copy.deepcopy(prevBoard)
                        #evaluate best move
                        if (score > bestScore):
                            bestScore = score
                            #alpha update
                            if(alpha < bestScore):
                                alpha = bestScore
                            # Alpha Beta Pruning 
                            if beta <= alpha: 
                                break
            return bestScore

        #opponent turn
        elif(player == opponent):
            #saving our board before any moves
            prevBoard = copy.deepcopy(board)
            bestScore = 1000
            #loop over opponent possible moves
            for i in range(7,13):
                if(not(isPocketEmpty(board,i))):
                    #move
                    playAgain = updateBoard(board,i,mode)
                    if(playAgain):
                        score = minimax(board,mode,depth+1,depthMax,opponent,alpha,beta)
                        #undo
                        board=copy.deepcopy(prevBoard)
                        #evaluate best move
                        if (score < bestScore):
                            bestScore = score
                            #beta update
                            if(beta > bestScore):
                                beta = bestScore
                            # Alpha Beta Pruning 
                            if beta <= alpha: 
                                break
                    else:
                        score = minimax(board,mode,depth+1,depthMax,AI,alpha,beta)
                        #undo
                        board=copy.deepcopy(prevBoard)
                        #evaluate best move
                        if (score < bestScore):
                            bestScore = score
                            #beta update
                            if(beta > bestScore):
                                beta = bestScore
                            # Alpha Beta Pruning 
                            if beta <= alpha: 
                                break
            return bestScore
        else:
            print("error in minimax !!!!!")
            return

####################################################### BONUS 1 ############################################################

def saveGame(fileName,board,player,mode,level):
    """
    parameters: the file name you want to save the game in, the board you want to save,the last played player, the mode of the game and the level
    it takes the paramters and save them in a list game in a text file
    returns: None
    """
    game= [board,player,mode,level]
    fileName = 'games/'+ fileName +'.txt'
    with open(fileName, 'wb') as f:
        pickle.dump(game,f)

def loadGame(fileName):
    """
    parameters: the file name you want to load the game from
    it opens the file and gives the saved list again to continue playing from the stopped position
    returns: gamelist 
    """
    fileName = 'games/'+ fileName +'.txt'
    buffer = open (fileName, "rb")
    game = pickle.load(buffer)
    return game