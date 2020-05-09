#define _CRT_SECURE_NO_WARNINGS
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include"structs.h"
#include "generators.h"
#include "file.h"

#define WORDS_NUM 1000

const int max_world_len = 10;


char* string_compiling(char** alf, float* probability, int line_num,int shift) {

	float* tempt = (float*)calloc(line_num, sizeof(float));
	for (int i = 0; i < line_num; i++) {
		tempt[i] = probability[i];
	}

	char* string = (char*)calloc(WORDS_NUM * max_world_len, sizeof(char));
	int rand_digit;
	for (int i = 0; i < line_num; i++) {
		i == 0 ? tempt[i] = tempt[i] * 1000 : (tempt[i] = tempt[i] * 1000 + tempt[i / 2]);
	}
	int random_size = (int)tempt[line_num - 2];
	srand(time(NULL) + shift);
	for (int i = 0; i < WORDS_NUM * max_world_len - 1; i++) {
		rand_digit = rand() % (random_size + 1);
		for (int j = 0; j < line_num - 1; j++) {
			if ((int)tempt[j] >= rand_digit) {
				strcat(string, alf[j]);
				break;
			}
		}
	}
	free(tempt);
	return string;
}

char* text_compiling(char** data, int line_num, int patterns_num, char* pattern,int shift) {

	char* text = NULL;
	int pointer = 0;
	text = (char*)calloc(WORDS_NUM * max_world_len, sizeof(char));

	srand(time(NULL) + shift);
	if (patterns_num) {
		int* random_positions = (int*)calloc(patterns_num, sizeof(int));
		int i = 0;
		while (i < patterns_num) {
			random_positions[i++] = rand() % WORDS_NUM;
			for (int j = 0; j < i - 1; j++) {
				if (random_positions[j] == random_positions[i - 1]) {
					i--;
					break;
				}
			}
		}
		quick_sort(random_positions, 0, patterns_num - 1);
		for (i = 0; i < WORDS_NUM; i++) {
			if (i == random_positions[pointer]) {
				pointer++;
				strcat(text, pattern);
				strcat(text, " ");
			}
			else {
				int r = rand() % line_num;
				strcat(text, data[r]);
			}
		}
		free(random_positions);
	}
	else {
		for (int i = 0; i < WORDS_NUM; i++) {
			int r = rand() % line_num;
			strcat(text, data[r]);
		}
	}
	return text;
}

void quick_sort(int* random_positions, int first, int last)
{
	int i = first, j = last, x = random_positions[(first + last) / 2];

	do {
		while (random_positions[i] < x) i++;
		while (random_positions[j] > x) j--;

		if (i <= j) {
			if (random_positions[i] > random_positions[j]) {
				int temp = random_positions[i];
				random_positions[i] = random_positions[j];
				random_positions[j] = temp;
			}
			i++;
			j--;
		}
	} while (i <= j);

	if (i < last)
		quick_sort(random_positions, i, last);
	if (first < j)
		quick_sort(random_positions, first, j);
}