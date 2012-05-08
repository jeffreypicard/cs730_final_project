/*
 * calc_stats.c
 *
 * Reads in data files from my A* python program's output
 * and calculates the relevant statics, writing them to a file.
 *
 * Author: Jeffrey Picard
 */
/* Standard headers */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

/* Constants */
#define DEBUG     0
#define INIT_SIZE 1000
#define USAGE "Usage: calc_stats <list_of_files>\n"
#define RESIZE_MAGNITUDE 2
/* count time nodes_gen nodes_exp */
#define DATA_COLUMNS 4
#define SCANF_STRING "%f %f %f %f\n"
#define COMMENT '#'

/* Macros */
#define EXIT_WITH_ERROR(...) {    \
  fprintf( stderr, __VA_ARGS__ ); \
  exit(1);                        \
}

#define EXIT_WITH_PERROR(...) {   \
  fprintf( stderr, __VA_ARGS__ ); \
  perror( NULL );                 \
  exit(1);                        \
}

/* Structs */
struct _stats {
  double **data;
  int size;
} typedef stats;

/* Function prototypes */
void read_data_file( char *, stats * );
void resize_data( stats * );
void init_stats( stats ** );
void destroy_stats( stats * );
void add_data( stats *, int, double, double, double );
void output_stats( FILE *, stats * );
void output_speedup( FILE *, stats *, stats * );

int main( int argc, char **argv )
{
  FILE *fp1, *fp2;
  stats *vanilla = NULL;
  stats *jps = NULL;
  stats *vanilla_four = NULL;
  stats *rsr = NULL;
  int i;
  if( argc == 1 ) 
    EXIT_WITH_ERROR(USAGE)

  fp1 = fopen("jps_speedup.dat", "w");
  fp2 = fopen("rsr_speedup.dat", "w");
  if( !fp1 || !fp2 )
    EXIT_WITH_PERROR("fopen failed in main: ")

  init_stats( &vanilla );
  init_stats( &jps );
  init_stats( &vanilla_four );
  init_stats( &rsr );

  assert( (argc-1) % 4 == 0 );

  for( i = 1; i < argc; i += 4 )
  {
    read_data_file( argv[i], vanilla );
    read_data_file( argv[i+1], jps );
    read_data_file( argv[i+2], vanilla_four );
    read_data_file( argv[i+3], rsr );
  }
  //output_stats( stdout, vanilla );
  //output_stats( stdout, jps );
  output_speedup( fp1, jps, vanilla );
  //output_stats( stdout, vanilla_four );
  //output_stats( stdout, rsr );
  output_speedup( fp2, rsr, vanilla_four );

  fclose( fp1 );
  fclose( fp2 );

  return 0;
}

int fpeek( FILE *fp )
{
  int c = fgetc( fp );
  ungetc( c, fp );
  return c;
}

/*
 * read_data_file
 *
 * Takes a data file and data matrix and
 * reads the files contents to the matrix.
 */
void read_data_file( char *file_name, stats *s )
{
  int index = 0, junk = 0;
  double path_length = 0, time = 0, nodes_gen = 0, nodes_exp = 0;
  FILE *fp_in = NULL;
  fp_in = fopen( file_name, "r" );
  if( !fp_in )
    EXIT_WITH_PERROR("Could not read file '%s': ", file_name )

  while( 1 )
  {
    /*
    if( fpeek( fp_in ) == COMMENT )
    {
      while( fgetc( fp_in ) != '\n' );
      continue;
    }*/

    junk = fscanf( fp_in, "%lf %lf %lf %lf", &path_length, &time, &nodes_gen, &nodes_exp );
#if DEBUG
    fprintf( stderr, "path_length: %lf\n"
                     "time:        %lf\n"
                     "nodes_gen:   %lf\n"
                     "nodes_exp:   %lf\n",
                     path_length, time, nodes_gen, nodes_exp );
#endif
    //fgetc( fp_in ); /* newline */
    if( junk == EOF )
      break;
    else if( junk != 4 )
    {
      EXIT_WITH_ERROR("Formatting error in read_data_file junk is %d\n", junk )
    }
    index = (int)path_length;
    add_data( s, index, time, nodes_gen, nodes_exp );
  }
  junk = fclose( fp_in );
  if( junk == EOF )
    EXIT_WITH_PERROR("Could not close file '%s': ", file_name )
}

