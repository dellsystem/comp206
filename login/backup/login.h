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

// Other
#ifndef boolean
#define boolean int
#define true 1
#define false 0
#endif

// Function Prototype(s)
boolean verify();
int unencode(char *src, char last, char *dest);
char * getValue( char * parameter, char * src);
