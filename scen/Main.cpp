/*
 * Main.cpp
 *
 * Main program for the scenerio loader.
 *
 * Author: Jeffrey Picard
 */

#include "ScenarioLoader.h"
#include "ScenarioConverter.h"

#include <stdio.h>
#include <stdlib.h>

using namespace std;

int main( int argc, char** argv )
{
  int exp = -1;
  if( argc != 2 && argc != 3 )
    EXIT_WITH_ERROR("Usage: a.out <scen_file_name> [experiment_num]\n");
  if( argc == 3 )
    exp = atoi( argv[2] );

  ScenarioLoader *scen = new ScenarioLoader( argv[1] );

  ScenarioConverter *sc = new ScenarioConverter( scen );

  //Experiment exp = scen->GetNthExperiment( 0 );

  //printf("exp: %s", exp.GetMapName() );

  //sc->PrintMap();

  sc->ConvertMap();

  //sc->PrintMap();
  if( exp >= 0 )
    sc->PrintNthExperiment( exp );
  else
    sc->PrintAllExperiments();

  delete sc;

  return 0;
}
