# Copyright (c) 2006 by Martin Rosenau

objs = main.o nfs.o ext2.o
uobjs = xumount.o
lobjs = xlsmounts.c
libs = -R/usr/lib/ext2fs -L/usr/lib/ext2fs -lgen -lsocket -lext2fs -lcom_err
INC = -I/usr/include/ext2fs

# Uncomment this for debugging information in the files
DEBUG = -g

all: mount_ext2fs xumount xlsmounts

xumount: $(uobjs)
	@echo Linking xumount
	@gcc $(DEBUG) $(uobjs) -o xumount

xlsmounts: $(lobjs)
	@echo Linking xlsmounts
	@gcc $(DEBUG) $(lobjs) -o xlsmounts

mount_ext2fs: $(objs)
	@echo Linking
	@gcc $(DEBUG) -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 $(objs) $(libs) -o mount_ext2fs

.c.o:
	@echo Compiling $<
	@gcc -c $< $(DEBUG) $(INC)

clean:
	@rm -f *.o
	@rm -f mount_ext2fs
	@rm -f xlsmounts
	@rm -f xumount

install:
	@mkdir -p $(DESTDIR)/usr/bin
	@mkdir -p $(DESTDIR)/usr/lib/fs/ext2fs
	@cp xumount $(DESTDIR)/usr/bin
	@cp xlsmounts $(DESTDIR)/usr/bin
	@cp mount_ext2fs $(DESTDIR)/usr/lib/fs/ext2fs/mount
	@ln -sf mount $(DESTDIR)/usr/lib/fs/ext2fs/fstyp
	@chmod 0755 $(DESTDIR)/usr/bin/xumount
	@chmod 0755 $(DESTDIR)/usr/bin/xlsmounts
	@chmod 0755 $(DESTDIR)/usr/lib/fs/ext2fs/*
