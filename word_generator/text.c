//
// Created by dmk01 on 18.02.2020.
//
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <malloc.h>
#include "text.h"
const int max_world_len = 10;
char *text_compiling(char **data, int words_num,int line_num){
    srand(time(NULL));
    char * out = (char*) calloc (words_num * max_world_len,sizeof(char));
    for (int i  = 0; i < words_num * max_world_len ;i++){
        int r = rand() % line_num ;
        strcpy(out, data[r]);
    }
    return out;
}
