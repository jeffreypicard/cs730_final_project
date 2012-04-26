'''
StateNode.py

Author Jeffrey Picard
'''

class StateNode:
  '''
  Class to represent a node of the search tree.
  '''

  def __init__(self, state, g=0, h=0):
    '''
    Constructor
    '''
    self.state = state
    self.g     = g
    self.h     = h
    self.f     = g+h

  def expand(self, theWorld, h='h0', expandAll=False):
    '''
    Expands this nodes children and returns them as a list
    '''
    heuristics = {
    'h0': self.hZero,
    'h1': self.dirtRemaining,
    'h2': self.manhattenDistance
    }
    children = []

    newState = self.state.vacuum()
    if newState != None:
      newNode = StateNode( newState, self.g+1, heuristics[h](newState) )
      children.append(newNode)
      if expandAll == False:
        return children

    newState = self.state.moveNorth(theWorld)
    if newState != None:
      newNode = StateNode( newState, self.g+1, heuristics[h](newState) )
      children.append(newNode)

    newState = self.state.moveSouth(theWorld)
    if newState != None:
      newNode = StateNode( newState, self.g+1, heuristics[h](newState) )
      children.append(newNode)

    newState = self.state.moveEast(theWorld)
    if newState != None:
      newNode = StateNode( newState, self.g+1, heuristics[h](newState) )
      children.append(newNode)

    newState = self.state.moveWest(theWorld)
    if newState != None:
      newNode = StateNode( newState, self.g+1, heuristics[h](newState) )
      children.append(newNode)

    return children

  def manhattenDistance(self, state ):
    '''
    Returns the manhatten distance needed to pick up
    the rest of the dirt.
    '''
    usedIndices = []
    manhattenDis = 0
    loc = state.curLoc
    #print(loc)
    #print(state.dirtList)
    for j in range(0,len(state.dirtList)):
      shortest = -1
      index    = 0
      i        = 0
      for dirt in state.dirtList:
        if index not in usedIndices:
          #print("loc[0] = " + str(loc[0]))
          #print("dirt[0] = " + str(dirt[0]))
          #print("loc[1] = " + str(loc[1]))
          #print("dirt[1] = " + str(dirt[1]))
          dis = abs(loc[0]-dirt[0]) + abs(loc[1]-dirt[1])
          if shortest == -1 or dis < shortest:
            shortest = dis
            i = index
        index = index + 1
      '''  
      blocks = 0
      for x in range(0,shortest[0]):
        if world.blocked((loc[0]+x,loc[1])):
          blocks = blocks + 1
      for x in range(0,shortest[1]):
        if world.blocked((loc[0]+shortest[0], loc[1]+x)):
          blocks = blocks + 1
      '''  
      usedIndices.append(i)
      manhattenDis = manhattenDis + shortest 
      loc = state.dirtList[i]
      #print("Next closest dirt: " + str(loc))
      #print("At index: " + str(i))
      #print("Distance away: " + str(dis))
      #print("Total distance so far: " + str(manhattenDis) )

    return manhattenDis + self.dirtRemaining(state)

  def dirtRemaining(self, state):
    '''
    Returns amount of dirt remaining.
    For use as a simple heuristic
    '''
    return len(state.dirtList)

  def hZero(self, state):
    '''
    Returns zero, for use as most simple
    heuristic.
    '''
    return 0

  def isClean(self):
    '''
    isClean call passed on to the state
    '''
    return self.state.isClean()

  def uniqueString(self, world):
    '''
    uniqueString call pass onto state
    '''
    return self.state.uniqueString(world)
