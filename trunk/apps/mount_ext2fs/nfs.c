/*
 * Mount EXT2FS - Mount an EXT2FS file system
 * using the NFS file system and an NFS server
 * Copyright (c) 2006 by Martin Rosenau
 *
 * This is free software; you can redistribute it and/or modify it under the
 * terms of the GNU General Public License, see the file COPYING.
 *
 * NFS server implementation
 */
#include "mount_ext2fs.h"

/* Get a big endian word */
static unsigned long getbig(const void *data,int off)
{
    const unsigned char *x=(const unsigned char *)data;
    return x[off]*0x1000000+x[1+off]*0x10000+x[2+off]*0x100+x[3+off];
}

#if 1
/* Debugging: dump data */
void dump(FILE *f,const void *data,int size)
{
    int i,j;
    for(i=0;i<size;i+=16)
    {
        for(j=i;j<i+16 && j<size;j++)
            fprintf(f," %02X",((const unsigned char *)data)[j]);
        fputc('\n',f);
    }
}
#endif

/* "No access"-Error */
static int nfs_no_access(const char *input,int len,char *output)
{
    memcpy(output,"\0\0\0\xD",4);
    return 4;
}

/* Handler for the NULL function */
static int nfs_null(const char *input,int len,char *output)
{
    return 0;
}

/* Handler for the getattr procedure */
static int nfs_getattr(const char *input,int len,char *output)
{
    int i;
    /* Check if the parent is the "public" handle
     * => Use root directory as parent */
    for(i=0;i<32 && !input[i];i++);
    i=fs_getattr((i==32)?fs_getroot():input,output+4);
    if(i)
    {
        *(unsigned *)output=htonl(i);
        return 4;
    }
    *(unsigned *)output=0;
    return 0x48;
}

/* Handler for the lookup procedure */
static int nfs_lookup(const char *input,int len,char *output)
{
    char name[256];
    int i,l;
    unsigned dummy;
    /* Get the file name to look up */
    l=input[35]&0xFF;
    if(input[36]=='\x80' && l>0)
    { i=37; l--; }
    else i=36;
    memcpy(name,input+i,l);
    name[l]=0;
    /* Get the root directory itself ? */
    if(!strcmp(name,"/"))
    {
        *(unsigned *)output=0;
        memcpy(output+4,fs_getroot(),32);
        i=fs_getattr(output+4,output+36);
        if(i)
        {
            *(unsigned *)output=htonl(i);
            return 4;
        }
        return 0x68;
    }
    /* Get "." */
    if(!strcmp(name,"."))
    {
        *(unsigned *)output=0;
        memcpy(output+4,input,32);
        i=fs_getattr(output+4,output+36);
        if(i)
        {
            *(unsigned *)output=htonl(i);
            return 4;
        }
        return 0x68;
    }
    /* Check if the parent is the "public" handle
     * => Use root directory as parent */
    for(i=0;i<32 && !input[i];i++);
    i=fs_lookup((i==32)?fs_getroot():input,name,output+4);
    if(i)
    {
        *(unsigned *)output=htonl(i);
        return 4;
    }
    i=fs_getattr(output+4,output+36);
    if(i)
    {
        *(unsigned *)output=htonl(i);
        return 4;
    }
    *(unsigned *)output=0;
    return 0x68;
}

/* Handler for the readlink procedure
 * We do not support that yet. */
static int nfs_readlink(const char *input,int len,char *output)
{
    memcpy(output,"\0\0\0\5",4); /* 5 = EIO */
    return 4;
}

/* Handler for the read procedure */
static int nfs_read(const char *input,int len,char *output)
{
    int i;
    unsigned long dlen;
    unsigned long offset;
    offset=getbig(input,32);
    dlen=getbig(input,36);
    if(dlen>NFS_MAXDATA) return -1;
    i=fs_getattr(input,output+4);
    if(!i)
    {
        dlen=fs_readdata(input,offset,dlen,output+0x4C);
        if(dlen<0) i=-dlen;
    }
    if(i)
    {
        *(unsigned *)output=htonl(i);
        return 4;
    }
    *(unsigned *)output=0;
    *(unsigned *)(output+0x48)=htonl(dlen);
    return (0x4F+dlen)&~3;
}

/* Handler for the readdir procedure */
static int nfs_readdir(const char *input,int len,char *output)
{
    int i;
    unsigned cookie;
    char dummy[32];
    memcpy(&cookie,input+32,4);
    /* Get the next valid entry */
    i=fs_readdir(input,&cookie,output+16,(unsigned *)(output+8));
    if(i>0)
    {
        *(unsigned *)output=htonl(i);
        return 4;
    }
    *(unsigned *)output=0;
    if(i == -2)
    {
        /* EOF */
        memcpy(output+4,"\0\0\0\0\0\0\0\1",8);
        return 12;
    }
    /* Not EOF */
    memcpy(output+4,"\0\0\0\1",4);
    i=strlen(output+16);
    *(unsigned *)(output+12)=htonl(i);
    i=(i+3)&~3;
    memcpy(output+i+16,&cookie,4);
    memcpy(output+i+20,"\0\0\0\0\0\0\0\0",8);
    return i+28;
}

