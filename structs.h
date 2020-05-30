#ifndef STRUCTS_H
#define STRUCTS_H

typedef struct {
	char* needle;
	int needleSize;
} Pattern;

typedef struct {
	char* haystack;
	int haystackSize;
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