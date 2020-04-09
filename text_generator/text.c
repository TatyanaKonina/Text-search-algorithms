//
// Created by dmk01 on 18.02.2020.
//
#include "text.h"
#include <time.h>
#include <stdlib.h>
#include <string.h>


const int max_world_len = 10;

char *text_compiling ( char ** data , int words_num , int line_num ) {
    char *text = NULL;
    text = ( char* )calloc( words_num * max_world_len, sizeof ( char ) );
    srand ( time ( NULL ) );
    for ( int i  = 0; i < words_num  ;i++ ) {
        int r = rand() % line_num ;
        strcat ( text , data[r] );
    }
    return text;
}
