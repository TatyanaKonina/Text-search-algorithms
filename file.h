#ifndef FILE_H
#define FILE_H

int words_num_in_file(char* name);

char** read_data(char* file_name, int line_num);

void processing_file_with_probability(char** data, char** alf, float* probability, int line_num);

#endif //FILE_H
