//
// Created by dmk01 on 18.02.2020.
//

#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include "file.h"

const int str_size = 10;

char ** read_data ( char * file_name,  int line_num ) {
    char** data = ( char** ) calloc ( line_num, sizeof ( char* ));
    for ( int i = 0 ; i < line_num ; i++ ) {
        data[ i ] = ( char* ) calloc (( str_size ), sizeof ( char ));
    }
    FILE * file = fopen(file_name,"r");
    if(file == NULL){
        return -1;
    }
    int pointer = 0;
    while(!feof(file)) {
        fgets(data[pointer],100, file);
        data[pointer][strlen(data[pointer]) - 1] = ' ';
        pointer++;
    }
    fclose ( file );

    return data;
}

int words_num ( char * file_name ) {
    int line_num = 0, any;
    FILE * file = fopen (file_name,"r");
    if ( file == NULL ) {
        return -1;
    }

    do {
        any = fgetc ( file );
        if( any == '\n') {
            line_num++;
        }
    } while (any != EOF);

    line_num++;

    fclose ( file );

    return line_num;
}

