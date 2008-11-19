/*
 * Mount NTFS - Mount an NTFS file system
 * using the NFS file system and an NFS server
 * Copyright (c) 2006 by Martin Rosenau
 *
 * This is free software; you can redistribute it and/or modify it under the
 * terms of the GNU General Public License, see the file COPYING.
 *
 * NTFS file system access
 *
 * File handles:
 * NFS2: File handles are 32 byte values
 * We use the first eight bytes (the first long long) as
 * inode number (index into MFT); the other bytes are unused
 */
#ifdef FSYS_NTFS

#include "ntfs.h"
#include "filesys.h"
#include "shared.h"
#include "pc_slice.h"

#define MAXCLUSTBUF 100
#define MAXINODEBUF 10

#ifdef clientmode
  #define read remote_read
  #define open remote_open
  #define llseek remote_llseek
#endif

extern int cur_fd;

typedef struct _inode {
    long long inode,parent;
    unsigned lastusage;
    int ftype;
    unsigned size;
    time_t mtime,ctime,atime;
    /* Buffer for directory information */
    unsigned short ntree,clusttree,ncuridx;
    unsigned short *treedata;
    char *curidx;
    /* The MFT entry */
    unsigned char mftentry[1];
} tinode,*pinode;

static struct _cluster {
    unsigned lastusage;
    long long cluster;
    unsigned char *data;
} clusters[MAXCLUSTBUF];

static pinode inodes[MAXINODEBUF];

static long long part_offset,mftclust;
static int clustlen,dskhandle,mftentsize,usedosnames,sectlen;
static unsigned disksize;
static pinode mft_inode;
static char cur_handle[256];

static int get_inode(long long inode,pinode *inodep,int nofile);

/* Get the data of a cluster */
static const unsigned char *
get_cluster(long long cluster)
{
    int i,oldest;
    unsigned ksusage;
    static unsigned curusage=1;
    /* Oups. */
    if(cluster<-1ll) return NULL;
    /* Look if the inode is in the cache;
     * if no, look for the oldest cache entry */
    ksusage=clusters[0].lastusage;
    for(i=oldest=0;i<MAXINODEBUF;i++)
    {
        if(clusters[i].cluster==cluster)
        {
            clusters[i].cluster=curusage++;
            return clusters[i].data;
        }
        else if(clusters[i].lastusage<ksusage)
        {
            ksusage=clusters[i].lastusage;
            oldest=i;
        }
    }
    /* A sparse file cluster */
    if(cluster==-1ll)
    {
        memset(clusters[oldest].data,0,clustlen);
        clusters[oldest].lastusage=curusage++;
        clusters[oldest].cluster=-1ll;
        return clusters[oldest].data;
    }
    /* Read the cluster */
    clusters[i].cluster=-2ll;
    llseek(dskhandle,cluster*clustlen+part_offset,SEEK_SET);
    if(read(dskhandle,clusters[oldest].data,clustlen)!=clustlen)
        return NULL;
    clusters[oldest].lastusage=curusage++;
    clusters[oldest].cluster=cluster;
    return clusters[oldest].data;
}

/* Translate a runlength table and a relative cluster number to
 * an absolute cluster number
 * Returns -1 for sparse, <-1 for error */
static long long
rel_to_cluster(const void *runs,long long rel)
{
    long long cluster,len;
    unsigned char nl,ns,sh,issparse,*run;
    run=(unsigned char *)runs;
    cluster=len=0; issparse=0;
    while(rel>=len)
    {
        rel-=len;
        nl=*(run++);
        ns=(nl&0xF0)>>4;
        nl&=0xF;
        if(!nl) return -2ll;
        issparse=!ns;
        for(sh=0,len=0;nl;nl--,sh+=8)
            len+=(*(run++))<<sh;
#ifdef NT4_SPARSE_FILES
        /* In Wind*ws NT sparse files are built differently. */
        if(ns==1 && *run==0xFF)
        {
            run++;
            issparse=1;
        }
        else /* (normal handling) */
#endif
        for(sh=0;ns;ns--,sh+=8)
        {
            if(ns==1) cluster+=(*((signed char *)(run++)))<<sh;
            else cluster+=(*(run++))<<sh;
        }
    }
    if(issparse) return -1ll;
    return cluster+rel;
}

/* Get a little endian word */
static unsigned
getlittle16(const void *data,int off)
{
    const unsigned char *x=(const unsigned char *)data;
    return x[off+1]*0x100+x[off];
}

