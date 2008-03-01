# Copyright (c) 2006 by Martin Rosenau

objs = prtpart.o
CFLAGS = -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -std=c99 -D__EXTENSIONS__
INC = 

# Uncomment this for debugging information in the files
DEBUG = -g

all: prtpart.bin prtpart

prtpart.bin: $(objs)
	@echo Linking
	@gcc $(DEBUG) $(CFLAGS) $(objs) -o prtpart.bin

prtpart:
	@cp prtpart.sh prtpart
	@chmod 0755 prtpart

.c.o:
	@echo Compiling $<
	@gcc -c $< $(DEBUG) $(INC) $(CFLAGS)

clean:
	@rm -f *.o
	@rm -f prtpart.bin
	@rm -f prtpart

install:
	@mkdir -p $(DESTDIR)/usr/bin
	@cp prtpart.bin $(DESTDIR)/usr/bin
	@cp prtpart $(DESTDIR)/usr/bin
	@chmod 0755 $(DESTDIR)/usr/bin/prtpart
	@chmod 0755 $(DESTDIR)/usr/bin/prtpart.bin
