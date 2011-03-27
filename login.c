#include <stdio.h>
#include <stdlib.h>
#define MAX_CHAR 300
#define MAX_LINE 100
#define FILEPATH "/Users/Eleyine/loginErrorMessage.html"

/** NOTE: The C program won't compile if MAX_CHAR and MAX_LINE aren't correctly defined. 300 and 100 work in
 * the case of our loginErrorMessage.html file.
 */

/* Prototype(s) */
char * toString(FILE * pFile);

/** Main Function */

int main(void)
{
	int i, j;
	printf("%s%c%c\n","Content-Type:text/html;charset=iso-8859-1", 13, 10);
	FILE * pFile = fopen(FILEPATH, "rt");
	if(pFile != NULL){
		char * htmlContent = (char*) malloc (MAX_CHAR * MAX_LINE);
		htmlContent = toString(pFile);
		fclose(pFile);
		for(i = 0; i < MAX_LINE; i++){
			for(j = 0; j < MAX_CHAR; j++){
				printf("%c", *(htmlContent + i*MAX_CHAR + j));
			}
		}
	}
}

/**
 * Converts the contents of the text file pointed by pFile to a 2D char array [MAX_LINE][MAX_CHAR] 
 * and returns a pointer to the 2D char array (i.e. array of strings)
 */

char * toString(FILE * pFile)
{
	char * content = (char*) malloc (MAX_CHAR * MAX_LINE);
	int i;
	for(i = 0; i < MAX_LINE && fgets((content + i*MAX_CHAR), MAX_CHAR, pFile) != NULL; i++);
	return content;
}