static unsigned
getlittle32(const void *data,int off)
{
    const unsigned char *x=(const unsigned char *)data;
    return x[off+3]*0x1000000+x[off+2]*0x10000+x[off+1]*0x100+x[off];
}

static long long
getlittle48(const void *data,int off)
{
    const unsigned char *x=(const unsigned char *)data;
    return getlittle32(data,off)+(((long long)getlittle16(data,off+4))<<32);
}

static long long
getlittle64(const void *data,int off)
{
    const unsigned char *x=(const unsigned char *)data;
    return getlittle32(data,off)+(((long long)getlittle32(data,off+4))<<32);
}

/* Find an attribute within an MFT entry
 * The function finds the attribute by type only;
 * the attribute's name is ignored. */
static const unsigned char *
find_attribute(const void *block,int typ)
{
    int p,t,l,maxlen;
    maxlen=getlittle32(block,0x18);
    if(maxlen<0x16) return NULL;
    p=getlittle16(block,0x14);
    while(1)
    {
        if(p+8>maxlen) return NULL;
        t=getlittle32(block,p);
        l=getlittle16(block,p+4);
        if(p+l>maxlen) return NULL;
        if(t==-1) return NULL;
        if(t==typ) return ((const char *)block)+p;
        p+=l;
    }
}

/* Read an attribute or a part of it.
 * Note: In NTFS the entire file contents is an attribute
 * typ is the attribute type; the attribute's name is ignored.
 * The name is used to distinguish between different attributes
 * of the same type; example: Converting a HFS file system to
 * NTFS => All files have a "" and a "resource" attribute of
 * the type 0x80 representing the data and the resource fork.
 * lvl is used for recursive calls and must be 0 otherwise. */
static int
read_attribute(pinode inode,int typ,long long offset,void *dest,
    unsigned len,int lvl)
{
    long long cluster,ll;
    unsigned off,pos,attpos,attllen,couldadddata;
    const unsigned char *attrib,*cldata;
    unsigned char *attlist;
    pinode combinode;
    int i,onlylisted;
    /* Too many recursions */
    if(lvl>10) return -5;
    /* Definition: offset<0 returns 0
     * This is useful for the recursive calls with $ATTRIBUTE_LISTs */
    if(offset<0) return 0;
    /* Find the attribute */
    attrib=find_attribute(inode->mftentry,typ);
    /* It is not in the MFT - maybe it is only stored
     * indirectly in an $ATTRIBUTE_LIST (see splitting
     * inodes below) */
    if(!attrib)
    {
        pos=0;
        onlylisted=1;
    }
    /* The attribute is stored directly */
    else if(!attrib[8])
    {
        onlylisted=0;
        ll=getlittle32(attrib,0x10)-offset;
        if(ll<0) ll=0;
        else if(len<ll) ll=len;
        pos=(unsigned)ll;
        memcpy(dest,attrib+getlittle16(attrib,0x14)+(int)offset,pos);
    }
    /* The attribute is stored anywhere in the file system */
    else
    {
        onlylisted=0;
        /* Get the first cluster */
        cluster=offset/clustlen;
        off=(unsigned)(offset%clustlen);
        attrib+=getlittle16(attrib,0x20);
        ll=rel_to_cluster(attrib,cluster);
        if(ll<-1ll) pos=0;
        else
        {
            cldata=get_cluster(ll);
            if(!cldata) return -5;
            /* Copy all bytes */
            for(pos=0;pos<len;pos++)
            {
                if(off>=clustlen)
                {
                    ll=rel_to_cluster(attrib,++cluster);
                    if(ll<-1ll) break;
                    else
                    {
                        cldata=get_cluster(ll);
                        if(!cldata) return -5;
                        off=0;
                    }
                }
                ((unsigned char *)dest)[pos]=cldata[off++];
            }
        }
    }
    /* NTFS is able to split file entries (inodes)
     * into multiple inodes; an $ATTRIBUTE_LIST is used to do this!
     * Concatenate them here !
     * Return if this is not needed.
     * typ==20: Nested $ATTRIBUTE_LISTs are not supported. */
    if(pos>=len || typ==0x20) return len;
    /* OK. The data needed is found in another inode.
     * Load the attribute list. */
    attrib=find_attribute(inode->mftentry,0x20);
    if(!attrib) return pos;
    attllen=getlittle32(attrib,attrib[8]?0x30:0x10);
    attlist=malloc(attllen);
    if(!attlist) return pos;
    if(read_attribute(inode,0x20,0,attlist,attllen,lvl)!=attllen)
    {
        free(attlist);
        return pos;
    }
    /* Add data from the other inodes */
    do {
        couldadddata=0;
        for(attpos=0;attpos+0x10<=attllen && len>pos;attpos+=i)
        {
            if(getlittle32(attlist,attpos)==typ)
            {
                ll=getlittle64(attlist,attpos+8);
                if(ll || onlylisted)
                    if(offset+pos>=ll*clustlen)
                {
                    i=get_inode(getlittle48(attlist,attpos+16),&combinode,1);
                    if(i)
                    {
                        free(attlist);
                        return -i;
                    }
                    i=read_attribute(combinode,typ,
                        offset+pos-getlittle64(attlist,attpos+8)*clustlen,
                        ((char *)dest)+pos,len-pos,lvl+1);
                    if(i<0)
                    {
                        free(attlist);
                        return -i;
                    }
                    else if(i>0)
                    {
                        pos+=i;
                        couldadddata=1;
                    }
                }
            }
            i=getlittle16(attlist,attpos+4);
            if(!i) break;
        }
    } while(couldadddata && len>pos);
    free(attlist);
    return pos;
}

