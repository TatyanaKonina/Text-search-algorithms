//
// Created by dmk01 on 18.02.2020.
//

#ifndef TEXT_GENERATOR_FILE_H
#define TEXT_GENERATOR_FILE_H
int file_size ( char * file_name );

void write_data ( char * name , char * data_out );

char ** read_data(char *file_name,int size_file, int *line_num);

#endif //TEXT_GENERATOR_FILE_H