/* Handler for the statfs procedure */
static int nfs_statfs(const char *input,int len,char *output)
{
    unsigned tsize, bsize, blocks, fbfree, fbavail, data[5];
    memcpy(output,"\0\0\0\0",4);
    memcpy(output+16,"\0\0\0\0\0\0\0\0",8);
    fs_statfs(&tsize, &bsize, &blocks, &fbfree, &fbavail);
    while(tsize>4096) tsize>>=1;
    data[0]=htonl(tsize);
    data[1]=htonl(bsize);
    data[2]=htonl(blocks);
    data[3]=htonl(fbfree);
    data[4]=htonl(fbavail);
    memcpy(output+4,data,20);
    return 24;
}

/* Function_ID - Handler pairs
 * Handler arguments:
 * indata - data after the header (data follwing the "verf" member in RPC)
 * inlen - data length
 * outdata - buffer for output data (following the "accept_stat" member)
 * Returns: >=0 = size of data, SUCCESS; (-1) = Error, GARBAGE_ARGS */
static const struct _t_procs {
    int id;
    int (*handler)(const char *indata,int inlen,char *outdata);
} procs[]= {
    {0,nfs_null},
    {1,nfs_getattr},
    {2,nfs_no_access}, /* setattr */
    /* 3 = root, unimplemented */
    {4,nfs_lookup},
    {5,nfs_readlink},
    {6,nfs_read},
    {7,nfs_no_access}, /* writecache */
    {8,nfs_no_access}, /* write */
    {9,nfs_no_access}, /* create */
    {10,nfs_no_access}, /* remove */
    {11,nfs_no_access}, /* rename */
    {12,nfs_no_access}, /* link */
    {13,nfs_no_access}, /* symlink */
    {14,nfs_no_access}, /* mkdir */
    {15,nfs_no_access}, /* rmdir */
    {16,nfs_readdir}, /* readdir */
    {17,nfs_statfs}, /* statfs */
    /* End marker */
    {0,NULL}
};

/* Process a single incoming UDP data packet
 * sock:   handle of socket
 * soa:    source address
 * buffer: data of the UDP packet
 * len:    size of the UDP packet */
void handle_nfs_packet(int sock,struct sockaddr_in *soa,const char *buffer,int len)
{
    union {
        int for_propper_alignment;
        char buf[9000];
    } buf;
    int q,p,i,j;
    /* This is a response! Why do we get this? */
    if(memcmp(buffer+4,"\0\0\0\0",4)) return;
    /* This is needed in every case */
    memcpy(buf.buf,buffer,4);
    /* Wrong RPC version */
    if(memcmp(buffer+8,"\0\0\0\2",4))
    {
        memcpy(&(buf.buf[4]),"\0\0\0\1\0\0\0\1\0\0\0\0\0\0\0\2\0\0\0\2",20);
        sendto(sock,buf.buf,24,0,(struct sockaddr *)soa,sizeof(struct sockaddr_in));
        return;
    }
    /* Build the common part of the response header */
    memcpy(&(buf.buf[4]),"\0\0\0\1\0\0\0\0",8);
    q=(getbig(buffer,28)+35)&~3;
    p=(getbig(buffer,q+4)+11)&~3;
    memcpy(&(buf.buf[12]),buffer+q,p);
    q+=p; p+=12;
    /* Not NFS */
    if(memcmp(buffer+12,"\0\1\x86\xA3",4))
    {
        memcpy(&(buf.buf[p]),"\0\0\0\1",4);
        sendto(sock,buf.buf,p+4,0,(struct sockaddr *)soa,sizeof(struct sockaddr_in));
        return;
    }
    /* Not NFS v. 2 */
    if(memcmp(buffer+16,"\0\0\0\2",4))
    {
        memcpy(&(buf.buf[p]),"\0\0\0\2\0\0\0\2\0\0\0\2",12);
        sendto(sock,buf.buf,p+12,0,(struct sockaddr *)soa,sizeof(struct sockaddr_in));
        return;
    }
    /* Look for the procedure */
    j=getbig(buffer,20);
    for(i=0;procs[i].handler;i++) if(procs[i].id==j)
    {
        i=procs[i].handler(buffer+q,len-q,&(buf.buf[p+4]));
        /* Garbage args */
        if(i<0)
        {
            memcpy(&(buf.buf[p]),"\0\0\0\4",4);
            i=0;
        }
        /* Args OK */
        else memcpy(&(buf.buf[p]),"\0\0\0\0",4);
        sendto(sock,buf.buf,p+i+4,0,(struct sockaddr *)soa,sizeof(struct sockaddr_in));
        return;
    }
    /* Unknown function */
    memcpy(&(buf.buf[p]),"\0\0\0\3",4);
    sendto(sock,buf.buf,p+4,0,(struct sockaddr *)soa,sizeof(struct sockaddr_in));
}


