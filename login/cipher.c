char * encrypt(int key, char * s)
{
	int i;
	for(i = 0; *(s + i) != '\0'; i++){
		*(s + i) = (*(s + i) + key) % 256;
	}
	return s;
}


