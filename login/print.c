#include "print.h"
#define crazy_num 2000
// Pretty lame but how am I supposed to know the maximal characters in a .html line?
//#define DEBUG

// Prints to browser the contents of the file in the string file path
int print(char * filePath)
{
	#ifdef DEBUG
		printf("Entered print()\n");
	#endif

	char * currentLine = (char*) malloc (crazy_num);
	printf("%s%c%c\n","Content-Type:text/html;charset=iso-8859-1", 13, 10);
    // First print out the header file
    
    // static login_header.html because C's string functions suck
    FILE *headerFile = fopen("layout/login_header.html", "rt");
    if ( headerFile != NULL ) {
        while (fgets(currentLine, crazy_num, headerFile) != NULL) {
            printf("%s\n", filter(currentLine, 32, 126));
            // filter thing = ASCII character workaround
            memset(currentLine, ' ', strlen(currentLine) + 1);
        }
        fclose(headerFile);
    } else {
        printf("Omg header file wtf");
    }

	FILE * pFile = fopen(filePath, "rt");
	if(pFile != NULL){
		while(fgets(currentLine, crazy_num, pFile) != NULL){
			printf("%s\n", filter(currentLine, 32, 126));
			memset(currentLine, ' ', strlen(currentLine) + 1); // extra 1 so that '\0' gets set to ' '
		}
		fclose(pFile);
	} else {

	#ifdef DEBUG
		printf("Unable to load file %s\n", filePath);
	#endif

	}
	#ifdef DEBUG
		printf("Exit print()\n");
	#endif
	return 0;
}


// Filters a string so it consists exclusively of characters between minASCII and maxASCII
// This is done with char math only, '\0' is appended at the end of the filtered string.
char * filter(char * src, int minASCII, int maxASCII)
{
	#ifdef DEBUG
		printf("Entered filter()\n");
	#endif
	// The filtered string's length is at most equal to the source's length
	char * dst = (char*) malloc (strlen(src)); 
	*dst = '\0';

	int dstIndex;
	for(dstIndex = 0; *src != '\0'; src++){
		if(*src >= minASCII &&
		   *src <= maxASCII){
			*(dst + dstIndex) = *src;
			dstIndex++;
		}
	}
	*(dst + dstIndex) = '\0';

	#ifdef DEBUG
		printf("Exit filter()\n");
	#endif

	return dst;
}