/* Do the fixup stuff; dest must point to the entire block e.g.
 * a complete MFT entry or a complete Index block */
static int
do_fixups(void *dest,unsigned len)
{
    unsigned pos;
    const unsigned char *cldata,*orgdata;
    /* Get rid of the fixups */
    cldata=orgdata=((unsigned char *)dest)+getlittle16(dest,4);
    for(pos=sectlen;pos<=len;pos+=sectlen)
    {
        cldata+=2;
#ifdef CHECK_FIXUP_SEQUENCES
        if(memcmp(((char *)dest)+pos-2,orgdata,2)) return 5;
#endif
        memcpy(((char *)dest)+pos-2,cldata,2);
    }
    return 0;
}

/* Translate a Wind*ws FILETIME into a time_t */
static time_t
get_time(const void *data)
{
    long long ftime;
    ftime=getlittle64(data,0);
    ftime-=0x19DB1DED53E8000ll;
    return (time_t)(ftime/10000000ll);
}

/* Create an inode from the MFT entry
 * This is called by get_inode() and by ntfs_initialize() to create the
 * inode of the MFT itself.
 * nofile: Allow non-file inodes */
static pinode
create_inode(long long inode,const unsigned char *mftentry,int nofile)
{
    int i,l;
    unsigned fsize;
    const unsigned char *attribs,*datab;
    pinode xinode;
    /* Check the MFT entry and get some data */
    attribs=find_attribute(mftentry,0x30);
    if(!attribs && !nofile) return NULL;
    if(attribs)
    {
        attribs+=0x18+attribs[9]*2;
        if(attribs[0x3B]&0x10)
            fsize=clustlen; /* Dummy: Size of a directory */
        else
        {
            /* Try to get the file size from the size of the data block;
             * If not applicable check the name information block */
            datab=find_attribute(mftentry,0x80);
            if(datab)
            {
                if(datab[8])
                {
                    if(getlittle32(datab,0x34)) fsize=0xFFFFFFFF;
                    else fsize=getlittle32(datab,0x30);
                }
                else fsize=getlittle32(datab,0x10);
            }
            else if(getlittle32(attribs,0x34)) fsize=0xFFFFFFFF;
            else fsize=getlittle32(attribs,0x30);
        }
    }
    /* Build the inode structure */
    l=getlittle16(mftentry,0x18);
    xinode=(pinode)malloc(sizeof(tinode)+l);
    if(!xinode) return NULL;
    xinode->treedata=NULL;
    xinode->curidx=NULL;
    memcpy(xinode->mftentry,mftentry,l);
    xinode->inode=inode;
    if(attribs)
    {
        xinode->parent=getlittle48(attribs,0);
        xinode->size=fsize;
        xinode->ftype=(attribs[0x3B]&0x10)?2:1;
        xinode->mtime=get_time(attribs+16);
        xinode->ctime=get_time(attribs+8);
        xinode->atime=get_time(attribs+32);
    }
    else xinode->ftype=-1;
    return xinode;
}

/* Get an inode's information and store the inode in the cache
 * The inode may become invalid after the next call to this function.
 * Nofile: allow internal inodes */
