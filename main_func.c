#define _CRT_SECURE_NO_WARNINGS
#include <malloc.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>

#include "main_func.h"

const int max_world_len = 10;
const int str_size = 10;

#define ALPHSIZE 123
#define BASE 256
#define QMOD 13
#define NAIMEM 1 //уникальный только matched
#define RKMEM 4 //уникальные: matched, radix, patNumber, textNumber
#define BMHMEM 127 //уникальные: ind, textInd, positionn, equal, badCharaters с размером ALPHSIZE + внутри функции считается динамически выделенная память под relatedshifts
#define KMPEM 1 // уникальные : prefix_mass

extern const char alphabet[];
extern const int alphabetAccess[];
//-----------------------------------------------algorithms----------------------------------------------------------------------------------------------------------------
SearchResult* boyerMooreHorspoolMatcher(SearchRequest* request)
{
	SearchResult *result;
	int shift = 1, i = 0, ind = 1, textInd = 0, position = (request->pattern->needleSize) - 1, equal = 0;
	int badCharacters[ALPHSIZE]={0}, *relatedShifts;
	char safeCharacter=0;
	clock_t start, finish;
	start = clock();

	result = (SearchResult*) malloc(sizeof(SearchResult));
	result->matchedShifts = (int*) calloc(request->text->haystackSize, sizeof(int));
	result->numberOfMatches = 0;
	result->memoryWaste = BMHMEM * sizeof(int) + sizeof(int*) + request->pattern->needleSize * sizeof(int);
	result->numOfCompares = 0;
	result->numOfExtraOps = 0;

	relatedShifts = (int*) calloc(request->pattern->needleSize, sizeof(int));

	for (i = request->pattern->needleSize - 2; i >= 0; i--) {
		if (badCharacters[request->pattern->needle[i]] < 1) {  //extra comparison
			badCharacters[request->pattern->needle[i]] = ind;
			relatedShifts[ind-1] = shift;
			result->numOfExtraOps++; 
			ind++;
		}
		shift++;
	}

	shift = 0;

	while (shift <= (request->text->haystackSize) - (request->pattern->needleSize) ) {
		ind = (request->pattern->needleSize) - 1;
		textInd = position;
		equal = 1;
		safeCharacter = request->text->haystack[textInd];
		while (equal && ind >= 0) {
			if ( !(request->pattern->needle[ind] == request->text->haystack[textInd]) ) {
				equal = 0;
			}
			else {
			ind--;
			textInd--;
			}
			result->numOfCompares++;
		}
		if (equal) { //
			result->matchedShifts[result->numberOfMatches++] = shift;
		}
		if (badCharacters[safeCharacter]) { //
			shift += relatedShifts[badCharacters[safeCharacter] - 1];
			position += relatedShifts[badCharacters[safeCharacter] - 1];
			result->numOfExtraOps++; // extra comparison
		}
		else {
			shift += request->pattern->needleSize;
			position += request->pattern->needleSize;
			result->numOfExtraOps += 2; //х2 extra comparison (failed if statement)
		}
	}

	free(relatedShifts);
	finish = clock();
	result->workTime = (double)(finish -start) / CLOCKS_PER_SEC;

	return result;
}

SearchResult* naiveStringMatcher(SearchRequest* request)
{
	SearchResult* result;
	int shift = 0, matched = 0, i = 0;
	clock_t start, finish;
	start = clock();


	result = (SearchResult*)malloc(sizeof(SearchResult));
	result->matchedShifts = (int*)calloc(request->text->haystackSize, sizeof(int));
	result->memoryWaste = NAIMEM * sizeof(int);
	result->numberOfMatches = 0;
	result->numOfCompares = 0;
	result->numOfExtraOps = 0; //no extra comparisons?

	for (shift = 0; shift <= (request->text->haystackSize) - (request->pattern->needleSize); shift++) {
		matched = 0;
		for (i = 0; i < (request->pattern->needleSize); i++) {                        //
			if (request->pattern->needle[i] == request->text->haystack[shift + i]) {  //
				matched++;                                                            //может переделать цикл и дбавить в него if c break, чтобы лишних итераций не капало?
			}																		  //
			result->numOfCompares++;											      //
		}																			  //
		if (matched == request->pattern->needleSize) {
			result->matchedShifts[result->numberOfMatches++] = shift;
		}
	}

	finish = clock();
	result->workTime = (double)(finish - start) / CLOCKS_PER_SEC;

	return result;
}