/*
 * add_data
 *
 * Adds data to the stats structure.
 */
void add_data( stats *s, int path_length, double time, double nodes_gen,
               double nodes_exp )
{
  while( path_length > s->size )
    resize_data( s );
  if( !s->data[ path_length ] )
  {
    s->data[ path_length ] = calloc( sizeof(double), DATA_COLUMNS );
    if( !s->data[ path_length ] )
      EXIT_WITH_PERROR("malloc failed in add_data: ")
  }
  s->data[ path_length ][0]++;
  s->data[ path_length ][1] += time;
  s->data[ path_length ][2] += nodes_gen;
  s->data[ path_length ][3] += nodes_exp;
}

/*
 * init_stats
 *
 * Takes a pointer to a stats pointer and initializes it.
 */
void init_stats( stats **s )
{
  *s = malloc( sizeof(stats) );
  if( !*s )
    EXIT_WITH_PERROR("malloc failed in init_stats: ")
  (*s)->data = calloc( sizeof(double*), INIT_SIZE );
  if( !(*s)->data )
    EXIT_WITH_PERROR("malloc failed in init_stats: ")
  (*s)->size = INIT_SIZE;
}

/*
 * destroy_stats
 *
 * Takes a stats struct pointer and free all it's data.
 */
void destroy_stats( stats *s )
{
  int i;
  for( i = 0; i < s->size; i++ )
    free( s->data[i] );
  free( s->data );
  free( s );
}

/*
 * resize_data
 *
 * Takes a stats struct and resizes the data matrix
 * so it can fit more data.
 */
void resize_data( stats *s )
{
  int i, j;
  int new_size = s->size * RESIZE_MAGNITUDE;
  double **new_data = calloc( sizeof(double*), new_size );
  if( !new_data )
    EXIT_WITH_PERROR("malloc failed in resize_data: ")

  for( i = 0; i < s->size; i++ )
  {
    new_data[i] = calloc( sizeof(double), DATA_COLUMNS );
    if( !new_data[i] )
      EXIT_WITH_PERROR("malloc failed in resize_data: ")
    for( j = 0; j < DATA_COLUMNS; j++ )
      new_data[i][j] = s->data[i][j];
  }
  free( s->data );
  s->data = new_data;
  s->size = new_size;
}

void output_speedup( FILE *fp, stats *faster, stats *slower )
{
  int i;
  fprintf(fp,"# path_length speedup_time speedup_nodes_gen\n");
  int size = slower->size < faster->size ? slower->size : faster->size;
  for( i = 0; i < size; i++ )
  {
    if( faster->data[i] && slower->data[i] )
    {
      double speedup_time = (slower->data[i][1] / slower->data[i][0]) / (faster->data[i][1] / faster->data[i][0]);
      double speedup_nodes_gen = (slower->data[i][2] / slower->data[i][0]) / (faster->data[i][2] / faster->data[i][0]);
      fprintf( fp, "%d %lf %lf\n", i, speedup_time, speedup_nodes_gen );
    }
  }

}

void output_stats( FILE *fp, stats *s )
{
  int i;
  fprintf(fp,"# path_length average_time average_nodes_gen average_nodes_exp\n");
  for( i = 0; i < s->size; i++ )
  {
    if( s->data[i] )
      fprintf( fp, "%d %lf %lf %lf\n", i,
                                      s->data[i][1] / s->data[i][0],
                                      s->data[i][2] / s->data[i][0],
                                      s->data[i][3] / s->data[i][0] );
  }
}

/*
 * summon_siege_of_herons
 *
 * To be implemented later.
 */
void summon_siege_of_herons( void )
{
}
