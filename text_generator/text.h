//
// Created by dmk01 on 18.02.2020.
//

#ifndef TEXT_GENERATOR2_TEXT_H
#define TEXT_GENERATOR2_TEXT_H
typedef struct  {
    char* haystack;
    int haystackSize;
    enum  {
        Random_stroke,
        Random_words,
        Article,
        User_string
    } Type_text ;
} Text;

typedef struct {
    char* needle;
    int needleSize;
    enum  {
        Generated_word,
        Word,
        User_word
    } Type_pattern ;
} Pattern;

typedef struct {
    Pattern* pattern;
    Text* text;
} SearchRequest;


char *text_compiling ( char **data , int words_num , int line_num );
#endif //TEXT_GENERATOR2_TEXT_H
