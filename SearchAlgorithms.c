#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "searchalgs.h"
#include "structs.h"

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
			if (badCharacters[safeCharacter]) { //
				shift += relatedShifts[badCharacters[safeCharacter] - 1];
				position += relatedShifts[badCharacters[safeCharacter] - 1];
				result->numOfExtraOps += 2; //х2 extra comparison
			}
			else {
				shift += request->pattern->needleSize;
				position += request->pattern->needleSize;
				result->numOfExtraOps += 2; //х2 extra comparison (failed if statement)
			}
		}
		else {
			if (badCharacters[request->text->haystack[textInd]]) { //
				shift += relatedShifts[badCharacters[request->text->haystack[textInd]] - 1];
				position += relatedShifts[badCharacters[request->text->haystack[textInd]] - 1];
				result->numOfExtraOps += 2; //х2 extra comparison (failed if(equal) statement)
			}
			else {
				shift += request->pattern->needleSize;
				position += request->pattern->needleSize;
				result->numOfExtraOps += 2; //х2 extra comparison (failed if statement + failed if(equal) statement)
			}
		}
	}

	free(relatedShifts);
	finish = clock();
	result->workTime = (double)(finish -start) / CLOCKS_PER_SEC;

	return result;
}

SearchResult* naiveStringMatcher(SearchRequest* request)
{
	SearchResult *result;
	int shift = 0, matched = 0, i = 0;
	clock_t start, finish;
	start = clock();


	result = (SearchResult*) malloc(sizeof(SearchResult));
	result->matchedShifts = (int*) calloc(request->text->haystackSize, sizeof(int));
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
		if (matched == request->pattern->needleSize ) {
			result->matchedShifts[result->numberOfMatches++] = shift;
		}
	}

	finish = clock();
	result->workTime = (double)(finish -start) / CLOCKS_PER_SEC;

	return result;
}

SearchResult* rabinKarpMatcher(SearchRequest* request)
{
	SearchResult *result;
	int radix = 0, patNumber = 0, textNumber = 0, shift = 0, matched = 0, i = 0;
	clock_t start, finish;
	start = clock();

	result = (SearchResult*) malloc(sizeof(SearchResult));
	result->matchedShifts = (int*) calloc(request->text->haystackSize, sizeof(int));
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

	for (shift = 0; shift <= (request->text->haystackSize) - (request->pattern->needleSize) ; shift++) {
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
		if (shift <= (request->text->haystackSize) - (request->pattern->needleSize) ) { //это сравнение вроде как лишнее, так как задано в цикле, но в книге оно было. Оставлять или не нужно?
			textNumber = (BASE * (textNumber - (request->text->haystack[shift]) * radix) + request->text->haystack[shift + request->pattern->needleSize]) % QMOD;
			result->numOfExtraOps++;
		}
		if (textNumber < 0) {
			textNumber += QMOD;
			result->numOfExtraOps++;
		}
	}

	finish = clock();
	result->workTime = (double)(finish -start) / CLOCKS_PER_SEC;

	return result;
}

SearchResult *knuthMorrisPrattMatcher(SearchRequest *request) {

    SearchResult *result;
    int *prefix_mass, i = 1, j = 0;

    clock_t start, finish;

    start = clock();

    result = (SearchResult *) malloc(sizeof(SearchResult));
    result->matchedShifts = (int *) calloc(request->text->haystackSize, sizeof(int));
    result->numberOfMatches = 0;
    result->memoryWaste =  KMPEM * sizeof(int *) + request->pattern->needleSize * sizeof(int);
    result->numOfCompares = 0;
    result->numOfExtraOps = 0;

    prefix_mass = (int *) calloc(request->pattern->needleSize, sizeof(int));
    prefix_mass[0] = 0;
    result->numOfExtraOps = request->pattern->needleSize;

    while (i != request->pattern->needleSize) {
        if (request->pattern->needle[j] == request->pattern->needle[i]) {
            prefix_mass[i] = j + 1;
            i++;
            j++;
        } else {
            if (j == 0) {
                prefix_mass[i] = 0;
                i++;
            } else {
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
    result->workTime = (double) (finish - start) / CLOCKS_PER_SEC;

    return result;
}

int main()
{
	SearchRequest *request;
	SearchResult *result;
	int numberofmatches = 0, answertext = 1, answerword = 1, i = 0, choice = 0;
	char text[50] = {0}, pattern[20] = {0}, catchenters[2];

	request = (SearchRequest*) malloc(sizeof(SearchRequest));
	request->pattern = (Pattern*) malloc(sizeof(Pattern));
	request->text = (Text*) malloc(sizeof(Text));

	while(answertext) {
		gets(text);
		request->text->haystack = text;
		request->text->haystackSize = strlen(text);
		answerword = 1;
		while(answerword) {
			gets(pattern);
			request->pattern->needle = pattern;
			request->pattern->needleSize = strlen(pattern);
			puts("What algorithm would you like to use?\n0.Naive matcher\n1.RK\n2.BMH");
			scanf("%d", &choice);
			switch (choice) {
			case NAI:
				result = naiveStringMatcher(request);
				break;
			case RK:
				result = rabinKarpMatcher(request);
				break;
			case BMH:
				result = boyerMooreHorspoolMatcher(request);
			break;
			}

			printf("it has been found %d matches in text with shifts: ", result->numberOfMatches);
			for (i = 0; i < result->numberOfMatches; i++) {
				printf("%d ",result->matchedShifts[i]);
			}
			printf("\ntime spent: %.10f", result->workTime);
			printf("\nmemory wasted: %d", result->memoryWaste);
			printf("\nnumber of symbol comparisons: %d", result->numOfCompares);
			printf("\nnumber of extra operations: %d", result->numOfExtraOps);

			free(result->matchedShifts);
			free(result);
			puts("\nfind another word in this text?\n yes - 1   no - 0");
			scanf("%d", &answerword);
			gets(catchenters);
		}
		puts("continue searching in the another text?\n yes - 1   no - 0");
		scanf("%d", &answertext);
		gets(catchenters);
	}

	free(request->pattern);
	free(request->text);
	free(request);

	return 0;
}

