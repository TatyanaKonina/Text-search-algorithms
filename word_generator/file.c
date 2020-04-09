//
// Created by dmk01 on 18.02.2020.
//
#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include <stdlib.h>
#include "file.h"
int file_size ( char * file_name ) {
    FILE*in = fopen ( file_name , "r" );
    if ( in  == NULL ) {
        return -1;
    }
    fseek ( in ,0L ,SEEK_END );
    int size = ftell ( in ) + 1;
    fseek ( in ,0L , SEEK_SET );
    fclose ( in );
    return size;
}

char ** read_data(char *file_name,int size_file, int *line_num){
    char** data = ( char** ) calloc ( size_file, sizeof ( char* ));
    for ( int i = 0 ; i < size_file ; i++ ) {
        data[ i ] = ( char* ) calloc (( size_file), sizeof ( char ));
    }
    FILE * file = fopen(file_name,"r");
    if(file == NULL){
        return -1;
    }
    int pointer = 0;
    while(!feof(file)) {
        fgets(data[pointer],100, file);
        data[pointer][strlen(data[pointer]) - 1] = ' ';
        (*line_num)++;
        pointer++;
    };
    fclose ( file );
    return data;
}

void write_data ( char * name , char * data_out ) {
    FILE *out = fopen ( name ,  "w" );
    fputs ( data_out , out );
    fclose ( out ) ;
}
