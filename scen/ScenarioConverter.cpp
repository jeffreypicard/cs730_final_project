/*
 * ScenarioConverter.cpp
 *
 * Class to read in a map from the file,
 * load the scenario, convert it to a format
 * my python program accepts and then write it
 * to stdout.
 *
 * Author: Jeffrey Picard
 */

#include <fstream>
#include <iostream>
#include <string>
#include <stdlib.h>

#include "ScenarioLoader.h"
#include "ScenarioConverter.h"

using namespace std;

ScenarioConverter::ScenarioConverter( ScenarioLoader *scen )
{
  this->scen = scen;
  ifstream in;
  char scrap[256], type[256];
  int rows, columns, i, j;

  Experiment exp = scen->GetNthExperiment( 0 );
  
  /*cout << "map " << exp.GetMapName() << "\n";*/

  in.open( exp.GetMapName(), ifstream::in );
  in >> scrap; 
  in >> type;
  in >> scrap;
  in >> rows;
  in >> scrap;
  in >> columns;
  in >> scrap;

  /*cout << "type " << type << "\n";
  cout << "rows " << rows << "\n";
  cout << "columns " << columns << "\n";*/

  this->rows = rows;
  this->columns = columns;
  this->map = (char**)malloc( sizeof(char*) * rows );

  for( i = 0; i < rows; i++ )
    this->map[i] = (char*)malloc( sizeof(char) * columns );

  in.get(); /*newline*/
  for( i = 0; i < rows; i++ )
  {
    for( j = 0; j < columns; j++ )
      this->map[i][j] = in.get();
    in.get(); /*newline*/
  }
}

ScenarioConverter::~ScenarioConverter( void )
{
  int i;
  delete this->scen;
  for( i = 0; i < this->rows; i++ )
    free( this->map[i] );
  free( this->map );
}

void ScenarioConverter::PrintAllExperiments( void )
{
  int num_experiments, i;
  num_experiments = this->scen->GetNumExperiments();
  cout << "experiments " << num_experiments / 50 << '\n';
  for( i = 0; i < num_experiments; i += 50 )
  {
    cerr << "i: " << i << '\n';
    this->PrintNthExperiment( i );
  }
}

void ScenarioConverter::PrintNthExperiment( int n )
{
  char old_start, old_goal;
  int start_x, start_y, goal_x, goal_y;
  Experiment exp = this->scen->GetNthExperiment( n );
  start_x = exp.GetStartX();
  start_y = exp.GetStartY();
  goal_x = exp.GetGoalX();
  goal_y = exp.GetGoalY();
  old_start = this->map[start_y][start_x];
  old_goal = this->map[goal_y][goal_x];
  this->map[start_y][start_x] = '@';
  this->map[goal_y][goal_x] = '*';

  this->PrintMap();

  this->map[start_y][start_x] = old_start;
  this->map[goal_y][goal_x] = old_goal;
}

void ScenarioConverter::PrintMap( void )
{
  int i, j;
  cout << this->columns << '\n';
  cout << this->rows << '\n';
  for( i = 0; i < this->rows; i++ )
  {
    for( j = 0; j < this->columns; j++ )
      cout << this->map[i][j];
    cout << '\n';
  }
}

void ScenarioConverter::ConvertMap( void )
{
  int i, j;
  for( i = 0; i < this->rows; i++ )
  {
    for( j = 0; j < this->columns; j++ )
      switch( this->map[i][j] )
      {
        case '.':
          this->map[i][j] = '_';
          break;
        case 'T':
        case '@':
        case 'O':
          this->map[i][j] = '#';
          break;
        default:
          EXIT_WITH_ERROR("Error: Bad map format.\n");
          break;
      }
  }
}