static int
get_inode(long long inode,pinode *inodep,int nofile)
{
    int i,freeone,oldest;
    unsigned ksusage;
    static unsigned curusage=1;
    static char *mftentry=NULL;
    pinode xinode;
    /* Space for the MFT entry */
    if(!mftentry)
    {
        mftentry=malloc(mftentsize);
        if(!mftentry) return 5;
    }
    /* Look if the inode is in the cache;
     * if no, look for unused cache entries
     * and find the oldest cache entry */
    for(i=oldest=0,freeone=-1,ksusage=0;i<MAXINODEBUF;i++)
    {
        if(!inodes[i]) freeone=i;
        else if(inodes[i]->inode==inode)
        {
            inodes[i]->lastusage=curusage++;
            *inodep=inodes[i];
            if(inodes[i]->ftype<0 && !nofile) return 5;
            return 0;
        }
        else if(inodes[i]->lastusage<ksusage || !ksusage)
        {
            ksusage=inodes[i]->lastusage;
            oldest=i;
        }
    }
    /* Which entry to use ? */
    if(freeone<0) freeone=oldest;
    /* Read the inode's MFT entry */
    i=read_attribute(mft_inode,0x80,inode*mftentsize,mftentry,mftentsize,0);
    if(i<0) return -i;
    if(i!=mftentsize) return 5;
    if(do_fixups(mftentry,mftentsize)) return 5;
    xinode=create_inode(inode,mftentry,nofile);
    if(!xinode) return 5;
    xinode->lastusage=curusage++;
    if(inodes[freeone])
    {
        free(inodes[freeone]->curidx);
        free(inodes[freeone]->treedata);
        free(inodes[freeone]);
    }
    *inodep=inodes[freeone]=xinode;
    return 0;
}

/* Initialize the NTFS access */
int
ntfs_initialize(long long offset, int partmode, int dosnames)
{
    unsigned char sec[512],*mftfirst;
    unsigned u,u2;
    long long ll;
    void *pold;

    /* Check for a partition table */
    part_offset = offset;
    llseek(dskhandle, part_offset, SEEK_SET);
    read(dskhandle, sec, 512);
    if(partmode == 2) partmode = memcmp(&(sec[3]),"NTFS    ",8)?1:0;
    if(partmode)
    {
        part_offset+=getlittle32(sec,0x1C6)*512;
        llseek(dskhandle,part_offset,SEEK_SET);
        read(dskhandle,sec,512);
    }
    /* Is it really NTFS ? */
    if(memcmp(&(sec[3]),"NTFS    ",8))
    {
        fprintf(stderr,"This is not an NTFS disk/image.\n");
        return (1);
    }
    usedosnames=dosnames;
    sectlen=sec[11]+0x100*sec[12];
    clustlen=sec[13]*sectlen;
    ll=getlittle64(sec,0x28);
    mftclust=getlittle64(sec,0x30);
    if(ll>0x7FFFFFFF) disksize=0x7FFFFFFF;
    else disksize=(unsigned)ll;
    /* Now get the data MFT entry for the MFT itself */
    llseek(dskhandle,part_offset+clustlen*mftclust,SEEK_SET);
    mftfirst=malloc(clustlen);
    if(!mftfirst)
    {
        fprintf(stderr,"Memory problem.\n");
        return (1);
    }
    read(dskhandle,mftfirst,clustlen);
    mftentsize=getlittle32(mftfirst,0x1C);
    if(mftentsize>clustlen)
    {
        pold=mftfirst;
        mftfirst=realloc(mftfirst,mftentsize);
        if(!mftfirst)
        {
            free(pold);
            fprintf(stderr,"Memory problem.\n");
            return (1);
        }
        read(dskhandle,mftfirst+clustlen,mftentsize-clustlen);
    }
    if(do_fixups(mftfirst,mftentsize))
    {
        free(mftfirst);
        fprintf(stderr,"Error: MFT seems to be damaged.\n");
        return (1);
    }
    mft_inode=create_inode(0,mftfirst,0);
    if(!mft_inode)
    {
        fprintf(stderr,"Error: Couldn\'t get the MFT inode.\n");
        return (1);
    }
    free(mftfirst);
    /* Initialize the cache */
    for(u=0;u<MAXCLUSTBUF;u++)
    {
        clusters[u].lastusage=0;
        clusters[u].cluster=-2ll;
        clusters[u].data=malloc(clustlen);
        if(!clusters[u].data)
        {
            for(u2=0;u2<u;u2++) free(clusters[u2].data);
            free(mft_inode);
            fprintf(stderr,"Not enough memory.");
            return (1);
        }
    }
    for(u=0;u<MAXINODEBUF;u++) inodes[u]=NULL;
    return 0;
}

/* Get the pointer to the handle of the root directory
 * this must be in a static buffer */
const char *
fs_getroot(void)
{
    static const long long roothandle[]={5,0,0,0};
    return (const char *)&(roothandle[0]);
}

