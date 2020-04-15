#ifndef SEARCHALGS_H
#define SEARCHALGS_H
#include "structs.h"

typedef enum ALGTYPES {
	NAI, RK, BMH,KMP
};

#define ALPHSIZE 123
#define BASE 256
#define QMOD 13
#define NAIMEM 1 //уникальный только matched
#define RKMEM 4 //уникальные: matched, radix, patNumber, textNumber
#define BMHMEM 127 //уникальные: ind, textInd, positionn, equal, badCharaters с размером ALPHSIZE + внутри функции считается динамически выделенная память под relatedshifts
#define KMPEM 1 // уникальные : prefix_mass

extern const char alphabet[];
extern const int alphabetAccess[];

SearchResult* naiveStringMatcher(SearchRequest* request);
SearchResult* rabinKarpMatcher(SearchRequest* request);
SearchResult* boyerMooreHorspoolMatcher(SearchRequest* request);
SearchResult* knuthMorrisPrattMatcher(SearchRequest * request);

#endif