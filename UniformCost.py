'''
UniformCost.py

Author: Jeffrey Picard
'''

import heapq
from State import State
from StateNode import StateNode

import GlobalVars

class UniformCost:
  '''
  Class for doing uniform cost search
  '''

  def __init__(self):
    '''
    Constructor
    '''

  def search(self, curState, world ):
    '''
    Does uniform cost search
    '''
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
      if node.isClean():
        return node.state
      GlobalVars.nodesExpanded = GlobalVars.nodesExpanded + 1
      for child in node.expand(world):
        GlobalVars.nodesGenerated = GlobalVars.nodesGenerated + 1
        if child.uniqueString(world) not in closedList:
          closedList[child.uniqueString(world)] = 1
          heapq.heappush(Q,(child.f,child))
          #Q.appendleft( child )


