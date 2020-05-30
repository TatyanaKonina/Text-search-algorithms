#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include "structs.h"
#include "stdlib.h"

const int str_size = 10;

char** read_data(char* file_name, int line_num) {
	char** data = (char**)calloc(line_num, sizeof(char*));
	for (int i = 0; i < line_num; i++) {
		data[i] = (char*)calloc((str_size), sizeof(char));
	}
	FILE* file = fopen(file_name, "r");
	if (file == NULL) {
		exit(ERROR_OPEN_FILE);
	}
	int pointer = 0;
	while (!feof(file)) {
		fgets(data[pointer], 100, file);
		data[pointer][strlen(data[pointer]) - 1] = ' ';
		pointer++;
	}
	fclose(file);
	return data;
}

int words_num_in_file(char* file_name) {
	int line_num = 0, any;
	FILE* file = fopen(file_name, "r");
	if (file == NULL) {
		return ERROR_OPEN_FILE;
	}
	do {
		any = fgetc(file);
		if (any == '\n') {
			line_num++;
		}
	} while (any != EOF);

	line_num++;

	fclose(file);

	return line_num;
}

void processing_file_with_probability(char** data, char** alf, float* probability, int line_num) {
	int i = 0;
	for (i = 0; i < line_num; i++) {
		char* istr;
		istr = strtok(data[i], " \n");
		if (istr != NULL) {
			alf[i] = istr;
			istr = strtok(NULL, " \n");
			probability[i] = atof(istr);
		}
	}
}
