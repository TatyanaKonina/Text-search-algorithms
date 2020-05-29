#ifndef MAIN_FUNC_H
#define MAIN_FUNC_H

#include "structs.h"


SearchRequest* make_text_storage(int texts_num, int text_type, char* file_in, char* pattern, int pattern_num, int num);
 
void Init_Memory_Request(SearchRequest* storage, int text_type, char * pattern);
 
SearchRequest* make_result_storage(SearchRequest* texts_storage, SearchResult* (algorithm)(SearchRequest* request), int texts_num);
 
SearchResult* make_statictic(SearchResult* result_storage, int texts_num);
#endif

