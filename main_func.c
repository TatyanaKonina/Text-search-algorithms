#define _CRT_SECURE_NO_WARNINGS
#include <malloc.h>
#include <stdlib.h>

#include "structs.h"
#include "generators.h"
#include "main_func.h"
#include "my_parser.h"
#include "file.h"


SearchRequest* make_text_storage(int texts_num, int text_type, char* file_in, char* pattern, int pattern_num) {
    //возвращает массив тестов
    SearchRequest* storage = (SearchRequest*)malloc(texts_num * sizeof(SearchRequest));
    switch (text_type) {
    case 0: {
        int line_num = words_num_in_file(file_in);
        char** data = read_data(file_in, line_num);
        char** alf = (char**)malloc((line_num) * sizeof(char*));
        for (int i = 0; i < line_num; i++)
        {
            alf[i] = (char*)malloc((10) * sizeof(char));
        }
        float* probability = (float*)calloc(line_num, sizeof(float));
        processing_file_with_probability(data, alf, probability, line_num);
        for (int i = 0; i < texts_num; i++) {
            Init_Memory_Request(&storage[i], text_type, pattern);
            storage[i].text->haystack = string_compiling(alf, probability, line_num, i);
            printf("%s\n", storage[i].text->haystack);
            storage[i].text->haystackSize = strlen(storage[i].text->haystack);
        }
        break;
    }
    case 1: {
        int line_num = words_num_in_file(file_in);
        char** data = read_data(file_in, line_num);
        for (int i = 0; i < texts_num; i++) {
            Init_Memory_Request(&storage[i], text_type,pattern);
            storage[i].text->haystack = text_compiling(data, line_num, pattern_num, pattern, i);
            printf("%s\n", storage[i].text->haystack);
            storage[i].text->haystackSize = strlen(storage[i].text->haystack);
        }
        break;
    }
    case 2: {
        PyObject* pFunc;
        pFunc = python_func_init();
        for (int i = 0; i < texts_num; i++) {
            Init_Memory_Request(&storage[i], text_type,pattern);
            storage[i].text->haystack = parser(pFunc);
            printf("%s\n", storage[i].text->haystack);
            storage[i].text->haystackSize = strlen(storage[i].text->haystack);
        }
    }
    }
    return storage;
}

void Init_Memory_Request(SearchRequest* storage, int text_type, char * pattern) {
    //выделяет память
    storage->pattern = (Pattern*)malloc(sizeof(Pattern));
    storage->pattern->needleSize = 0;
    storage->text = (Text*)malloc(sizeof(Text));
    storage->text->haystackSize = 0;
    storage->text->text_type = text_type;

    storage->pattern->needle = _strdup(pattern);
    storage->pattern->needleSize = strlen(pattern);
}

SearchRequest* make_result_storage(SearchRequest* texts_storage, SearchResult* (algorithm)(SearchRequest* request), int texts_num) {
    // прогоняет алгоритмы на всех текстах (на вход масссив тестов)
    //возвращает массив searchReasult
    SearchResult* storage = (SearchResult*)malloc(texts_num * sizeof(SearchResult));
    for (int i = 0; i < texts_num; i++) {
        storage[i] = *(algorithm(&texts_storage[i]));
    }
    return storage;
}

SearchResult* make_statictic(SearchResult* result_storage, int texts_num) {
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

    StaticticResult->numberOfMatches = StaticticResult->numberOfMatches / texts_num;
    StaticticResult->numOfCompares = StaticticResult->numOfCompares / texts_num;
    StaticticResult->numOfExtraOps = StaticticResult->numOfExtraOps / texts_num;
    StaticticResult->workTime = StaticticResult->workTime / texts_num;
    StaticticResult->memoryWaste = StaticticResult->memoryWaste / texts_num;
}
