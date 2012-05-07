/*
 * ScenarioConverter.h
 *
 * Header file for ScenarioConverter.cpp
 *
 * Author: Jeffrey Picard
 */

#ifndef SCENARIO_CONVERTER_H
#define SCENARIO_CONVERTER_H
#include "ScenarioLoader.h"

#define EXIT_WITH_ERROR(...) {    \
  fprintf( stderr, __VA_ARGS__ ); \
  exit(1);                        \
}                                 

class ScenarioConverter
{
  public:
    ScenarioConverter( ScenarioLoader * );
    ~ScenarioConverter( void );
    void PrintMap( void );
    void ConvertMap( void );
    void PrintNthExperiment( int );
    void PrintAllExperiments( void );
  private:
    int rows, columns;
    char** map;
    ScenarioLoader *scen;
};

#endif
