# Copyright (c) 2006 by Martin Rosenau

objs = pscan.o \
	fsys_ext2fs.o \
	fsys_reiserfs.o  \
	fsys_xfs.o  \
	fsys_fat.o  \
	fsys_jfs.o  \
	fsys_ntfs.o  \
	namecomp.o  \
	fsys_minix.o \
	fsys_ufs.o \
	fsys_ufs2.o \
	fsys_ffs.o

CFLAGS = -D_FILE_OFFSET_BITS=64 -std=c99 -D__EXTENSIONS__ \
	-DFSYS_EXT2FS \
	-DFSYS_REISERFS \
	-DFSYS_XFS \
	-DFSYS_FAT \
	-DFSYS_JFS \
	-DFSYS_NTFS \
	-DFSYS_MINIX \
	-DFSYS_UFS \
	-DFSYS_UFS2 \
	-DFSYS_FFS \
	-DGRUB_UTIL

INC = 

# Uncomment this for debugging information in the files
DEBUG = -g

all: pscan

pscan: $(objs)
	@echo Linking
	@gcc $(DEBUG) $(CFLAGS) $(objs) -o pscan

.c.o:
	@echo Compiling $<
	@gcc -c $< $(DEBUG) $(INC) $(CFLAGS)

clean:
	@rm -f *.o
	@rm -f pscan

install:
	@mkdir -p $(DESTDIR)/usr/bin
	@cp pscan $(DESTDIR)/usr/bin
	@chmod 0755 $(DESTDIR)/usr/bin/pscan
