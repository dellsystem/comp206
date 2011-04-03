// Guards
#ifndef STDIO_GUARD
#define STDIO_GUARD
#include <stdio.h>
#endif

#ifndef STDLIB_GUARD
#define STDLIB_GUARD
#include <stdlib.h>
#endif

#ifndef STRING_GUARD
#define STRING_GUARD
#include <string.h>
#endif

// Prototype(s) 
int print(char * filePath);
char * filter(char * src, int minASCII, int maxASCII);