SearchResult* rabinKarpMatcher(SearchRequest* request)
{
	SearchResult* result;
	int radix = 0, patNumber = 0, textNumber = 0, shift = 0, matched = 0, i = 0;
	clock_t start, finish;
	start = clock();

	result = (SearchResult*)malloc(sizeof(SearchResult));
	result->matchedShifts = (int*)calloc(request->text->haystackSize, sizeof(int));
	result->memoryWaste = RKMEM * sizeof(int);
	result->numberOfMatches = 0;
	result->numOfCompares = 0;
	result->numOfExtraOps = 0;

	radix = (int)pow((float)BASE, request->pattern->needleSize - 1) % QMOD;

	for (i = 0; i < request->pattern->needleSize; i++) {
		patNumber = (BASE * patNumber + request->pattern->needle[i]) % QMOD;
		textNumber = (BASE * textNumber + request->text->haystack[i]) % QMOD;
		result->numOfExtraOps += 2; //ну тут просто хэши создаются циклом, может тоже считать за extra operation?
	}

	for (shift = 0; shift <= (request->text->haystackSize) - (request->pattern->needleSize); shift++) {
		matched = 0;
		if (patNumber == textNumber) {
			for (i = 0; i < request->pattern->needleSize; i++) {                         //
				if (request->pattern->needle[i] == request->text->haystack[shift + i]) { //
					matched++;                                                           //может переделать цикл и дбавить в него if c break, чтобы лишних итераций не капало?
					result->numOfCompares++;                                             //
				}                                                                        //
			}                                                                            //
			if (matched == request->pattern->needleSize) {
				result->matchedShifts[result->numberOfMatches++] = shift;
			}
			result->numOfExtraOps++; //comparisons of hashes
		}
		if (shift <= (request->text->haystackSize) - (request->pattern->needleSize)) { //это сравнение вроде как лишнее, так как задано в цикле, но в книге оно было. Оставлять или не нужно?
			textNumber = (BASE * (textNumber - (request->text->haystack[shift]) * radix) + request->text->haystack[shift + request->pattern->needleSize]) % QMOD;
			result->numOfExtraOps++;
		}
		if (textNumber < 0) {
			textNumber += QMOD;
			result->numOfExtraOps++;
		}
	}

	finish = clock();
	result->workTime = (double)(finish - start) / CLOCKS_PER_SEC;

	return result;
}

SearchResult* knuthMorrisPrattMatcher(SearchRequest* request) {

	SearchResult* result;
	int* prefix_mass, i = 1, j = 0;

	clock_t start, finish;

	start = clock();

	result = (SearchResult*)malloc(sizeof(SearchResult));
	result->matchedShifts = (int*)calloc(request->text->haystackSize, sizeof(int));
	result->numberOfMatches = 0;
	result->memoryWaste = KMPEM * sizeof(int*) + request->pattern->needleSize * sizeof(int);
	result->numOfCompares = 0;
	result->numOfExtraOps = 0;

	prefix_mass = (int*)calloc(request->pattern->needleSize, sizeof(int));
	prefix_mass[0] = 0;
	result->numOfExtraOps = request->pattern->needleSize;

	while (i != request->pattern->needleSize) {
		if (request->pattern->needle[j] == request->pattern->needle[i]) {
			prefix_mass[i] = j + 1;
			i++;
			j++;
		}
		else {
			if (j == 0) {
				prefix_mass[i] = 0;
				i++;
			}
			else {
				j = prefix_mass[j - 1];
			}
		}
	}

	i = 0, j = 0;
	while (i != request->text->haystackSize) {
		while (j > 0 && request->pattern->needle[j] != request->text->haystack[i]) {
			result->numOfCompares++;
			j = prefix_mass[j - 1];
		}
		if (request->text->haystack[i] == request->pattern->needle[j]) {
			result->numOfCompares++;
			j++;
		}
		if (j == request->pattern->needleSize) {
			result->matchedShifts[result->numberOfMatches++] = i - request->pattern->needleSize + 1;

		}
		i++;
	}

	free(prefix_mass);
	finish = clock();
	result->workTime = (double)(finish - start) / CLOCKS_PER_SEC;

	return result;
}
//---------------------------------------------------------------file.h-------------------------------------------------------------------------------------------------------
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
//--------------------------------------------------------------generator-----------------------------------------------------------------------------------

