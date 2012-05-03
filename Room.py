'''
Room.py

Repesentation of a room for RSR

Author: Jeffrey Picard
'''

class Room:

  def __init__( self, ul ):
    '''
    Class representation of a room for RSR.
    '''
    self.ul = ul    # Upper left point
    self.ur = None  # Upper right point
    self.bl = None  # Bottom left point
    self.br = None  # Bottom right point
    self.size = 0
  
  def fixEdges( self, edges, goalList ):
    '''
    Takes a list of goals (points) and checks to
    see if any of them are contained in this room
    '''
    for g in goalList:
      if self.contains( g ):
        #print("Goal in room")
        edges[((self.ul[0],g[1]),'s')] = (g,g[0]-self.ul[0])
        edges[(g,'n')] = ((self.ul[0],g[1]),g[0]-self.ul[0])
        edges[((g[0],self.ul[1]),'e')] = (g,g[1]-self.ul[1])
        edges[(g,'w')] = ((g[0],self.ul[1]),g[1]-self.ul[1])
        edges[((self.br[0]-1,g[1]),'w')] = (g,self.br[0]-1-g[0])
        edges[(g,'e')] = ((self.br[0]-1,g[1]),self.br[0]-1-g[0])
        edges[((g[0],self.br[1]-1),'w')] = (g,self.br[1]-1-g[1])
        edges[(g,'e')] = ((g[0],self.br[1]-1),self.br[1]-1-g[1])
      #print("")

  def contains( self, p ):
    '''
    Takes a points p and returns whether or not
    this room contains it.
    '''
    #print( "ul: " + str(self.ul) + "br: " + str(self.br) )
    #print( p )
    if self.ul[0] >= p[0] or self.ul[1] >= p[1] or self.br[0]-1 <= p[0] or self.br[1]-1 <= p[1]:
      return False
    return True
