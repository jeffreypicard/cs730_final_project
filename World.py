'''
World.py

Author: Jeffrey Picard
'''

from State import State
from Room import Room
import heapq

class World:
  '''
  Class to represent the static world.
  This is shared between all the states.
  '''

  def __init__(self, data, columns, rows):
    '''
    Constructor
    '''
    self.data     = data
    self.columns  = columns
    self.rows     = rows
    self.RSRData  = [ [ data[i][j] for j in range(0,columns) ] 
                      for i in range(0,rows) ]
    self.dirt     = self.dirtList()
    self.start    = self.startPoint()
    self.uList    = self.makeUList()
  
  def blocked(self, loc):
    '''
    Returns true or false about whether the position
    is blocked.
    '''
    return self.data[loc[0]][loc[1]] == '#'

  def getUList(self):
    '''
    '''
    return self.uList

  def makeUList(self):
    '''
    '''
    l = []
    for i in range(0,self.rows):
      for j in range(0,self.columns):
        if self.data[i][j] == '*':
          l.append('_')
        else:
          l.append(self.data[i][j])
    return l


  def toString(self,newLine=True):
    '''
    Returns a string representation of the world
    '''
    string = ""
    for i in range(0,self.rows):
      for j in range(0,self.columns):
        string = string + self.data[i][j]
      if newLine:
        string = string + '\n'
    return string

  def RSRDataToString(self,newLine=True):
    '''
    Returns a string representation of the world
    '''
    string = ""
    for i in range(0,self.rows):
      for j in range(0,self.columns):
        string = string + self.RSRData[i][j]
      if newLine:
        string = string + '\n'
    return string


  def dirtList(self):
    '''
    Returns a list of tuples of the locations of
    all the dirt in the world in the form (x,y,0).
    The zero is used in the State class to indicate
    that dirt has not yet been cleaned up.
    '''
    l = []
    for i in range(0,self.rows):
      for j in range(0,self.columns):
        if self.data[i][j] == '*':
          l.append((i,j))
    return l

  def startPoint(self):
    '''
    Return the starting point as a tuple in the form
    (x,y)
    '''
    for i in range(0,self.rows):
      for j in range(0,self.columns):
        if self.data[i][j] == '@':
          return (i,j)
  
  def getState(self):
    '''
    Returns an initial state for the world
    '''
    state = State(self.dirtList,self.start)

  def RSRDecomposition( self ):
    '''
    Calculates the decomposition needed for
    Rectangular Symmetry Reduction (RSR)
    '''
    Q = []
    rooms = []
    for i in range(0,self.rows):
      for j in range(0,self.columns):
        if self.data[i][j] != '#':
          room = Room((i,j))
          self.calcPriority( room )
          heapq.heappush(Q,(-room.size,room))
    while Q != []:
      a = heapq.heappop(Q)
      self.calcPriority( a[1] )
      if a[0] == -a[1].size:
        if a[1].br[0] - a[1].ul[0] > 2 and a[1].br[1] - a[1].ul[1] > 2:
          self.roomFill( a[1] )
          rooms.append( a[1] )
        #print( a[0] )
        #print( self.RSRDataToString() )
      else:
        heapq.heappush(Q,(-a[1].size,a[1]))
    for room in rooms:
      print( "size: " + str(room.size) )
      print( "\tul: " + str(room.ul) )
      print ( "\tbr: " + str(room.br) )
    print( self.RSRDataToString() )

  def calcPriority( self, room ):
    '''
    Calculates the priority of the given tile
    for RSR.
    '''
    i_b = room.ul[0]
    j_b = room.ul[1]
    room.br = (0,0)
    priority = 0
    i = i_b
    j = j_b
    depthLimit = self.columns
    blocked = False
    while True:
      j = j_b
      if i == self.rows or self.RSRData[i][j] == '#' or self.RSRData[i][j] == '+':
        x = (i-i_b)
        y = (j-j_b+1)
        z = x*y
        if x > 2 and y > 2 and z > priority:
          room.ur = (j_b,i)
          room.br = (i,j+1)
          room.bl = (i_b,j+1)
          priority = z
        break
      while True:
        if j == self.columns or j == depthLimit or self.data[i][j] == '#' or self.RSRData[i][j] == '+':
          x = (i-i_b+1)
          y = (j-j_b)
          z = x*y
          if x > 2 and y > 2 and z > priority:
            room.ur = (j_b,i+1)
            room.br = (i+1,j)
            room.bl = (i_b,j)
            priority = z
          depthLimit = j
          break
        j = j + 1
      i = i + 1

    '''
    i = i_b
    j = j_b
    blocked = False
    while True:
      if self.data[i][j] == '#' or j == self.columns-1:
        if (i-i_b+1)*(j-j_b+1) > priority:
          priority = (i-i_b+1)*(j-j_b+1)
        break
      i = i_b
      while True:
        if self.data[i][j] == '#' or i == self.rows-1:
          if (i-i_b+1)*(j-j_b+1) > priority:
            priority = (i-i_b+1)*(j-j_b+1)
          blocked = True
          break
        i = i + 1
      if blocked:
        break
      j = j + 1
    '''
    '''
    blocked = False
    while j < self.columns:
      for k in range(i_b,self.rows):
        if self.data[k][j] == '#':
          blocked = True
          break
      if blocked:
        break
      j = j+1
    priority = (i-i_b)*(j-j_b)

    i = i_b
    j = j_b
    while j < self.columns:
      if self.data[i][j] == '#':
        break
      j = j + 1
    blocked = False
    while i < self.rows:
      for k in range(j_b,self.columns):
        if self.data[i][k] == '#':
          blocked = True
          break
      if blocked:
        break
      i = i+1
    if (i-i_b)*(j-j_b) > priority:
      priority = (i-i_b)*(j-j_b)
    '''
    #if priority == 27:
    #  print( "i="+str(i_b)+",j="+str(j_b) )
    room.size = priority

  def roomFill( self, room ):
    '''
    Takes a room and fills in the RSRData matrix
    so that those spots are not used for subsequent
    rooms.
    '''
    i_b = room.ul[0]
    j_b = room.ul[1]
    i_e = room.br[0]
    j_e = room.br[1]
    if i_e-i_b == 1 or j_e-j_b == 1:
      return
    for i in range(i_b,i_e):
      for j in range(j_b,j_e):
        self.RSRData[i][j] = '+'
