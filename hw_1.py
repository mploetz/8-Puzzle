"""
B351 - Assignment1
Author Matt Ploetz
Partner Tim Jones
"""
import copy
import random
import time
import math
import heapq
import queue

goal = [1, 2, 3, 4, 5, 6, 7, 8, " "]
def printState(board):
    b = 0
    while(b < 9):
        boardStr = ""
        c = 0
        while(c < 3):
            boardStr+="["+str(board[b+c])+"]"
            c+=1
        
        print(boardStr)
        b+=c
def checkSolvable(arr): # checks the inversions of the given board
    inversions = 0
    b = 0
    while(b < len(arr)):
        c = b+1
        while(c < len(arr)):
            if arr[c]> arr[b]:
                inversions+=1
            c+=1
        b+=1
    if (inversions%2==1):#if the inversion is odd, its unsolvable
        return False
    else:
        return True 
def genRandomBoard(): #returns a valid, but random board
    board = [1,2,3,4,5,6,7,8,0]
    random.shuffle(board)
    while(not(checkSolvable(board))):
        random.shuffle(board)
    zeroIndex = board.index(0)
    board[zeroIndex]=" "
    return board

def BFS(state, goal, limit):
    printState(state)
    frontier = []
    frontier.append(makeNode(state,None,0,0))
    explored = dict()
    counter = 0
    while(True):
        if len(frontier)==0: return print("Path is not found")
        nextNode = frontier.pop()
        if nextNode.state == goal:
            moves = []
            temp = nextNode
            cost = nextNode.cost
            while(True):
                state = temp.state
                moves.append(state)
                if temp.depth==0:
                    break
                temp = temp.parent
            print("Start")
            moves.reverse()
          #  if len(moves) < 200: # printing is limited to 200
          #          for i in moves:
          #              printState(i)
          #              print("")
          #          print("Goal Above")
            print("Total Moves Needed %i" % (len(moves)-1))
            break
           # return moves
        else:
            temp = nextNode.state
            explored[str(temp)]=True

        counter+=1
        if(counter > limit):
            return print("Reached limit of moves")
        expand = expandNodeUninformed(nextNode,explored)
        for i in expand:
            frontier.append(i)

#BFS([1,2,3,4,5,6,7," ",8],[1,2,3,4,5,6,7,8," "])
#BFS([8," ",6,5,4,7,2,3,1],[1,2,3,4,5,6,7,8," "])

def Astar(state, goal, limit):
    printState(state)
    frontier = queue.PriorityQueue()
    frontier.put((0,0,makeNode(state,None,0,0)))
    explored = dict()
    counter = 0
    count = 0
    while(True):
        if frontier.empty(): return print("No path found")
        currentTuple = frontier.get()
        nextNode = currentTuple[2]
        if nextNode.state == goal:
            moves = []
            temp = nextNode
            while(True):
                state = temp.state
                moves.append(state)
                if temp.depth==0:
                    break
                temp = temp.parent
            print("Start")
            moves.reverse()
          #  if len(moves) < 200: # Will print all states if moves is < 200
          #          for i in moves:
          #              printState(i)
          #              print("")
            print("Total Moves Needed %i" % (len(moves) - 1))
            break 
        else:
            temp = nextNode.state
            explored[str(temp)]=True
        counter+=1
        if(counter > limit):
            return print("Reached limit of moves")
        expand = expandNodeInformed(nextNode)
        for i in expand:
            if None == explored.get(str(i.state)):
                count+=1
                cost= movesNeeded(i.state,goal)
                frontier.put((cost,count,i))
                explored[str(i.state)] = i.cost
            else:
                oldNode = explored.get(str(i.state))
                if oldNode> i.cost:
                    del explored[str(i.state)]
                    explored[str(i.state)] = i.cost
                    count+=1
                    cost= movesNeeded(i.state,goal)
                    frontier.put((cost,count,i))

