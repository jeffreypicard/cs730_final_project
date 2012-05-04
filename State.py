'''
State.py

Code for a state for A* search.

Author: Jeffrey Picard
'''

from copy import deepcopy
import math

class State:
  '''
  Class to represent a world state
  '''

  def __init__(self, curLoc, dirtList, actions=[]):
    '''
    Constructor
    '''
    self.curLoc   = curLoc
    self.dirtList = dirtList
    self.actions  = actions
    #This is set after the first call to uniqueString
    #So it is never calculated more than once.
    self.string   = None

  def copy(self):
    '''
    Returns a copy of itself
    '''
    return State( self.curLoc, self.dirtList, self.actions )

  def printString(self, theWorld, newLine=True):
    '''
    Returns string formatted nicely.
    '''
    string = ''
    for i in range(0,theWorld.rows):
      for j in range(0,theWorld.columns):
        if theWorld.blocked( (i,j) ):
          string = string + '[#]'
        elif (i,j) in self.dirtList:
          if (i,j) == self.curLoc:
            string = string + '[$]'
          else:
            string = string + '[*]'
        elif (i,j) == self.curLoc:
          string = string + '[@]'
        else:
          string = string + '[_]'
      if newLine:
        string = string + '\n'
    return string
  
  def pathCost( self ):
    '''
    Returns the cost of the path to the state.
    '''
    cost = 0
    for x in self.actions:
      if len(x) == 1:
        cost = cost + 1
      elif len(x) == 2:
        cost = cost + math.sqrt(2)
    return cost

  def toString(self,newLine=True):
    '''
    Returns a string representation of the state
    (The moves required to get there)
    '''
    if self.actions == []:
      return ""
    if newLine:
      string = ''.join([x+'\n' for x in self.actions])
    else:
      string = ''.join([x for x in self.actions])
    return string

  def uniqueString(self, theWorld):
    '''
    Returns a unique string representing the state.
    For use in a dictionary (hash table)
    '''
    #if self.string != None:
     # return self.string
    #string = self.printString(theWorld,False)
    #print(string)
    #return string
    #
    # Python strings are incredibly slow.
    # Building a list up front, editing it as
    # needed and joining it before returning the
    # string is about 15 times faster acording
    # the the profiler I used. (cProfile)
    #
    l = ['_' for x in range(0,theWorld.rows*theWorld.columns)]
    for (i,j) in self.dirtList:
      l[(i)*theWorld.columns+j] = '*'
    if self.curLoc in self.dirtList:
      l[(self.curLoc[0])*theWorld.columns+self.curLoc[1]] = '$'
    else:
      l[(self.curLoc[0])*theWorld.columns+self.curLoc[1]] = '@'

    self.string = ''.join(l)
    #print(string)
    return self.string
    '''
    string = ''
    for i in range(0,theWorld.rows):
      for j in range(0,theWorld.columns):
        if (i,j) in self.dirtList:
          if (i,j) == self.curLoc:
            string = string + '$'
          else:
            string = string + '*'
        elif (i,j) == self.curLoc:
          string = string + '@'
        else:
          string = string + '_'
    
    print(string)
    return string
    '''
    #string = string + ''.join([str(x[0])+str(x[1]) for x in self.dirtList])
    #for tpl in self.dirtList:
      #string = string + str(tpl[0]) + str(tpl[1])
    #string = string + str(self.curLoc[0]) + str(self.curLoc[1])
    '''
    l = []
    for i in range(0,theWorld.rows):
      for j in range(0,theWorld.columns):
        if theWorld.blocked( (i,j) ):
          l.append('#')
        elif (i,j) in self.dirtList:
          if (i,j) == self.curLoc:
            l.append('$')
          else:
            l.append('*')
        elif (i,j) == self.curLoc:
          l.append('@')
        else:
          l.append('_')
     
    return ''.join(l)
    '''

  def isClean(self):
    '''
    Return true if the state is clean
    '''
    '''
    for tpl in dirtList:
      if tpl[2] == 0:
        return False
    return True
    '''
    if self.dirtList == []:
      return True
    return False

  def vacuum(self):
    '''
    Attemps to vacuum
    '''
    if self.curLoc in self.dirtList:
      #newState = self.copy()
      newState = deepcopy(self)
      newState.actions.append('V')
      newState.dirtList.remove((self.curLoc[0],self.curLoc[1]))
      return newState
    else:
      #print( str(self.curLoc) + "Not dirty" )
      return None
  
  def moveNorth(self, theWorld, jump=None):
    '''
    Attempts to move north
    '''
    M = 1
    if self.curLoc in self.dirtList:
      #print("NORTH?!?!?")
      #return None
      pass
    if jump:
      proposedLoc = jump[0]
      M = jump[1]
    else:
      if self.curLoc[0] == 0:
        return None
      proposedLoc = (self.curLoc[0]-1,self.curLoc[1])
      if theWorld.blocked(proposedLoc):
        return None
    newState = deepcopy(self)
    newState.curLoc = proposedLoc
    for i in range(0,M):
      newState.actions.append('N')
    return newState

  def moveNorthWest(self, theWorld, jump=None):
    '''
    Attempts to move north west
    '''
    M = 1
    if self.curLoc in self.dirtList:
      #print("NORTH?!?!?")
      #return None
      pass
    if jump:
      proposedLoc = jump[0]
      M = jump[1]
    else:
      if self.curLoc[0] == 0 or self.curLoc[1] == 0:
        return None
      proposedLoc = (self.curLoc[0]-1,self.curLoc[1]-1)
      if theWorld.blocked(proposedLoc):
        return None
    newState = deepcopy(self)
    newState.curLoc = proposedLoc
    for i in range(0,M):
      newState.actions.append('NW')
    return newState

  def moveNorthEast(self, theWorld, jump=None):
    '''
    Attempts to move north west
    '''
    M = 1
    if self.curLoc in self.dirtList:
      #print("NORTH?!?!?")
      #return None
      pass
    if jump:
      proposedLoc = jump[0]
      M = jump[1]
    else:
      if self.curLoc[0] == 0 or self.curLoc[1] == theWorld.columns-1:
        return None
      proposedLoc = (self.curLoc[0]-1,self.curLoc[1]+1)
      if theWorld.blocked(proposedLoc):
        return None
    newState = deepcopy(self)
    newState.curLoc = proposedLoc
    for i in range(0,M):
      newState.actions.append('NE')
    return newState

  def moveSouth(self, theWorld, jump=None):
    '''
    Attempts to move south
    '''
    M = 1
    if self.curLoc in self.dirtList:
      #print("SOUTH?!?!?")
      #return None
      pass
    if jump:
      proposedLoc = jump[0]
      M = jump[1]
    else:
      if self.curLoc[0] == theWorld.rows-1:
        return None
      proposedLoc = (self.curLoc[0]+1,self.curLoc[1])
      if theWorld.blocked(proposedLoc):
        return None
    newState = deepcopy(self)
    newState.curLoc = proposedLoc
    for i in range(0,M):
      newState.actions.append('S')
    return newState

  def moveSouthWest(self, theWorld, jump=None):
    '''
    Attempts to move south
    '''
    M = 1
    if self.curLoc in self.dirtList:
      #print("SOUTH?!?!?")
      #return None
      pass
    if jump:
      proposedLoc = jump[0]
      M = jump[1]
    else:
      if self.curLoc[0] == theWorld.rows-1 or self.curLoc[1] == 0:
        return None
      proposedLoc = (self.curLoc[0]+1,self.curLoc[1]-1)
      if theWorld.blocked(proposedLoc):
        return None
    newState = deepcopy(self)
    newState.curLoc = proposedLoc
    for i in range(0,M):
      newState.actions.append('SW')
    return newState

  def moveSouthEast(self, theWorld, jump=None):
    '''
    Attempts to move south
    '''
    M = 1
    if self.curLoc in self.dirtList:
      #print("SOUTH?!?!?")
      #return None
      pass
    if jump:
      proposedLoc = jump[0]
      M = jump[1]
    else:
      if self.curLoc[0] == theWorld.rows-1 or self.curLoc[1] == theWorld.columns-1:
        return None
      proposedLoc = (self.curLoc[0]+1,self.curLoc[1]+1)
      if theWorld.blocked(proposedLoc):
        return None
    newState = deepcopy(self)
    newState.curLoc = proposedLoc
    for i in range(0,M):
      newState.actions.append('SE')
    return newState

  def moveEast(self, theWorld, jump=None):
    '''
    Attempts to move east
    '''
    M = 1
    if self.curLoc in self.dirtList:
      #print("EAST?!?!?")
      #return None
      pass

    if jump:
      proposedLoc = jump[0]
      M = jump[1]
    else:
      if self.curLoc[1] == theWorld.columns-1:
        return None
      proposedLoc = (self.curLoc[0],self.curLoc[1]+1)
      if theWorld.blocked(proposedLoc):
        return None
    newState = deepcopy(self)
    newState.curLoc = proposedLoc
    for i in range(0,M):
      newState.actions.append('E')
    return newState

    return None

  def moveWest(self, theWorld, jump=None):
    '''
    Attempts to move west
    '''
    M = 1
    if self.curLoc in self.dirtList:
      #print("WEST?!?!?")
      #return None
      pass

    if jump:
      proposedLoc = jump[0]
      M = jump[1]
    else:
      if self.curLoc[1] == 0:
        return None
      proposedLoc = (self.curLoc[0],self.curLoc[1]-1)
      if theWorld.blocked(proposedLoc):
        return None
    newState = deepcopy(self)
    newState.curLoc = proposedLoc
    for i in range(0,M):
      newState.actions.append('W')
    return newState

    return None


