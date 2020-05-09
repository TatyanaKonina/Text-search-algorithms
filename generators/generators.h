#ifndef TEXT_GENERATOR2_TEXT_H
#define TEXT_GENERATOR2_TEXT_H

void quick_sort(int* random_positions, int first, int last);

char* text_compiling(char** data, int line_num, int pattern_num, char* pattern,int shift);

char* string_compiling(char** alf, float* probability, int line_num,int shift);


#endif 
