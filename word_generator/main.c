#include <stdio.h>
#include <stdlib.h>
#include "file.h"
#include "text.h"
int main(int argc , char * argv[] ) {
    if ( argc != 4) {
        printf ("ERROR" );
        return -2;
    }
    char * file_name_in = argv[ 1 ];
    char * file_name2 = argv[ 2 ] ;
    int words_num = atoi(argv[ 3 ]);
    int line_num = 0;
    int size_file = file_size ( file_name_in );
    char ** data = read_data (file_name_in,size_file,&line_num);
    char * text_out = text_compiling(data,words_num , line_num);
    write_data ( file_name2 , text_out );
    return 0;
}