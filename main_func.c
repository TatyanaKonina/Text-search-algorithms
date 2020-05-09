#include "structs.h"
#include "generators.h"
#include "main_func.h"
#include <malloc.h>
#include <stdlib.h>
#include "my_parser.h"
#include "file.h"


SearchResult* statictics_for_stroke( SearchResult* (algorithm)(SearchRequest* request), int texts_num, char* pattern, char *file_in) {
    int pointer = 0;

    SearchResult* StaticticResult = NULL;
    StaticticResult = (SearchResult*)malloc(sizeof(SearchResult));
    StaticticResult->workTime = 0;
    StaticticResult->numberOfMatches = 0;
    StaticticResult->memoryWaste = 0;
    StaticticResult->numOfCompares = 0;
    StaticticResult->numOfExtraOps = 0;

    SearchRequest* Request;
    Request = (SearchRequest*)malloc(sizeof(SearchRequest));
    Request->pattern = (Pattern*)malloc(sizeof(Pattern));
    Request->pattern->needleSize = 0;
    Request->text = (Text*)malloc(sizeof(Text));
    Request->text->haystackSize = 0;

    Request->pattern->needle = _strdup(pattern);
    Request->pattern->needleSize = strlen(pattern);


    int line_num = words_num_in_file(file_in);

    char** data = read_data(file_in, line_num);

    char** alf = (char**)malloc((line_num) * sizeof(char*));//???????? ??????
    for (int i = 0; i < line_num; i++)
    {
        alf[i] = (char*)malloc((10) * sizeof(char));
    }

    float* probability = (float*)calloc(line_num, sizeof(float));

    processing_file_with_probability(data, alf, probability, line_num);

    for (int i = 0; i < texts_num; i++) {
        
        Request->text->haystack = string_compiling(alf, probability, line_num,i);
        printf("%s\n\n\n", Request->text->haystack);
        Request->text->haystackSize = strlen(Request->text->haystack);
        //free(Request->text->haystack);

        SearchResult* Result;
        Result = algorithm(Request);
        StaticticResult->numberOfMatches += Result->numberOfMatches;
        StaticticResult->numOfCompares += Result->numOfCompares;
        StaticticResult->numOfExtraOps += Result->numOfExtraOps;
        StaticticResult->workTime += Result->workTime;
        StaticticResult->memoryWaste += Result->memoryWaste;
    }

    

    //for (int i = 0; i < line_num ; i++)  // цикл по строкам
    //	free(alf[i]);   // освобождение памяти под строку
    //free(alf);

    //free(data);

    //free(probability);

    StaticticResult->numberOfMatches = StaticticResult->numberOfMatches / texts_num;
    StaticticResult->numOfCompares = StaticticResult->numOfCompares / texts_num;
    StaticticResult->numOfExtraOps = StaticticResult->numOfExtraOps / texts_num;
    StaticticResult->workTime = StaticticResult->memoryWaste / texts_num;
    StaticticResult->memoryWaste = StaticticResult->memoryWaste / texts_num;

    return  StaticticResult;
}
SearchResult* statictics_for_text( int patterns_num, SearchResult* (algorithm)(SearchRequest* request), int texts_num, char* pattern, char* file_in) {
    int pointer = 0;
    SearchResult* StaticticResult;
    StaticticResult = (SearchResult*)malloc(sizeof(SearchResult));
    StaticticResult->workTime = 0;
    StaticticResult->numberOfMatches = 0;
    StaticticResult->memoryWaste = 0;
    StaticticResult->numOfCompares = 0;
    StaticticResult->numOfExtraOps = 0;

    SearchRequest* Request;
    Request = (SearchRequest*)malloc(sizeof(SearchRequest));
    Request->pattern = (Pattern*)malloc(sizeof(Pattern));
    Request->pattern->needleSize = 0;
    Request->text = (Text*)malloc(sizeof(Text));
    Request->text->haystackSize = 0;


    Request->pattern->needle = _strdup(pattern);
    Request->pattern->needleSize = strlen(pattern);

    int line_num = words_num_in_file(file_in);
    char** data = read_data(file_in, line_num);


    for (int i = 0; i < texts_num; i++) {
          Request->text->haystack = text_compiling(data, line_num, patterns_num, pattern,i);
          Request->text->haystackSize = strlen(Request->text->haystack);
          printf("%s\n\n\n", Request->text->haystack);
          SearchResult* Result;
          Result = algorithm(Request);
          StaticticResult->numberOfMatches += Result->numberOfMatches;
          StaticticResult->numOfCompares += Result->numOfCompares;
          StaticticResult->numOfExtraOps += Result->numOfExtraOps;
          StaticticResult->workTime += Result->workTime;
          StaticticResult->memoryWaste += Result->memoryWaste;
    }

    StaticticResult->numberOfMatches = StaticticResult->numberOfMatches / texts_num;
    StaticticResult->numOfCompares = StaticticResult->numOfCompares / texts_num;
    StaticticResult->numOfExtraOps = StaticticResult->numOfExtraOps / texts_num;
    StaticticResult->workTime = StaticticResult->memoryWaste / texts_num;
    StaticticResult->memoryWaste = StaticticResult->memoryWaste / texts_num;

    return  StaticticResult;
}
SearchResult* statictics_for_book(SearchResult* (algorithm)(SearchRequest* request), int texts_num, char* pattern) {
    int pointer = 0;
    SearchResult* StaticticResult;
    StaticticResult = (SearchResult*)malloc(sizeof(SearchResult));
    StaticticResult->workTime = 0;
    StaticticResult->numberOfMatches = 0;
    StaticticResult->memoryWaste = 0;
    StaticticResult->numOfCompares = 0;
    StaticticResult->numOfExtraOps = 0;

    SearchRequest* Request;
    Request = (SearchRequest*)malloc(sizeof(SearchRequest));
    Request->pattern = (Pattern*)malloc(sizeof(Pattern));
    Request->pattern->needleSize = 0;
    Request->text = (Text*)malloc(sizeof(Text));
    Request->text->haystackSize = 0;

    Request->pattern->needle = _strdup(pattern);
    Request->pattern->needleSize = strlen(pattern);

    PyObject* pFunc;
    pFunc = python_func_init();
    for (int i = 0; i < texts_num; i++) {
         Request->text->haystack = _strdup(parser(pFunc));
         Request->text->haystackSize = strlen(Request->text->haystack);
         SearchResult* Result;
         Result = algorithm(Request);
         StaticticResult->numberOfMatches += Result->numberOfMatches;
         StaticticResult->numOfCompares += Result->numOfCompares;
         StaticticResult->numOfExtraOps += Result->numOfExtraOps;
         StaticticResult->workTime += Result->workTime;
         StaticticResult->memoryWaste += Result->memoryWaste;
    }
   
    python_clean(pFunc);

    StaticticResult->numberOfMatches = StaticticResult->numberOfMatches / texts_num;
    StaticticResult->numOfCompares = StaticticResult->numOfCompares / texts_num;
    StaticticResult->numOfExtraOps = StaticticResult->numOfExtraOps / texts_num;
    StaticticResult->workTime = StaticticResult->memoryWaste / texts_num;
    StaticticResult->memoryWaste = StaticticResult->memoryWaste / texts_num;

    return  StaticticResult;


}