char* string_compiling(char** alf, float* probability, int line_num, int shift, int sim_num) {

	float* tempt = (float*)calloc(line_num, sizeof(float));
	for (int i = 0; i < line_num; i++) {
		tempt[i] = probability[i];
	}

	char* string = (char*)calloc(sim_num, sizeof(char));
	int rand_digit;
	//составление диапазонов
	for (int i = 0; i < line_num; i++) {
		i == 0 ? tempt[i] = tempt[i] * 1000 : (tempt[i] = tempt[i] * 1000 + tempt[i / 2]);
	}
	int random_size = (int)tempt[line_num - 2];
	srand(time(NULL) + shift);
	for (int i = 0; i < sim_num - 1; i++) {
		rand_digit = rand() % (random_size + 1);
		for (int j = 0; j < line_num - 1; j++) {//проверка на подходящий диапазон
			if ((int)tempt[j] >= rand_digit) {
				strcat(string, alf[j]);
				break;
			}
		}
	}
	free(tempt);
	return string;
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

char* text_compiling(char** data, int line_num, int patterns_num, char* pattern, int shift, int words_num) {
	int* random_positions = NULL;
	char* text = NULL;
	int pointer = 0;
	text = (char*)calloc(words_num * max_world_len, sizeof(char));

	srand(time(NULL) + shift);
	if (patterns_num) { //если пользователь хочет текст с паттернами
		random_positions = (int*)calloc(patterns_num, sizeof(int));
		int i = 0;
		while (i < patterns_num) {//создаем массив рандомных позиций
			random_positions[i++] = rand() % words_num;
			for (int j = 0; j < i - 1; j++) {
				if (random_positions[j] == random_positions[i - 1]) {
					i--;
					break;
				}
			}
		}
		quick_sort(random_positions, 0, patterns_num - 1);//сортируем
	}
	for (int i = 0; i < words_num; i++) {
		if ((i == random_positions[pointer]) && patterns_num) {
			pointer++;               // если попали на               
			strcat(text, pattern);   //рандомную позиция                      
			strcat(text, " ");       // вставляем паттерн
		}
		else {
			int r = rand() % line_num;
			strcat(text, data[r]);
		}
	}
	if (patterns_num) {
		free(random_positions);
	}

	return text;
}

//----------------------------------------------dll-func---------------------------------------------------------------------------------------------------------------------

DLL_EXPORT SearchRequest* make_text_storage (int texts_num, int text_type, char* file_in, char* pattern, int pattern_num, int num) {
	
    //возвращает массив тестов
    SearchRequest* storage = (SearchRequest*)malloc(texts_num * sizeof(SearchRequest));
	char* text;
    switch (text_type) {
    case STROKE: {
        int line_num = words_num_in_file(file_in);
        char** data = read_data(file_in, line_num);
        char** alf = (char**)malloc((line_num) * sizeof(char*));
        for (int i = 0; i < line_num; i++)
        {
            alf[i] = (char*)malloc((max_world_len) * sizeof(char));
        }
        float* probability = (float*)calloc(line_num, sizeof(float));
        processing_file_with_probability(data, alf, probability, line_num);
		for (int i = 0; i < texts_num; i++) {
			text = string_compiling(alf, probability, line_num, i, num);
			Init_Memory_Request(&storage[i], text_type, pattern,text);
			//storage[i].text->haystack = string_compiling(alf, probability, line_num, i, num);
			//storage[i].text->haystackSize = strlen(storage[i].text->haystack);
		}
        break;
    }
    case TEXT: {
        int line_num = words_num_in_file(file_in);
        char** data = read_data(file_in, line_num);
        for (int i = 0; i < texts_num; i++) {
			text = text_compiling(data, line_num, pattern_num, pattern, i, num);
            Init_Memory_Request(&storage[i], text_type, pattern,text);
            //storage[i].text->haystack = text_compiling(data, line_num, pattern_num, pattern, i, num);
           // printf("%s\n", storage[i].text->haystack);
            //storage[i].text->haystackSize = strlen(storage[i].text->haystack);
        }
    }
   
    }
    return storage;
}

void Init_Memory_Request(SearchRequest* storage, int text_type, char* pattern,char * text) {
    //выделяет память под SearchRequest
    storage->pattern = (Pattern*)malloc(sizeof(Pattern));
    storage->pattern->needleSize = 0;
    storage->text = (Text*)malloc(sizeof(Text));
    storage->text->haystackSize = 0;
    storage->text->text_type = text_type;
    storage->pattern->needle = _strdup(pattern);
    storage->pattern->needleSize = strlen(pattern);
	storage->text->haystack = _strdup(text);
	storage->text->haystackSize = strlen(text);
}

DLL_EXPORT SearchRequest* make_result_storage(SearchRequest* texts_storage, int algorithm_type, int texts_num) {
    // прогоняет алгоритмы на всех текстах (на вход масссив тестов)
    //возвращает массив searchReasult
    SearchResult* storage = (SearchResult*)malloc(texts_num * sizeof(SearchResult));
	for (int i = 0; i < texts_num; i++) {
		switch (algorithm_type) {
		case BMHM: {
			storage[i] = *(boyerMooreHorspoolMatcher(&texts_storage[i]));
			break;
		}
		case NAIVE: {
			storage[i] = *(naiveStringMatcher(&texts_storage[i]));
			break;
		}
		case RKM: {
		    storage[i] = *(rabinKarpMatcher(&texts_storage[i]));
			break;
		}
		case KMPM: {
		    storage[i] = *(knuthMorrisPrattMatcher(&texts_storage[i]));
			break;
		}
		}
	}
    return storage;
}

DLL_EXPORT SearchResult* make_statictic(SearchResult* result_storage, int texts_num) {
    //делает статистику по алгортиму, на вход массив searchReasult
    SearchResult* StaticticResult;
    StaticticResult = (SearchResult*)malloc(sizeof(SearchResult));
    StaticticResult->workTime = 0;
    StaticticResult->numberOfMatches = 0;
    StaticticResult->memoryWaste = 0;
    StaticticResult->numOfCompares = 0;
    StaticticResult->numOfExtraOps = 0;
    for (int i = 0; i < texts_num; i++) {

        StaticticResult->numberOfMatches += result_storage[i].numberOfMatches;
        StaticticResult->numOfCompares += result_storage[i].numOfCompares;
        StaticticResult->numOfExtraOps += result_storage[i].numOfExtraOps;
        StaticticResult->workTime += result_storage[i].workTime;
        StaticticResult->memoryWaste += result_storage[i].memoryWaste;
    }

    StaticticResult->numOfCompares = StaticticResult->numOfCompares / texts_num;
    StaticticResult->numOfExtraOps = StaticticResult->numOfExtraOps / texts_num;
    StaticticResult->workTime = StaticticResult->workTime / texts_num;

    StaticticResult->numberOfMatches = StaticticResult->numberOfMatches / texts_num;
    
    StaticticResult->memoryWaste = StaticticResult->memoryWaste / texts_num;

    return StaticticResult;
}

DLL_EXPORT SearchRequest* make_parser_storage(char ** text, char* pattern, int texts_num,int len) {
	SearchRequest* storage = (SearchRequest*)malloc(texts_num * sizeof(SearchRequest));
	for (int i = 0; i < texts_num; i++) {
		Init_Memory_Request(&storage[i], BOOK, pattern,text[i]);
		if (storage[i].text->haystackSize > len) {
			storage[i].text->haystack[len] = '\0';
			storage[i].text->haystackSize = strlen(storage[i].text->haystack);
		}
	}
	return storage;
}
//-----------------------------------------------------------------------------------------