# 2.0
def Astarier(state, goal, limit):
    printState(state)
    frontier = queue.PriorityQueue()
    frontier.put((0,0,makeNode(state,None,0,0)))
    explored = dict()
    counter = 0
    count = 0
    while(True):
        if frontier.empty(): return print("No path found")
        currentTuple = frontier.get()
        nextNode = currentTuple[2]
        if nextNode.state == goal:
            moves = []
            temp = nextNode
            while(True):
                state = temp.state
                moves.append(state)
                if temp.depth==0:
                    break
                temp = temp.parent
            print("Start")
            moves.reverse()
           # if len(moves) < limit: # Will print all states if moves is < limit
           #         for i in moves:
           #             printState(i)
           #             print("")
            print("Total Moves Needed %i" % (len(moves) - 1))
            break 
        else:
            temp = nextNode.state
            explored[str(temp)]=nextNode.cost
        counter+=1
        if(counter > limit):
            return print("Reached limit of moves")
        expand = expandNodeInformed(nextNode)
        tuples = []
        for i in expand:
            if None == explored.get(str(i.state)):
                count+=1
                cost= movesNeeded2(i.state,goal)
                frontier.put((cost,count,i))
                explored[str(i.state)] = i.cost
            else:
                oldNode = explored.get(str(i.state))
                if oldNode> i.cost:
                    del explored[str(i.state)]
                    explored[str(i.state)] = i.cost
                    count+=1
                    cost= movesNeeded2(i.state,goal)
                    frontier.put((cost,count,i))
                
                    
        #tuples.sort(reverse=True, key=lambda s: s[0])
        #for i in tuples:
        #    frontier.append(i[1])


def movesNeeded(state,goal): #a star helper by computing the distance between points
    needed = 0
    for i in state:
        index = goal.index(i)
        stateIndex = state.index(i)
        if index != stateIndex:
            needed+= abs(stateIndex/9-index/9)+abs(stateIndex%9-index%9)
    return needed

def movesNeeded2(state,goal): #a star helper by computing the distance between points
    sumDist = 0
    for i in state:
        index = goal.index(i)
        stateIndex = state.index(i)            
        if stateIndex != index:
            sumDist += (index - stateIndex)**2
    return sumDist

def testInformedSearch(init,goal,limit):
    print("Starting Informed Search")
    Astar(init,goal,limit)

def testUninformedSearch(init,goal,limit):
    print("Starting Uninformed Search")
    BFS(init,goal,limit)

def testInformedSearch2(initialState, goalState, limit):
    print("Starting Informed Search (2.0)")
    Astarier(initialState, goalState, limit)

def makeState(nw,n,ne,w,c,e,sw,s,se):
    newState = [nw,n,ne,w,c,e,sw,s,se]
    return newState
def makeNode(state, parent, depth, pathCost):
   return Node(state,parent, depth,pathCost)


class Node :
	def __init__( self, state, parent, depth, cost):
		self.state = state
		self.parent = parent
		self.depth = depth
		self.cost = cost

def expandNodeUninformed(node, explored):
    expandedNodes = []
    up =(makeNode(moveUp(node.state),node,node.depth+1,node.cost+1))
    if up.state != None and None == explored.get(str(up.state)):
        expandedNodes.append(up)
    down =(makeNode(moveDown(node.state),node,node.depth+1,node.cost+1))
    if down.state != None and None == explored.get(str(down.state)):
        expandedNodes.append(down)
    left =(makeNode(moveLeft(node.state),node,node.depth+1,node.cost+1))
    if left.state != None and None == explored.get(str(left.state)):
        expandedNodes.append(left)
    right =(makeNode(moveRight(node.state),node,node.depth+1,node.cost+1))
    if right.state != None and  None == explored.get(str(right.state)):
        expandedNodes.append(right)
    return expandedNodes
def expandNodeInformed(node):
    expandedNodes = []
    up =(makeNode(moveUp(node.state),node,node.depth+1,node.cost+1))
    if up.state != None:
        expandedNodes.append(up)
    down =(makeNode(moveDown(node.state),node,node.depth+1,node.cost+1))
    if down.state != None :
        expandedNodes.append(down)
    left =(makeNode(moveLeft(node.state),node,node.depth+1,node.cost+1))
    if left.state != None:
        expandedNodes.append(left)
    right =(makeNode(moveRight(node.state),node,node.depth+1,node.cost+1))
    if right.state != None:
        expandedNodes.append(right)
    return expandedNodes

    

"""
Moving Functions
"""
# moveUp
# params State YPosition XPosition
# returns a State where the Blank is moved up one YPosition
def moveUp(state):
    newState = copy.deepcopy(state)
    index = newState.index(" ")
    if index not in [0,1,2]:
        temp = state[index-3]
        swap = state[index]
        newState[index-3]=swap
        newState[index]=temp
        return newState
    else:
        return None
# moveDown
# params State YPosition XPosition
# returns a State where the Blank is moved down one YPosition
def moveDown(state):
    newState = copy.deepcopy(state)
    index = newState.index(" ")
    if index not in [6,7,8]:
        temp = state[index+3]
        swap = state[index]
        newState[index+3]=swap
        newState[index]=temp
        return newState
    else:
        return None
