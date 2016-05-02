/* islander.c
 * $Smake: cc -O -o %F %f msecond.o random_int.o -lpthread -lm
 * 
 * 02/19/2015 by CDR M. Bilzor, U.S. Naval Academy
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <semaphore.h>
#include <pthread.h>
#include <stdbool.h>
#include "random_int.h"

#define NUM_ISLANDERS		50
#define NUM_COCONUTS		50
#define NUM_MACHETES		3
#define NUM_FUNNELS		6
#define MEAN_DRINK_TIME		1000

/*==========================================================================*/

/* Macros to encapsulate POSIX semaphore functions, and global variables */
#define semaphore_create(s,v)	sem_init( &s, 0, v )
#define semaphore_wait(s)		sem_wait( &s )
#define semaphore_signal(s)		sem_post( &s )
#define semaphore_release(s)	sem_destroy( &s )

typedef sem_t semaphore;
//create the semaphore instances
semaphore machetes;
semaphore funnels;
semaphore coconuts;

bool has_coconut[NUM_ISLANDERS];
bool has_machete[NUM_ISLANDERS];
bool has_funnel[NUM_ISLANDERS];

// These represent the number of each resource currently available
int coconuts_available = NUM_COCONUTS;
int machetes_available = NUM_MACHETES;
int funnels_available = NUM_FUNNELS;


/*==========================================================================*/

void get_coconut(int n)
{
  //wait for an availiable coconut
  semaphore_wait(coconuts);
  while (coconuts_available < 1) {printf( "shouldn't get here");}
  coconuts_available--;
  has_coconut[n] = true;
}

void get_machete(int n)
{
  //wait for an availiable machete
semaphore_wait(machetes);
 while (machetes_available < 1) {printf( "shouldn't get here");}
	machetes_available--;
	has_machete[n] = true;
}

void get_funnel(int n)
{
  //wat for an availiable funnel
semaphore_wait(funnels);
while (funnels_available < 1) {printf( "shouldn't get here");}
	funnels_available--;
	has_funnel[n] = true;
}

void drop_coconut(int n)
{
  coconuts_available++;
	has_coconut[n] = false;

        //let the islanders know that your done with the coconut
         semaphore_signal(coconuts);
}

void drop_machete(int n)
{
  machetes_available++;
	has_machete[n] = false;

        //let the islanders know that your done with the machete
        semaphore_signal(machetes);
}

void drop_funnel(int n)
{
  funnels_available++;
	has_funnel[n] = false;
        //let the islanders know that your done with the machete
        semaphore_signal(funnels);
}

/*==========================================================================*/

void islander( int * islander_data )
/* Simulate an islander. Each islander must obtain a coconut, machete, and
funnel in order to make his pina colada for happy hour. This function islander
is called via pthread_create(). The argument is a pointer to an array of 
islander numbers. */
{
    int n = islander_data[0];
	int r = 0;

	/* Get Supplies */
	r = rand() % 3;
	switch(r) {
		case 0:	get_coconut(n); printf("islander %i got a coconut\n", n); fflush(stdout);
				get_machete(n); printf("islander %i got a machete\n", n); fflush(stdout);
				get_funnel(n);  printf("islander %i got a funnel\n", n); fflush(stdout);
				break;
		case 1:
				get_machete(n); printf("islander %i got a machete\n", n); fflush(stdout);
				get_funnel(n);  printf("islander %i got a funnel\n", n); fflush(stdout);
				get_coconut(n); printf("islander %i got a coconut\n", n); fflush(stdout);
				break;
		case 2:
				get_funnel(n);  printf("islander %i got a funnel\n", n); fflush(stdout);
				get_coconut(n); printf("islander %i got a coconut\n", n); fflush(stdout);
				get_machete(n); printf("islander %i got a machete\n", n); fflush(stdout);
	} 

	/* Enjoy Pina Colada */
	printf("islander %i enjoying a pina colada\n", n); fflush(stdout);
	usleep( 1000L * random_int(MEAN_DRINK_TIME) );	/* microseconds */

	/* Release Supplies */
	drop_funnel(n);
	printf("islander %i released a funnel\n", n); fflush(stdout);

	drop_machete(n);
	printf("islander %i released a machete\n", n); fflush(stdout);

	drop_coconut(n);
	printf("islander %i released a coconut\n", n); fflush(stdout);

    /* Done */
	printf("islander %i done\n", n); fflush(stdout); 
    pthread_exit(NULL);
}

/*==========================================================================*/

int main( int argc, char *argv[] )
{

    int i;
    pthread_t med[NUM_ISLANDERS];
    int islander_data[NUM_ISLANDERS];
    int s = 1;
	srand(time(NULL));

        //instanciate my semaphores
        semaphore_create(machetes, NUM_MACHETES);
        semaphore_create(funnels, NUM_FUNNELS);
        semaphore_create(coconuts, NUM_COCONUTS);

    /* Create a thread for each islander. */
    for ( i = 0; i < NUM_ISLANDERS; i++ )
    {
		islander_data[i] = i;
		has_coconut[i] = false;
		has_machete[i] = false;
		has_funnel[i] = false;
		if ( pthread_create( &med[i], NULL, (void *(*)(void *)) &islander, &islander_data[i] ) != 0 ) 
		{
		    fprintf( stderr, "Cannot create thread for islander %d\n", i );
		    exit( 1 );
		}
    }

    /* Wait for all islanders to finish. */
    for ( i = 0; i < NUM_ISLANDERS; i++ )
    {
		pthread_join( med[i], NULL );
    }

    //release my semaphores
    semaphore_release(machetes);
    semaphore_release(funnels);
    /* Produce the final report. */
    printf( "All islanders have achieved happyhour\n" );
    return 0;
}