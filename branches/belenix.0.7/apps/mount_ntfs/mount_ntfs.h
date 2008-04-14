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

/* Functions of nfs.c */
void handle_nfs_packet(int sock,struct sockaddr_in *soa,const char *buffer,int len);

/* Functions of ntfs.c */
int ntfs_initialize(const char *image,long long offset,int partmode,int dosnames);
const char *fs_getroot(void);
int fs_getattr(const char *handle,char *attrs);
int fs_lookup(const char *parent,const char *name,char *child);
void fs_statfs(unsigned *tsize,unsigned *bsize,unsigned *blocks);
int fs_readdir(const char *handle,unsigned *cookie,char *name,unsigned *id);
int fs_getfileid(const char *handle,unsigned *id);
int fs_getparent(const char *child,char *parent,unsigned *id);
int fs_readdata(const char *handle,unsigned offset,int len,void *dest);

/* Functions of namecomp.c */
int compare_unicode(const char *text1,const char *text2,int len);