/* The the attributes (fattr structure) of a file
 * Return 0 or an NFS error code */
int
fs_getattr(const char *handle, char *attrs)
{
    pinode inode;
    int i;
    /* Get the inode */
    i=get_inode(*(const long long *)handle,&inode,0);
    if(i) return i;
    /* Fill the output field */
    switch(inode->ftype)
    {
      case 1: /* FILE */
        ((unsigned*)attrs)[0]=htonl(1);
        ((unsigned*)attrs)[1]=htonl(0100555);
        break;
      case 2: /* DIR */
        ((unsigned*)attrs)[0]=htonl(2);
        ((unsigned*)attrs)[1]=htonl(040555);
        break;
      default:
        ((unsigned*)attrs)[0]=0;
        ((unsigned*)attrs)[1]=htonl(0140000);
        break;
    }
    ((unsigned*)attrs)[2]=htonl(1); /* Link count */
    ((unsigned*)attrs)[3]=htonl(getuid());
    ((unsigned*)attrs)[4]=htonl(getgid());
    ((unsigned*)attrs)[5]=htonl(inode->size);
    ((unsigned*)attrs)[6]=htonl(clustlen);
    ((unsigned*)attrs)[7]=htonl((inode->size+clustlen-1)/clustlen);
    ((unsigned*)attrs)[8]=0; /* rdev */
    ((unsigned*)attrs)[9]=0; /* File system ID ? */
    /* File ID - take the lower 32 bits of the inode number
     * It is used in host byte order = network byte order */
    ((unsigned*)attrs)[10]=*(unsigned *)handle;
    ((unsigned*)attrs)[11]=htonl(inode->atime);
    ((unsigned*)attrs)[12]=0; /* after comma part */
    ((unsigned*)attrs)[13]=htonl(inode->mtime);
    ((unsigned*)attrs)[14]=0;
    ((unsigned*)attrs)[15]=htonl(inode->ctime);
    ((unsigned*)attrs)[16]=0;
    return 0;
}

/* Recursively search a directory for subitems
 * Note that a directory is organized as a tree
 * in NTFS. Drawback: The directory must be read
 * once completely before the first record can
 * be read. Advantage: Less complex implementation
 *
 * The function is called recursively and by load_tree_nodes()
 * It is not called from another context. */
static int
find_tree_nodes(pinode inode,const unsigned char *entry,int maxlen)
{
    unsigned char *indexblock;
    const unsigned char *ptr;
    int l,i,fnp,blockat,nmaxlen;
    indexblock=NULL;
    while(1)
    {
        if(maxlen<0x10)
        {
            free(indexblock);
            return 5;
        }
        l=getlittle16(entry,8);
#if 0
        /* The documentation from sourceforge
         * seems to be wrong */
        fnp=10+getlittle16(entry,10);
#else
        /* The file name is always at 0x52 !! */
        fnp=0x52;
#endif
        if((entry[12]&1) && inode->ntree<0xFFF0)
        {
            if(!indexblock)
            {
                indexblock=malloc(inode->clusttree);
                if(!indexblock) return 5;
            }
            if(entry[12]&2) ptr=entry+0x10;
            else ptr=entry+((2*entry[fnp-2]+fnp+7)&~7);
            if(memcmp(ptr+2,"\0\0\0\0",4))
            {
                free(indexblock);
                return 5;
            }
            blockat=getlittle32(ptr,0);
            inode->treedata[inode->ntree++]=(unsigned short)blockat;
            i=read_attribute(inode,0xA0,(long long)blockat*clustlen,
                indexblock,inode->clusttree,0);
            if(i!=inode->clusttree) i=-5;
            if(!i) if(memcmp(indexblock,"INDX",4)) i=-5;
            if(i<0)
            {
                free(indexblock);
                return -i;
            }
            if(do_fixups(indexblock,inode->clusttree)) return 5;
            ptr=indexblock+getlittle32(indexblock,0x18)+0x18;
            nmaxlen=getlittle32(indexblock,0x1C);
            i=find_tree_nodes(inode,ptr,nmaxlen);
            if(i)
            {
                free(indexblock);
                return i;
            }
        }
        if(entry[12]&2)
        {
            free(indexblock);
            return 0;
        }
        entry+=l;
        maxlen-=l;
    }
}

/* Ensure the tree node positions are known
 * This function is called by get_next_direntry() */
