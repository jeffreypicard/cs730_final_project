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
  
  def contains( self, point ):
    '''
    Takes a point and checks to see if this room
    contains it.
    '''
