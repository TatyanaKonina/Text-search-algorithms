#include <stdio.h>
#include <stdlib.h>
#include "file.h"
#include "text.h"
int main(int argc , char * argv[] ) {
    if ( argc != 3) {
        printf ("ERROR" );
        return -2;
    }
    char * file_name_in = argv[ 1 ];
    int customer_words_num = atoi(argv[ 2 ]);
    int line_num = words_num ( argv [ 1 ] );
    char ** data = read_data ( file_name_in , line_num );
    char * text = text_compiling ( data, customer_words_num , line_num );
    printf("%s", text);
    return 0;
}