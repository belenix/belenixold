# Copyright (c) 2006 by Martin Rosenau

objs = main.o nfs.o ntfs.o namecomp.o
libs = -R/usr/foss/lib -lsocket

# Uncomment this for debugging information in the files
#DEBUG = -ggdb

# Uncomment these for remote-server test (client.c / server.c)
# objs += client.o
# DEBUG += -Dclientmode

mount_ntfs: $(objs)
	@echo Linking
	@gcc -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 $(objs) $(libs) -o mount_ntfs $(DEBUG)

.c.o:
	@echo Compiling $<
	@gcc -c $< $(DEBUG)

clean:
	@rm -f *.o
	@rm -f mount_ntfs

install:
	@mkdir -p $(DESTDIR)/usr/lib/fs/ntfs
	@cp mount_ntfs $(DESTDIR)/usr/lib/fs/ntfs/mount

