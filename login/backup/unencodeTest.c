#include <stdlib.h>
#include <stdio.h>
int unencode(char * src, char last, char *dest)
{
	#ifdef DEBUG
		printf("Entered unencode()\n");
	#endif
	for(; *src != last; src++, dest++){
		if(*src == '+'){
			*dest = ' ';
		}else if(*src == '%') {
			int code;
			if(sscanf(src+1, "%2x", &code) != 1) code = '?';
			*dest = code;
			src += 2;
			/*int code;
			if(sscanf(src+1, "%2x", &code) == 0){
				*dest = code;
				src+=2;
			} else if(sscanf(src+1, "%3x", &code) == 1){ 
		   // added this part because ascii values can have 3 digits
				*dest = code;
				src+=3;
			} else {
				code ='?';
			}*/
		} else {
			*dest = *src;
	//#ifdef DEBUG
	//	printf("Copied character %c\n", *dest);
	//#endif
		}
	}
	*dest = '\n';
	*++dest = '\0';
	#ifdef DEBUG
		printf("Exit unencode()\n");
	#endif
	return 0;
}

int main(void){
	char * unencoded = (char *) malloc (100);
	unencode("login?user=bob+smith&pass=abc", '\0', unencoded);
	printf("%s", unencoded);
	return 0;
}

