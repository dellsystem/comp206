all: login backup
backup: login.c print.c cipher.c
	cp *.[ch] backup
login: login.o print.o cipher.o
	gcc -Wall -o login.cgi cipher.o print.o login.o
	cp login.cgi ..
login.o: login.c login.h
	gcc -Wall -c login.c
cipher.o: cipher.c cipher.h
	gcc -Wall -c cipher.c
print.o: print.c print.h
	gcc -Wall -c print.c
	cp *.[ch] backup