# moveLeft
# params State YPosition XPosition
# returns a State where the Blank is moved left one XPosition
def moveLeft(state):
    newState = copy.deepcopy(state)
    index = newState.index(" ")
    if index not in [0,3,6]:
        temp = state[index-1]
        swap = state[index]
        newState[index-1]=swap
        newState[index]=temp
        return newState
    else:
        return None
# moveRight
# params State YPosition XPosition
# returns a State where the Blank is moved right one XPosition
def moveRight(state):
    newState = copy.deepcopy(state)
    index = newState.index(" ")
    if index not in [2,5,8]:
        temp = state[index+1]
        swap = state[index]
        newState[index+1]=swap
        newState[index]=temp
        return newState
    else:
        return None

#TESTING#
initialState = makeState(1,2,3,4,5,6,7," ",8)
goalState = makeState(1,2,3,4,5,6,7,8," ")
time1 = time.time()
testUninformedSearch(initialState,goalState,200)
time2 = time.time()
uninformed = round(time2-time1, 3)
time1 = time.time()
testInformedSearch(initialState,goalState,200)
time2 = time.time()
informedTime = round(time2-time1, 3)
print("Uninformed time: " + str(uninformed))
print("Informed time: " + str(informedTime))

# Awful boards
startState = [1, " ", 2, 3, 4, 5, 6, 7, 8]
time1 = time.time()
testUninformedSearch(startState, goalState, 500)
time2 = time.time()
uninformed = round(time2-time1, 3)
print("Uninformed time: " + str(uninformed))
time1 = time.time()
testInformedSearch(startState, goalState, 500)
time2 = time.time()
informedTime = round(time2-time1, 3)
print("Informed time: " + str(informedTime))
#time1 = time.time()
#testInformedSearch2(startState, goalState, 500)
#time2 = time.time()
#informedTime2 = round(time2-time1, 3)
#print("Informed time: " + str(informedTime2))

# Set timetest to false to stop autotest
timetest = True
if timetest:
    initialState = makeState(1,2,3,4,5,6,7," ",8)
    goalState = makeState(1,2,3,4,5,6,7,8," ")
    time1 = time.time()
    testUninformedSearch(initialState,goalState,10000)
    time2 = time.time()
    uninformed = time2-time1
    time1 = time.time()
    testInformedSearch(initialState,goalState,10000)
    time2 = time.time()
    informedTime = time2-time1
    time1 = time.time()
    testInformedSearch2(initialState,goalState,10000)
    time2 = time.time()
    informedBad = time2-time1
    print("Uninformed time: " + str(round(uninformed,3)))
    print("Informed bad time: " + str(round(informedBad,3)))
    print("Informed time: " + str(round(informedTime,3)))

    initialState = makeState(8," ",6,5,4,7,2,3,1)
    time1 = time.time()
    testUninformedSearch(initialState,goalState,100000)
    time2 = time.time()
    uninformed = time2-time1
    time1 = time.time()
    testInformedSearch(initialState,goalState,100000)
    time2 = time.time()
    informedTime = time2-time1
    time1 = time.time()
    testInformedSearch2(initialState,goalState,100000)
    time2 = time.time()
    informedBad = time2-time1
    print("Uninformed time: " + str(round(uninformed,3)))
    print("Informed bad time: " + str(round(informedBad,3)))
    print("Informed time: " + str(round(informedTime,3)))

    initialState = makeState(" ",6,7,5,4,8,2,3,1)
    time1 = time.time()
    testUninformedSearch(initialState,goalState,100000)
    time2 = time.time()
    uninformed = time2-time1
    time1 = time.time()
    testInformedSearch(initialState,goalState,100000)
    time2 = time.time()
    informedTime = time2-time1
    time1 = time.time()
    testInformedSearch2(initialState,goalState,100000)
    time2 = time.time()
    informedBad = time2-time1
    print("Uninformed time: " + str(round(uninformed,3)))
    print("Informed bad time: " + str(round(informedBad,3)))
    print("Informed time: " + str(round(informedTime,3)))

#Testing random boards
b = 0
while(b < 10):
    testInformedSearch(genRandomBoard(),goalState, 500)
    b+=1
# informed 2.0
i = 0
while i < 10:
    #testInformedSearch2(genRandomBoard(), goalState, 500)
    i += 1