static int
load_tree_nodes(pinode inode)
{
    const unsigned char *ptr;
    int i,maxlen;
    /* Is the tree already read ?
     * If not: Find all tree nodes */
    if(inode->treedata) return 0;
    /* Reserve the space */
    inode->ntree=0;
    inode->treedata=malloc(sizeof(unsigned short)*0x10000);
    if(!(inode->treedata)) return 5;
    /* Read the index root */
    ptr=find_attribute(inode->mftentry,0x90);
    /* The index root must be resident (stored directly
     * in the MFT entry); UNIMP: What if the index root is
     * located in an $ATTRIBUTE_LIST ?? Does this happen at all? */
    if(!ptr) return 5;
    if(ptr[8]) return 5;
    ptr+=getlittle16(ptr,0x14);
    inode->clusttree=((signed char *)ptr)[12];
    if(inode->clusttree>0) inode->clusttree*=clustlen;
    else inode->clusttree=1<<(-inode->clusttree);
    maxlen=getlittle32(ptr,20)-getlittle32(ptr,16);
    ptr+=getlittle32(ptr,16)+16;
    i=find_tree_nodes(inode,ptr,maxlen);
    if(i)
    {
        free(inode->treedata);
        inode->treedata=NULL;
        return 5;
    }
    inode->treedata=realloc(inode->treedata,
        sizeof(unsigned short)*(inode->ntree+1));
    return 0;
}

/* Get the next entry;
 * Returns (-1)=EOF, (-2)=Again, 0=OK or an error code
 * *cookie=16 is the first entry
 * A pointer to the entry is written to *entry
 * bothnames!=0: List both long and 8.3 file names */
static int
get_next_direntry(pinode inode,unsigned *cookie,
    const unsigned char **entry,int bothnames)
{
    int offset,i,idx;
    /* Entry is beyond the directorie's end */
    if(((*cookie)>>16)>inode->ntree) return (-1);
    /* Ensure the tree has been read */
    i=load_tree_nodes(inode);
    if(i) return i;
    /* Entry in the index root */
    if(*cookie<0x10000)
    {
        offset=(*cookie)-16;
        *entry=find_attribute(inode->mftentry,0x90);
        (*entry)+=0x18+2*(*entry)[9];
        (*entry)+=getlittle32(*entry,16)+16;
    }
    /* Entry in the index store */
    else
    {
        /* No store for the current index, yet. */
        if(!inode->curidx)
        {
            inode->curidx=malloc(inode->clusttree);
            if(!inode->curidx) return 5;
            inode->ncuridx=(-1);
        }
        /* The currently loaded index is not the required one. */
        idx=(*cookie)>>16;
        if(inode->ncuridx!=idx)
        {
            inode->ncuridx=(-1);
            i=read_attribute(inode,0xA0,
                (long long)(inode->treedata[idx-1])*clustlen,
                inode->curidx,inode->clusttree,0);
            if(i!=inode->clusttree) return 5;
            if(i<0) return -i;
            if(do_fixups(inode->curidx,inode->clusttree)) return 5;
        }
        offset=(*cookie)&0xFFFF;
        *entry=inode->curidx+getlittle32(inode->curidx,0x18)+0x18;
    }
    /* Get the (offset+1)-th entry */
    for(;offset>0;offset--)
    {
        /* End of the current index found */
        if((*entry)[12]&2)
        {
            (*cookie)+=0x10000;
            (*cookie)&=~0xFFFF;
            return (-2);
        }
        /* Go to the next entry */
        (*entry)+=getlittle16(*entry,8);
    }
    /* The end-of-node index does not contain a file. */
    if((*entry)[12]&2)
    {
        (*cookie)+=0x10000;
        (*cookie)&=~0xFFFF;
        return (-2);
    }
    /* The next entry */
    (*cookie)++;
    /* Is it a special entry ? */
    if(!memcmp((*entry)+1,"\0\0\0\0\0",5))
        if(**entry<16 && **entry!=5) return (-2);
    /* Is it an 8.3 file name of a file with long file name
     * or a long file name => check "usedosnames" */
    if(!bothnames)
        if(((*entry)[0x51]==2 && !usedosnames) ||
            ((*entry)[0x51]==1 && usedosnames)) return (-2);
    return 0;
}


/*
 * Look up the file handle of a file named "name" in the
 * directory parent (handle); write the handle to "child"
 * This implementation does not use the B-Tree routines
 * but searches all nodes (unsorted) for the entry.
 * THIS IS VERY SLOW
 */
