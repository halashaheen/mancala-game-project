import math
import copy

#player value
opponent, AI =  False, True

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
            
