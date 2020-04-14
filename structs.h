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
	int *matchedShifts;
	int numberOfMatches;
	int numOfCompares;
	int numOfExtraOps;
	double workTime;
	int memoryWaste;
} SearchResult;

#endif
