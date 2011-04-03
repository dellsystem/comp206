// Headers
#include "login.h"
#include "cipher.h" 
#include "print.h"

// Definitions
#define CHAR_MAX 20
#define USER_MAX 50

#define KEY 1
#define lineDelim 9 
// ascii 9 gives a nice output on excel (values appear on separate lines)

#define csvpath "../database/users.csv"
#define room1path "../room1tmp.html"
#define errorpath "../login_error.html"
//#define DEBUG

// Global Variables
// Input
char user_1[CHAR_MAX];
char pass_1[CHAR_MAX];

// Database
// You may thing using structs is overdoing it since we're just checking for the correct
// username and password. But they can really come in handy while editing, deleting or adding.
// If this was to be a full version login.cgi, structs would be the ideal tools.
struct record {
	char name[CHAR_MAX]; 
	char pass[CHAR_MAX]; 
	char type[CHAR_MAX]; 
} R[USER_MAX];

/*------------------------ GET USER AND PASS INPUT ---------------------*/
// Parses the value of a parameter from an uncoded string file. 
//E.g. getValue("user=", "login?user=bob&pass=abc") returns "bob"
char * getValue( char * parameter, char * src){
	#ifdef DEBUG
		printf("Entered getValue()\n");
	#endif
	
	char * value = (char *) malloc(CHAR_MAX);
	int srclen = strlen(src);
	int parlen = strlen(parameter);
	int i, j;
	i = 0;
	while(strncmp(parameter, src , parlen) != 0 && i < srclen){
		src++;
		i++;
	}

	for(j = 0; i < srclen && *(src + j + parlen) != '&' && *(src + j + parlen) != '\0' ; j++, i++){
		*(value + j) = *(src + j + parlen);
	}
	*(value + j) = '\0';

	#ifdef DEBUG
		printf("getValue() returned %s\n", value);
	#endif

	return value;
}

/*------------------------ UNENCODE ---------------------*/
// Slides code
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
	*dest = '\0';
	#ifdef DEBUG
		printf("Exit unencode()\n");
	#endif
	return 0;
}

/*------------------------ VERIFY ---------------------*/
// Returns true if the username and password match. 
//Returns false if they don't exist or do not match.
boolean verify()
{
	#ifdef DEBUG
		printf("Entered verify(), user and pass to verify = (%s, %s)\n", user_1, pass_1);
	#endif

	boolean v = false;
	int i;
	for(i = 0; (i < USER_MAX) && (v == false); i++){
		#ifdef DEBUG
			printf("Comparing username %s with %s\nComparing password %s with %s\n", user_1, R[i].name, pass_1, R[i].pass);
		#endif
		if((strcmp(user_1, R[i].name) == 0) && (strcmp(pass_1, R[i].pass) == 0))
			v = true;
	}

	#ifdef DEBUG
		printf("Exit verify() with return value %d\n", v);
	#endif

	if (v == true)
		return true;
	else
		return false;
}


/*------------------------ MAIN ---------------------*/

int main (int argc, const char * argv[]) 
{		
	
	#ifdef DEBUG
		printf("Entered main()\n");
	#endif

	// Variable Declaration
	int key = KEY;
	FILE *data;
	char matrix[USER_MAX][CHAR_MAX*3 + 3];
	int i, j; // for loops
	
	// Some initializations
	memset(user_1, 32, CHAR_MAX);
	memset(pass_1, 32, CHAR_MAX);
	
	/*------------------------ RETRIEVE DATA FROM USERS.CSV ---------------------*/
	data = fopen(csvpath, "rt");
	
	#ifdef DEBUG
		printf("Loading csv file..\n");
	#endif

	if(data != NULL){

	#ifdef DEBUG
		printf("The csv file exists\n");
	#endif

		for(i = 0; i < USER_MAX ; i++){
			// Other initializations 
			memset(matrix[i], 32, USER_MAX);
			//memset(duplicate[i], 32, USER_MAX);
			memset(R[i].name, 32, CHAR_MAX);
			memset(R[i].pass, 32, CHAR_MAX);
			memset(R[i].type, 32, CHAR_MAX);
			
			// Scan, store and decrypt 
			if(fgets(matrix[i], CHAR_MAX*3 + 3 , data) != NULL){
				
				#ifdef DEBUG
					printf("\tDecrypt\n");
				#endif
				// Decrypt 
				strcpy(matrix[i], encrypt(-key, matrix[i]));
				
				// Get the position of the last character 
				for(j = 0; j < 50 && *(matrix[i] + j) != '\0'; j++);
				
				// Remove the last character (i.e. lineDelim) 
				if(*(matrix[i] + (j-1)) == lineDelim){
					*(matrix[i] + (j-1)) = '\0';
				}
				
				#ifdef DEBUG
					printf("\tParse\n");
				#endif

				// Parse and store data in an array of record structs 
				strcpy(R[i].name, strtok(strdup(matrix[i]), " ,"));
				strcpy(R[i].pass, strtok(NULL, " ,"));
				strcpy(R[i].type, strtok(NULL, " \0"));

				#ifdef DEBUG 
					printf("\tname:%s\n\tpass:%s\n\ttype:%s\n", R[i].name, R[i].pass, R[i].type);
				#endif
				
			} else {
				break;
			}
		}

	}
	fclose(data);

	#ifdef DEBUG
		printf("Done retrieving data from csv file\n");
	#endif
	
	/*------------------------ RETRIEVE INPUT DATA ---------------------*/
	// parses the input data and stores it into user_1 and pass_1
	// Assuming it's of the form “login?user=bob&pass=abc”
	
	#ifdef DEBUG
		printf("Retrieving cgi input data\n");
	#endif

	int inputSize = 200;
	//char encodedInput[inputSize]; 
	char unencodedInput[inputSize];
	//char c;
	//int n = atoi(getenv("CONTENT_LENGTH"));
	//char encodedInput[n];
	//char unencodedInput[n];
	//int min = (inputSize < n)? inputSize : n; 
	// I don 't know why vybs wanted to limit the input size but here's how I would do it
	//for(i = 0; (c = getchar()) != EOF && i < n; i++){
	//	encodedInput[i] = c;
	//}
	//encodedInput[i] = '\0';
	char * encodedInput = "login?username=RoadRunner&password=BipBip";
	unencode(encodedInput,'\0', unencodedInput);
	strcpy(user_1, getValue("username=", unencodedInput));
	strcpy(pass_1, getValue("password=", unencodedInput));
	
	#ifdef DEBUG
		printf("Done retrieving cgi input data\n");
	#endif

	/* ------------------------ CGI OUTPUT ---------------------*/
	
	#ifdef DEBUG
		printf("Start cgi output\n");
	#endif

	if(verify()){
		   print(room1path);
	} else {
		   print(errorpath);
	}

	#ifdef DEBUG
		printf("Done cgi ouput\n");
	#endif

	return EXIT_SUCCESS;
}
