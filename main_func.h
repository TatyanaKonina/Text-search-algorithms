#ifndef MAIN_FUNC_H
#define MAIN_FUNC_H

#define DLL_EXPORT __declspec(dllexport)
//-------------------------------------------------------structs-----------------------------------------------------------------------------------
typedef struct {
	char* needle;
	int needleSize;
} Pattern;

typedef struct {
	char* haystack;
	int haystackSize;
	int text_type;
} Text;

typedef struct {
	Pattern* pattern;
	Text* text;
} SearchRequest;

typedef struct {
	int* matchedShifts;
	int numberOfMatches;
	int numOfCompares;
	int numOfExtraOps;
	double workTime;
	int memoryWaste;
} SearchResult;

typedef enum Errors {
	ERROR_OPEN_PYFILE = -1,
	ERROR_MODULE_OBJECT = -2,
	ERROR_DICT_OBJECT = -3,
	ERROR_VALUE = -4,
	ERROR_FUNC = -5,
	ERROR_CALL_FUNC = -6,
	ERROR_OPEN_FILE = -7,
	ERROR_TEXT_TYPE = -8
}Errors;

typedef enum Text_type {
	STROKE = 0,
	TEXT = 1,
	BOOK = 2,
}Text_type;

typedef enum Algoritm_type {
	BMHM = 0,
	NAIVE = 1,
	RKM = 2,
	KMPM = 3
}Algoritm_type;

//----------------------------------------------------dll-------------------------------------

DLL_EXPORT SearchRequest* make_text_storage(int texts_num, int text_type, char* file_in, char* pattern, int pattern_num, int num);

void Init_Memory_Request(SearchRequest* storage, int text_type, char* pattern, char * text);

DLL_EXPORT SearchResult* make_result_storage(SearchRequest* texts_storage, int algorithm_type, int texts_num);

DLL_EXPORT SearchResult* make_statictic(SearchResult* result_storage, int texts_num);

DLL_EXPORT SearchRequest* make_parser_storage(char** text, char* pattern, int text_num,int len);

#endif
