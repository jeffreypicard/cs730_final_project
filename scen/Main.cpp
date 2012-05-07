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
  if( argc != 2 )
    EXIT_WITH_ERROR("Usage: a.out <scen_file_name>\n");

  ScenarioLoader *scen = new ScenarioLoader( argv[1] );

  ScenarioConverter *sc = new ScenarioConverter( scen );

  //Experiment exp = scen->GetNthExperiment( 0 );

  //printf("exp: %s", exp.GetMapName() );

  //sc->PrintMap();

  sc->ConvertMap();

  //sc->PrintMap();

  sc->PrintAllExperiments();

  delete sc;

  return 0;
}
