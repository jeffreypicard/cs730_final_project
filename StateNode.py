'''
StateNode.py

Author Jeffrey Picard
'''

from State import State
import math

class StateNode:
  '''
  Class to represent a node of the search tree.
  '''

  def __init__(self, state, g=0, h=0, parentDis=0):
    '''
    Constructor
    '''
    self.state      = state
    self.g          = g
    self.h          = h
    self.f          = g+h
    self.parentDis  = parentDis

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

    depthIncrease = 1

    newState = self.state.vacuum()
    if newState != None:
      newNode = StateNode( newState, self.g+depthIncrease, heuristics[h](newState), self.parentDis )
      children.append(newNode)
      if expandAll == False:
        #print("Vacuuming!")
        return children

    ############# Testing phase for JPS ###############

    if theWorld.jps:
      successors = theWorld.identifySuccessors( self.state, theWorld.start, self.state.dirtList, self.parentDis )
      #print("State")
      #print( self.state.printString( theWorld ) )
      if successors != []:
        #print("Successors")
        for s in successors:
          newState = State( (s[0],s[1]), self.state.dirtList, s[2] )
          #print(newState.printString(theWorld))
          newNode = StateNode( newState, self.g+s[3], heuristics[h](newState), s[3] )
          children.append( newNode )
        return children
      #print("No successors!")
      return children
    '''

    print( self.state.printString( theWorld ) ) 
    print("Successors:")
    for s in successors:
      print( "\t" + str(s) )
    print("\n")
    '''
    ############# End testing phase for JPS ##############

    ############# north #############

    if (self.state.curLoc,'n') in theWorld.edges:
      jump = theWorld.edges[ (self.state.curLoc, 'n') ]
    else:
      jump = None

    if jump:
      newState = self.state.moveNorth(theWorld,jump)
      depthIncrease = jump[1]
    else:
      newState = self.state.moveNorth(theWorld)
    if newState != None:
      newNode = StateNode( newState, self.g+depthIncrease, heuristics[h](newState) )
      children.append(newNode)

    ########### north west ##########

    if theWorld.EightWayMove:
      if (self.state.curLoc,'nw') in theWorld.edges:
        jump = theWorld.edges[ (self.state.curLoc, 'nw') ]
      else:
        jump = None
      if jump:
        newState = self.state.moveNorthWest(theWorld,jump)
        depthIncrease = jump[1]
      else:
        newState = self.state.moveNorthWest(theWorld)
      if newState != None:
        newNode = StateNode( newState, self.g+(depthIncrease*math.sqrt(2)), heuristics[h](newState) )
        children.append(newNode)

    ########### north east ##########

    if theWorld.EightWayMove:
      if (self.state.curLoc,'ne') in theWorld.edges:
        jump = theWorld.edges[ (self.state.curLoc, 'ne') ]
      else:
        jump = None
      if jump:
        newState = self.state.moveNorthEast(theWorld,jump)
        depthIncrease = jump[1]
      else:
        newState = self.state.moveNorthEast(theWorld)
      if newState != None:
        newNode = StateNode( newState, self.g+(depthIncrease*math.sqrt(2)), heuristics[h](newState) )
        children.append(newNode)


    ############# south #############

    if (self.state.curLoc, 's') in theWorld.edges:
      jump = theWorld.edges[ (self.state.curLoc,'s') ]
    else:
      jump = None

    depthIncrease = 1
    if jump:
      newState = self.state.moveSouth(theWorld,jump)
      depthIncrease = jump[1]
    else:
      newState = self.state.moveSouth(theWorld)
    if newState != None:
      newNode = StateNode( newState, self.g+depthIncrease, heuristics[h](newState) )
      children.append(newNode)

    ########### south west ##########

    if theWorld.EightWayMove:
      if (self.state.curLoc,'sw') in theWorld.edges:
        jump = theWorld.edges[ (self.state.curLoc, 'sw') ]
      else:
        jump = None
      if jump:
        newState = self.state.moveSouthWest(theWorld,jump)
        depthIncrease = jump[1]
      else:
        newState = self.state.moveSouthWest(theWorld)
      if newState != None:
        newNode = StateNode( newState, self.g+(depthIncrease*math.sqrt(2)), heuristics[h](newState) )
        children.append(newNode)

    ########### south east ##########

    if theWorld.EightWayMove:
      if (self.state.curLoc,'se') in theWorld.edges:
        jump = theWorld.edges[ (self.state.curLoc, 'se') ]
      else:
        jump = None
      if jump:
        newState = self.state.moveSouthEast(theWorld,jump)
        depthIncrease = jump[1]
      else:
        newState = self.state.moveSouthEast(theWorld)
      if newState != None:
        newNode = StateNode( newState, self.g+(depthIncrease*math.sqrt(2)), heuristics[h](newState) )
        children.append(newNode)


    ############# east #############

    if (self.state.curLoc, 'e') in theWorld.edges:
      jump = theWorld.edges[ (self.state.curLoc,'e') ]
    else:
      jump = None

    depthIncrease = 1
    if jump:
      newState = self.state.moveEast(theWorld,jump)
      depthIncrease = jump[1]
    else:
      newState = self.state.moveEast(theWorld)
    if newState != None:
      newNode = StateNode( newState, self.g+depthIncrease, heuristics[h](newState) )
      children.append(newNode)

    ############# west #############

    if (self.state.curLoc, 'w') in theWorld.edges:
      jump = theWorld.edges[ (self.state.curLoc,'w') ]
    else:
      jump = None

    depthIncrease = 1
    if jump:
      newState = self.state.moveWest(theWorld,jump)
      depthIncrease = jump[1]
    else:
      newState = self.state.moveWest(theWorld)
    if newState != None:
      newNode = StateNode( newState, self.g+depthIncrease, heuristics[h](newState) )
      children.append(newNode)

    #print("children")
    #for c in children:
    #  print( c.state.printString(theWorld) )

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
