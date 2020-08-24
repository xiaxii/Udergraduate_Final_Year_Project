//
//  OS4.c
//  Test
//
//  Created by 夏曦 on 2019/4/16.
//  Copyright © 2019 夏曦. All rights reserved.
//

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

void *worker(void *param);

#define NUMBER_OF_DARTS      50000000
#define NUMBER_OF_THREADS    2

/* the number of hits in the circle */
int circle_count = 0;
pthread_mutex_t lock;

/*
 * Generates a double precision random number
 */
double random_double()
{
    return random() / ((double)RAND_MAX + 1);
    //every call to rand gives a sudo random number between 0 and RAND_MAX
}

int main (int argc, const char * argv[]) {
    int darts_per_thread = NUMBER_OF_DARTS/ NUMBER_OF_THREADS;
    int i;
    
    double estimated_pi;
    
    /*mutex clock*/
    pthread_mutex_init(&lock,NULL);
    
    /*pthread_t is used to initialise the thread ID*/
    pthread_t workers[NUMBER_OF_THREADS];
    
    
    /* seed the random number generator */
    srandom((unsigned)time(NULL));
    
    /*creat threads*/
    for (i = 0; i < NUMBER_OF_THREADS; i++)
        pthread_create(&workers[i], 0, worker, &darts_per_thread);
    
    /*wait for the end of a thread, do resource recycling*/
    for (i = 0; i < NUMBER_OF_THREADS; i++)
        pthread_join(workers[i],NULL);
    
    /* estimate Pi */
    estimated_pi = 4.0 * circle_count / NUMBER_OF_DARTS;
    
    printf("Pi = %f\n",estimated_pi);
    
    return 0;
}

void *worker(void *param)
{
    int number_of_darts;
    number_of_darts = *((int *)param);
    int i;
    int hit_count = 0;
    double x,y;
    
    for (i = 0; i < number_of_darts; i++) {
        
        /* generate random numbers between -1.0 and +1.0 (exclusive) */
        x = random_double() * 2.0 - 1.0;
        y = random_double() * 2.0 - 1.0;
        
        if ( sqrt(x*x + y*y) < 1.0 )
            ++hit_count;
    }
    /*lock*/
    pthread_mutex_lock(&lock);
    printf("locked!\n");
    circle_count += hit_count;
    /*unlock*/
    pthread_mutex_unlock(&lock);
    printf("unlocked!\n");
    
    pthread_exit(0);
}


