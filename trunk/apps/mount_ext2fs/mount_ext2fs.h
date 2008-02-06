/*
 * Mount NTFS - Mount an NTFS file system
 * using the NFS file system and an NFS server
 * Copyright (c) 2006 by Martin Rosenau
 *
 * Main include file
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <et/com_err.h>
#include <ext2fs/ext2fs.h>

/* Functions of nfs.c */
void handle_nfs_packet(int sock,struct sockaddr_in *soa,const char *buffer,int len);

static long NFNON = 0;
static long NFREG = 1;
static long NFDIR = 2;
static long NFBLK = 3;
static long NFCHR = 4;
static long NFLNK = 5;

enum stat {
    NFS_OK = 0,
    NFSERR_PERM=1,
    NFSERR_NOENT=2,
    NFSERR_IO=5,
    NFSERR_NXIO=6,
    NFSERR_ACCES=13,
    NFSERR_EXIST=17,
    NFSERR_NODEV=19,
    NFSERR_NOTDIR=20,
    NFSERR_ISDIR=21,
    NFSERR_FBIG=27,
    NFSERR_NOSPC=28,
    NFSERR_ROFS=30,
    NFSERR_NAMETOOLONG=63,
    NFSERR_NOTEMPTY=66,
    NFSERR_DQUOT=69,
    NFSERR_STALE=70,
};

/* The size in bytes of the opaque file handle. */
static int NFS_FHSIZE = 32;

/*
 * The size in bytes of the opaque "cookie" passed by
 * READDIR.
 */
static int NFS_COOKIESIZE = 4;

/* The maximum number of bytes in a filename argument. */
static int NFS_MAXNAMLEN = 255;

/* The maximum number of bytes in a pathname argument. */
static int NFS_MAXPATHLEN = 1024;

/*
 * The maximum number of bytes of data in a READ or
 * WRITE request.
 */
static int NFS_MAXDATA = 8192;

struct _readdir_priv_ {
	uint32_t *fid;
        int rnum, cnum;
	int end;
	char *name;
};

/* Functions of ext2fs.c */
int ext2_initialize(const char *image, unsigned long long offset, int partmode, int echo);
const char *fs_getroot(void);
int fs_getattr(const char *handle,char *attrs);
int fs_lookup(const char *parent,const char *name,char *child);
void fs_statfs(unsigned *tsize,unsigned *bsize,unsigned *blocks, unsigned *fbfree, unsigned *fbavail);
int fs_readdir(const char *handle,unsigned *cookie,char *name,unsigned *id);
int fs_getfileid(const char *handle,unsigned *id);
unsigned long fs_readdata(const char *handle,unsigned long offset,unsigned long len,void *dest);

/* Functions of namecomp.c */
int compare_unicode(const char *text1,const char *text2,int len);
