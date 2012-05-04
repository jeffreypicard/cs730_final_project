'''
DepthFirst.py

Code for a depth first search implementation in python.

Author: Jeffrey Picard
'''

from StateNode import StateNode
from State import State

import GlobalVars

class DepthFirst:
  '''
  Implements depth first searches.
  '''

  def __init__(self):
    '''
    Constructor
    '''

  def search(self, curState, world, maxDepth=-1):
    '''
    Iterative version of depth first search.
    This currently has some bugs and is not fit for use!
    It does not return an optimal solution when used with
    iterative deepening. The recrusive version works, though.
    '''
    closedList = {}
    queue = []
    startNode = StateNode( curState, 0, 0 )
    closedList[startNode.uniqueString(world)] = 1
    queue.append( startNode )
    depth = 0
    if maxDepth == -1:
      maxDepth = 1000000
    #return self.do_search(queue,closedList,world,depth,maxDepth)
    while True:
      if queue == []:
        return None
      node = queue.pop()
      #if node.uniqueString(world) in closedList:
        #print( node.state.printString(world) )
      if node.isClean():
        return node.state
      if depth < maxDepth:
        GlobalVars.nodesExpanded = GlobalVars.nodesExpanded + 1
        for child in node.expand( world ):
          GlobalVars.nodesGenerated = GlobalVars.nodesGenerated + 1
          if child.uniqueString(world) not in closedList:
            closedList[child.uniqueString(world)] = 1
            queue.append( child )
        depth = depth + 1
      else:
        depth = depth - 1
        #print(len(closedList))
        del closedList[node.uniqueString(world)]
        #print(len(closedList))

  def rec_search(self,queue,closedList,world,depth,maxDepth):
    '''
    Recursive version of depth first search.
    '''
    if queue == []:
      return None
    node = queue.pop()
    if node.isClean():
      return node.state
    if depth < maxDepth:
      GlobalVars.nodesExpanded = GlobalVars.nodesExpanded + 1
      for child in node.expand( world ):
        GlobalVars.nodesGenerated = GlobalVars.nodesGenerated + 1
        if child.uniqueString(world) not in closedList:
          closedList[child.uniqueString(world)] = 1
          queue.append( child )
          result = self.rec_search(queue,closedList,world,depth+1,maxDepth)
          if result != None:
            return result
    else:
      #print("Duplicate found!")
      del closedList[node.uniqueString(world)]
      return None

  def iterativeSearch(self,curState,world,maxDepth):
    '''
    Does an iterative depthfirst search by
    calling the normal one
    '''
    result = None
    if maxDepth == -1:
      maxDepth = 1000000
    while result == None:
      #print(maxDepth)
      Q = []
      closedList = {}
      root = StateNode( curState, 0, 0)
      Q.append(root)
      closedList[curState.uniqueString(world)] = 1
      result = self.rec_search(Q,closedList,world,0,maxDepth)
      maxDepth = maxDepth + 1

    return result
