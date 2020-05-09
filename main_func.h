#ifndef MAIN_FUNC_H
#define MAIN_FUNC_H

#include "structs.h"


SearchResult* statictics_for_stroke( SearchResult* (algorithm)(SearchRequest* request), int texts_num, char* pattern, char * file_in);

SearchResult* statictics_for_text( int patterns_num, SearchResult* (algorithm)(SearchRequest* request), int texts_num, char* pattern, char* file_in);

SearchResult* statictics_for_book(SearchResult* (algorithm)(SearchRequest* request), int texts_num, char* pattern);
#endif

