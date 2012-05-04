'''
AStar.py

Code for an A* implementation in python.

Author: Jeffrey Picard
'''

import heapq
from State import State
from StateNode import StateNode

import GlobalVars 

class AStar:
  '''
  Class for A* search algorithm.
  '''

  def __init__(self):
    '''
    Constructor
    '''

  def search(self, curState, world, heuristic ):
    '''
    Does A* search
    '''
    global nodesExpanded
    global nodesGenerated
    closedList = {}
    Q = []
    startNode = StateNode( curState, 0, 0 )
    closedList[startNode.uniqueString(world)] = 1
    #Q.appendleft( startNode )
    heapq.heappush(Q,(startNode.f,startNode))
    while True:
      if len(Q) == 0:
        return None
      node = heapq.heappop(Q)[1]
      #print("popping node")
      #print( node.f )
      #print( node.state.toString() )

      if node.isClean():
        return node.state
      GlobalVars.nodesExpanded = GlobalVars.nodesExpanded + 1
      for child in node.expand(world, heuristic):
        #print( child.f )
        #print( child.uniqueString(world) )
        #print( child.state.toString() )
        s = child.uniqueString(world)
        GlobalVars.nodesGenerated = GlobalVars.nodesGenerated + 1
        if s not in closedList or child.f+1 < closedList[s]:
          #print("pushing node")
          #print( child.f )child.f+1
          #print( child.state.toString() )
          closedList[s] = child.f+1
          heapq.heappush(Q,(child.f,child))