int
fs_lookup(const char *parent,const char *name,char *child)
{
    unsigned cookie;
    int i,o,c,j;
    const unsigned char *direntry;
    unsigned char ucname[520];
    pinode inode;

    /* Get the inode of the directory */
    i=get_inode(*(const long long *)parent,&inode,0);
    if(i) {
        return i;
    }

    if(inode->ftype!=2) return 20;
    /* Build the file name */
    for(i=o=0;name[i] && o<512;)
    {
        if(name[i]=='%' && !usedosnames)
        {
            c=0; i++;
            if(name[i]=='%')
            {
                i++;
                c=j='%';
            }
            else for(j=c=0;j<4;j++)
            {
                if(name[i]>='0' && name[i]<='9')
                    c=(c<<4)+name[i++]-'0';
                else if(name[i]>='A' && name[i]<='F')
                    c=(c<<4)+name[i++]-'A'+10;
                else if(name[i]>='a' && name[i]<='f')
                    c=(c<<4)+name[i++]-'a'+10;
                else break;
            }
            if(!j) c='%';
            ucname[o++]=c&0xFF;
            ucname[o++]=c>>8;
        }
        else
        {
            ucname[o++]=name[i++];
            ucname[o++]=0;
        }
    }
    /* Name too long => File does not exist */
    if(name[i]) return 2;
    /* Search the directory for the entry */
    cookie=16;
    while(1)
    {
        i=get_next_direntry(inode,&cookie,&direntry,1);
        if(i>0) return i;
        else if(i==(-1)) return 2;
        else if(i==(-2)) continue;
        else if(i<0) return 5; /* Oups */
        else
        {
            /* Do the names match ? */
            if(o==2*direntry[0x50])
            {
                if(compare_unicode(ucname,direntry+0x52,o>>1))
                {
                /* Yes -> Return the handle ! */
                memset(child+8,0,26);
                *(long long *)child=getlittle48(direntry,0);
                return 0;
                }
            }
        }
    }
}

/* Read a directory entry.
 * Return 0=OK, (-1)=EOF, (-2)=Again, Error code
 * (-2 means: the current entry is invalid; e.g. deleted file)
 * handle: Directory handle
 * cookie: Which entry is to be read?
 *    (0..15): Reserved for internal use
 *    16: First entry of the directory
 *    nn: Other entry, value returned by a previous call
 * The cookie of the next entry is returned
 * name: The filename goes here
 * id: The file ID is returned here; it should be equal to the
 *    file ID returned by fs_getattr (in network byte order) */
int
fs_readdir(const char *handle,unsigned *cookie,char *name,unsigned *id)
{
    pinode inode;
    int i,o,l;
    const unsigned char *direntry;
    /* Get the inode of the directory */
    i=get_inode(*(const long long *)handle,&inode,0);
    if(i) return i;
    if(inode->ftype!=2) return 20;
    /* Find the next entry */
    i=get_next_direntry(inode,cookie,&direntry,0);
    if(i) return i;
    /* Translate the file name from Unicode */
    for(i=0x52,o=0,l=2*direntry[0x50]+0x52;i<l;i+=2)
    {
        /* Illegal entry - Unic*de character in a 8.3 file name */
        if(direntry[i+1] && usedosnames) return (-2);
        /* Encode Unic*de characters as %XXXX */
        else if(direntry[i+1] || (direntry[i]<' ' && !usedosnames))
            o+=sprintf(name+o,"%%%04X",(direntry[i+1]<<8)+direntry[i]);
        /* Encode the '%' character as "%%" */
        else if(direntry[i]=='%' && !usedosnames) name[o++]=name[o++]='%';
        /* No encoding needed. */
        else name[o++]=direntry[i];
    }
    name[o]=0;
    /* 2006-08-04: Corrected: "*id" handling was missing up to now
     * as "inodes" are 48 bits long on NTFS but only 32 on NFS2 there
     * may be two files with the same inode !! */
    memcpy(id,direntry,4);
    return 0;
}

/* Get the file system status
 * tsize: Optimum transfer size (bytes; max: 4096)
 * bsize: Cluster size (bytes)
 * blocks: Size of the entire FS (clusters) */
void
fs_statfs(unsigned *tsize,unsigned *bsize,unsigned *blocks)
{
    *tsize=(clustlen>1024)?1024:clustlen;
    *bsize=clustlen;
    *blocks=disksize;
}

/* Get the file ID from the handle - in our case this is simple */
int
fs_getfileid(const char *handle,unsigned *id)
{
    memcpy(id,handle,4);
    return 0;
}

