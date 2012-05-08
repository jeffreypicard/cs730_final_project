'''
Main2.py

Main for final project for CS730.

Author: Jeffrey Picard
'''

import sys
import time
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

    self.speedups = {
    'rsr': 1,
    'jps': 1
    }

    self.speedup = ''

    self.experiments = 1

    self.EightWayMove = True

    self.columns = None # Hack
    
  def parseExperiments( self ):
    '''
    Checks to see if the number of experiments was specified.
    '''
    first = sys.stdin.readline()
    if first.startswith("experiments"):
      self.experiments = int(first[11:])
    else:
      #sys.stdin.seek(0,0)
      self.columns = int(first)

  def parseWorld(self):
    '''
    Parses the world representation from standard in.
    '''
    # Hack
    if not self.columns:
      columns = int(sys.stdin.readline())
    else:
      columns = self.columns
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
        if len(sys.argv) > 3:
          if sys.argv[3] in self.speedups:
            self.speedup = sys.argv[3]
          elif sys.argv[3] == '4':
            self.EightWayMove = False
          else:
            print("Error: Unknown speed-up algorithm")
            exit(1)
      else:
        print("Error: No heuristic specified")
        exit(1)


if __name__ == "__main__":
  main = Main()
  main.parseCommandLine()
  main.parseExperiments()
  #main.experiments = main.experiments / 5
  timingStart = [ 0.0 for x in range(0,main.experiments) ]
  timingEnd = [ 0.0 for x in range(0,main.experiments) ]
  nodeGenList = [ 0 for x in range(0,main.experiments) ]
  nodeExpList = [ 0 for x in range(0,main.experiments) ]
  for i in range(0,main.experiments):
    timingStart[i] = time.time()
    world = main.parseWorld()
    if not world.validWorld():
      continue
    #print( world.toString() )
    world.EightWayMove = main.EightWayMove
    if main.speedup == 'rsr':
      world.RSRDecomposition()
      world.EightWayMove = False
    elif main.speedup == 'jps':
      world.jps = True
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
    
    timingEnd[i] = time.time()
    nodeGenList[i] = GlobalVars.nodesGenerated
    nodeExpList[i] = GlobalVars.nodesExpanded

    if endState != None:
      #print( endState.toString() )
      #print( str(endState.pathCost()) )
      #print(str(GlobalVars.nodesGenerated) + " nodes generated\n" +
      #      str(GlobalVars.nodesExpanded)  + " nodes expanded")
      print( str(endState.pathCost()) + " " + str(timingEnd[i]-timingStart[i]) + " " + 
             str(GlobalVars.nodesGenerated) + " " + str(GlobalVars.nodesExpanded) )
    else:
      print("No path found")
    GlobalVars.nodesGenerated = 0
    GlobalVars.nodesExpanded = 0
    
  '''
  timingTotal = [ x - y for x,y in zip(timingEnd,timingStart) ]
  totalTime = sum(timingTotal)
  avgTime = totalTime / main.experiments
  totalNodeGen = sum( nodeGenList )
  totalNodeExp = sum( nodeExpList )
  avgNodeGen = totalNodeGen / main.experiments
  avgNodeExp = totalNodeExp / main.experiments
  print("\n########## Performance Statistics ##########\n")
  print("#TotalTime AverageTime TotalNodesGenerated Average")
  print("Total Time: " + str(totalTime) )
  print("Average Time: " + str(avgTime) )
  print("\nTotal Nodes Generated: " + str(totalNodeGen) )
  print("Average Nodes Generated: " + str(avgNodeGen) )
  print("\nTotal Nodes Expanded: " + str(totalNodeExp) )
  print("Average Nodes Expanded: " + str(avgNodeExp) )
  '''
