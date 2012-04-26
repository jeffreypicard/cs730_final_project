'''
Assignment1.py

Assignment 1 for CS730... Let's try it in python this time.

Author: Jeffrey Picard
'''

import sys
import cProfile

from World import World
from State import State
from DepthFirst import DepthFirst
from StateNode import StateNode
from UniformCost import UniformCost
from AStar import AStar

import GlobalVars

class Main:
  '''
  Main class for running the program.
  '''

  def __init__(self):
    '''
    Constructor
    '''
    self.algorithms = {
    'a-star'         : 1,
    'depth-first'    : 1,
    'depth-first-id' : 1,
    'uniform-cost'   : 1
    }

    self.algorithm  = ''

    self.heuristics = {
    'h0' : 1,
    'h1' : 1,
    'h2' : 1
    }

    self.heuristic  = ''
    

  def parseWorld(self):
    '''
    Parses the world representation from standerd in.
    '''
    columns = int(sys.stdin.readline())
    rows    = int(sys.stdin.readline())
    worldData = []
    for i in range(0,rows):
      worldData.append([])
      string = sys.stdin.readline()
      for j in range(0,columns):
        worldData[i].append(string[j])
    world = World( worldData, columns, rows )
    return world

  def parseCommandLine(self):
    '''
    Parses the command line options for the program.
    '''
    if len(sys.argv) == 1:
      print("Error: Not enough arguments")
      exit(1)
    if sys.argv[1] in self.algorithms:
      self.algorithm = sys.argv[1]
    else:
      print("Error: Unkown algorithm")
      exit(1)
    if self.algorithm == 'a-star':
      if len(sys.argv) > 2:
        if sys.argv[2] in self.heuristics:
          self.heuristic = sys.argv[2]
        else:
          print("Error: Unknown heuristic")
          exit(1)
      else:
        print("Error: No heuristic specified")
        exit(1)


if __name__ == "__main__":
  main = Main()
  main.parseCommandLine()
  world = main.parseWorld()
  startState = State( world.start, world.dirt )

  endState = None
  if main.algorithm == 'depth-first':
    algo = DepthFirst()
    #endState = algo.search( startState, world )
    #Does regular depth first, just calls the recursive version
    #of regular depth first search with no depth limit
    endState = algo.iterativeSearch( startState, world, -1)
  elif main.algorithm == 'depth-first-id':
    algo = DepthFirst()
    endState = algo.iterativeSearch( startState, world, 1 )
  elif main.algorithm == 'uniform-cost':
    algo = UniformCost()
    endState = algo.search( startState, world )
  elif main.algorithm == 'a-star':
    algo = AStar()
    endState = algo.search( startState, world, main.heuristic )
    #cProfile.run('algo.search( startState, world, main.heuristic )', 'a_star_prof')

  if endState != None:
    print( endState.toString() )
    print(str(GlobalVars.nodesGenerated) + " nodes generated\n" +
          str(GlobalVars.nodesExpanded)  + " nodes expanded")