/* Get the parent directory */
int
fs_getparent(const char *child,char *parent,unsigned *id)
{
    pinode inode;
    int i;
    i=get_inode(*(const long long *)child,&inode,0);
    if(i) return i;
    memset(parent,0,32);
    memcpy(parent,&(inode->parent),sizeof(long long));
    memcpy(id,&(inode->parent),4);
    return 0;
}

/* Read data from a file
 * Return the number of bytes read or a negative error code */
int
fs_readdata(const char *handle,unsigned offset,int len,void *dest)
{
    pinode inode;
    int i;
    /* Get the inode of the directory */
    i=get_inode(*(const long long *)handle,&inode,0);
    if(i) return -i;
    if(inode->ftype!=1) return 21;
    /* Read the file data */
    return read_attribute(inode,0x80,offset,dest,len,0);
}

/*
 * Look up one pathname component. The "cur_handle" contains the
 * handle to the component that was looked up earlier. That is
 * the parent in which the given component is looked up.
 * "name" is the name of the entry to be looked up.
 */
static int
lookup_one_entry(const char *name)
{
    char hdl[256];
    int i,l;
    unsigned dummy;

    /* Get the root directory itself ? */
    if(strcmp(name,"/") == 0)
    {
        memcpy(cur_handle, fs_getroot(), 32);
        return (0);
    }

    /* Get "." */
    if(strcmp(name, ".") == 0)
    {
        /* Ignore "." since that handle was already fetched by
         * the previous call to this function.
         */
        return (0);
    }

    /* Get ".." */
    if(strcmp(name, "..") == 0)
    {
        *(unsigned *)hdl = 0;
        if(memcmp(cur_handle, fs_getroot(), 32) != 0)
        {
            i = fs_getparent(cur_handle, hdl, &dummy);
            if (i == 0) {
                memcpy(cur_handle, hdl, 256);
            } else {
                return (i);
            }
        }
        else
        {
            /* "/.." is "/" */
            memcpy(cur_handle, fs_getroot(), 32);
        }
        return (0);
    }

    i = fs_lookup(cur_handle,  name, hdl);
    if(i)
    {
        return (i);
    }
    memcpy(cur_handle, hdl, 256);
    return (0);
}


/*
 * Support functions to allow NTFS access via a GRUB-like API.
 */
int
ntfs_mount(void)
{
  /* Check partition type for harddisk */
  if (((current_drive & 0x80) || (current_slice != 0))
      && (current_slice != PC_SLICE_TYPE_NTFS))
    return 0;

  /* Set our disk fd and fetch the root "/" handle */
  dskhandle = cur_fd;
  (void) memcpy(cur_handle, fs_getroot(), 32);
  if (ntfs_initialize(part_start * SECTOR_SIZE, 2, 0) == 0) {
      return (1);
  }
  return (0);    
}

int
ntfs_read(char *buf, int len)
{
    int i, dlen;
    unsigned tot, flen;
    char attrs[70];

    if(len > 0x2000) return (0);
    i=fs_getattr(cur_handle, attrs);
    if(i == 0)
    {
        flen = ntohl(((unsigned*)attrs)[5]);
        if (filepos + len > flen) {
            len = flen - filepos;
            if (len < 1) {
                return (0);
            }
        }
        dlen=fs_readdata(cur_handle, filepos, len, buf);
        if(dlen<1) {
            return (0);
        } else {
            filepos += dlen;
        }
        return (1);
    }
    return (0);
}

int
ntfs_dir(char *dirname)
{
    int len, i, list = 0;
    char *tok, attrs[70];
    char name[256];
    unsigned cookie = 16, id;

    len = strlen(dirname);
    if (len == 0)
        return (0);

    /* If absolute pathname ensure we are starting with root handle */
    if (dirname[0] == '/') {
        if ((i = lookup_one_entry("/")) != 0) {
            return (0);
        }
    }

    /* Trailing "/" means we want to list dir in GRUB style. */
    if (dirname[len-1] == '/') {
        list = 1;
    }

    /* Lookup all the pathname components, one at a time */
    tok = strtok(dirname, "/");
    while (tok != NULL) {
        if ((i = lookup_one_entry(tok)) != 0) {
            return (0);
        }
        tok = strtok(NULL, "/");
    }

    if (list) {
        i = fs_getattr(cur_handle, attrs);
        if (((unsigned *)attrs)[1] != htonl(040555))
            return (0);
        
        while ((i = fs_readdir(cur_handle, &cookie, name, &id)) != -1) {
            if (i != -2) {
                if (print_possibilities > 0)
                    print_possibilities = -print_possibilities;
                print_a_completion (name);
            }
        }
    }
    return (1);
}

#endif /* FSYS_NTFS */
