/*
 * Mount EXT2FS - Mount an EXT2FS file system
 * using the NFS file system and an NFS server
 * Copyright (c) 2006 by Martin Rosenau
 * Adapted from ntfs.c by Moinak Ghosh
 *
 * This is free software; you can redistribute it and/or modify it under the
 * terms of the GNU General Public License, see the file COPYING.
 *
 * EXT2FS file system access
 *
 * File handles:
 * NFS2: File handles are 32 byte values
 * We use the first 4 bytes (the first unsigned long) as
 * inode number. The other bytes are unused;
 */
#include <limits.h>
#include "mount_ext2fs.h"

struct ext2_file {
        errcode_t               magic;
        ext2_filsys             fs;
        ext2_ino_t              ino;
        struct ext2_inode       inode;
        int                     flags;
        __u64                   pos;
        blk_t                   blockno;
        blk_t                   physblock;
        char                    *buf;
};

static ext2_filsys mnt_fs;
static char newname[PATH_MAX+25];

/* Open the EXT2FS filesystem */
int ext2_initialize(const char *image, unsigned long long offset,int partmode, int echo)
{
    errcode_t rv;
    int flags;

    if (offset > 0) {
        snprintf(newname, PATH_MAX+25, "%s?offset=%llu", image, offset);

    } else {
        strlcpy(newname, image, PATH_MAX);
    }

    flags = EXT2_FLAG_JOURNAL_DEV_OK;
    if (partmode == 0)
        flags |= EXT2_FLAG_IMAGE_FILE;

    rv = ext2fs_open(newname, flags, 0, 0, unix_io_manager, &mnt_fs);

    if (rv) {
        if (echo)
		com_err("mount_ext2fs", rv, "while trying to open %s",
                	image);
        return (NFSERR_PERM);
    }

    return (NFS_OK);
}

/* Get the pointer to the handle of the root directory
 * this must be in a static buffer */
const char *fs_getroot(void)
{
    static const uint32_t roothandle[]={EXT2_ROOT_INO, 0, 0, 0, 0, 0, 0, 0};
    return (const char *)&(roothandle[0]);
}

/* The the attributes (fattr structure) of a file
 * Return 0 or an NFS error code */
int fs_getattr(const char *handle,char *attrs)
{
    struct ext2_inode inode;
    errcode_t rv;
    /* Get the inode. Inode caching is done by the ext2 library */
    rv = ext2fs_read_inode(mnt_fs, *(ext2_ino_t *)handle, &inode);
    if(rv) {
        com_err("mount_ext2fs", rv, "while trying to read inode %u",
                *(uint32_t *)handle);
        if (rv == EXT2_ET_BAD_INODE_NUM)
            return (NFSERR_STALE);
        else if (rv == EXT2_ET_NO_MEMORY)
            return (NFSERR_NXIO);
        else
            return (NFSERR_IO);
    }

    /* Fill the output field */
    switch((inode.i_mode) & LINUX_S_IFMT)
    {
      case LINUX_S_IFREG: /* FILE */
        ((unsigned*)attrs)[0]=htonl(NFREG);
        break;
      case LINUX_S_IFDIR: /* DIR */
        ((unsigned*)attrs)[0]=htonl(NFDIR);
        break;
      case LINUX_S_IFLNK: /* LINK */
        ((unsigned*)attrs)[0]=htonl(NFLNK);
        break;
      case LINUX_S_IFCHR: /* CHR */
        ((unsigned*)attrs)[0]=htonl(NFCHR);
        break;
      case LINUX_S_IFBLK: /* BLK */
        ((unsigned*)attrs)[0]=htonl(NFBLK);
        break;
      default:
        ((unsigned*)attrs)[0]=htonl(NFNON);
        break;
    }
    ((unsigned*)attrs)[1]=htonl(inode.i_mode);
    ((unsigned*)attrs)[2]=htonl(inode.i_links_count); /* Link count */
    ((unsigned*)attrs)[3]=htonl(inode.i_uid);
    ((unsigned*)attrs)[4]=htonl(inode.i_gid);
    ((unsigned*)attrs)[5]=htonl(EXT2_I_SIZE(&inode));
    ((unsigned*)attrs)[6]=htonl(mnt_fs->blocksize);
    ((unsigned*)attrs)[7]=0; /* rdev */
    ((unsigned*)attrs)[8]=htonl(inode.i_blocks);
    ((unsigned*)attrs)[9]=0; /* File system ID ? */
    /* File ID - take the 32 bits of the inode number
     * It is used in host byte order = network byte order */
    ((unsigned*)attrs)[10]=*(unsigned *)handle;
    ((unsigned*)attrs)[11]=htonl(inode.i_atime);
    ((unsigned*)attrs)[12]=0; /* after comma part */
    ((unsigned*)attrs)[13]=htonl(inode.i_mtime);
    ((unsigned*)attrs)[14]=0;
    ((unsigned*)attrs)[15]=htonl(inode.i_ctime);
    ((unsigned*)attrs)[16]=0;
    return (NFS_OK);
}

/* Look up a the file handle of a file named "name" in the
 * directory parent (handle); write the handle to "child"
 */
int fs_lookup(const char *parent,const char *name,char *child)
{
    ext2_ino_t inum;
    errcode_t rv;

    rv = ext2fs_lookup(mnt_fs, *(ext2_ino_t *)parent, name,
		strlen(name), NULL, &inum);

    if (rv == EXT2_ET_FILE_NOT_FOUND)
        return (NFSERR_NOENT);

    memset(child, 0, NFS_FHSIZE);
    *(uint32_t *)child = inum;
    return (NFS_OK);
}

int
readdir_callback(struct ext2_dir_entry *dent, unsigned int offset, int blocksize,
                 char *buf, void *priv)
{
    struct _readdir_priv_ *rdpriv  = (struct _readdir_priv_ *)priv;

    if (rdpriv->cnum == rdpriv->rnum) {
        strncpy(rdpriv->name, dent->name, dent->name_len & 0xFF);
        rdpriv->name[dent->name_len & 0xFF] = '\0';
        *(rdpriv->fid) = dent->inode;
	rdpriv->end = 0;
        return (DIRENT_ABORT);
    }
    rdpriv->cnum++;
    return (0);
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
int fs_readdir(const char *handle, unsigned *cookie, char *name, unsigned *id)
{
    struct ext2_inode inode;
    errcode_t rv;
    char *buf;
    struct _readdir_priv_ rdpriv;

    rv = ext2fs_read_inode(mnt_fs, *(ext2_ino_t *)handle, &inode);
    if(rv) {
        com_err("mount_ext2fs", rv,  "while trying to read inode %u",
                *(uint32_t *)handle);
        if (rv == EXT2_ET_BAD_INODE_NUM)
            return (NFSERR_STALE);
        else
            return (NFSERR_IO);
    }

    if (!LINUX_S_ISDIR(inode.i_mode))
        return (NFSERR_NOTDIR);

    buf = (char *)malloc(mnt_fs->blocksize * 2);
    if (!buf)
        return (NFSERR_IO);

    rdpriv.name = name;
    rdpriv.rnum = *cookie;
    rdpriv.cnum = 0;
    rdpriv.fid = id;
    rdpriv.end = 1;
    rv = ext2fs_dir_iterate(mnt_fs, *(ext2_ino_t *)handle, 0, buf,
                     readdir_callback, &rdpriv);
    free(buf);
    if (rv) {
        com_err("mount_ext2fs", rv, "while trying trying to iterate %u",
                *(uint32_t *)handle);
        return (NFSERR_IO);
    }

    if (rdpriv.end)
        return (-2);

    (*cookie)++;
    return (NFS_OK);
}

/* Get the file system status
 * tsize: Optimum transfer size (bytes; max: 4096)
 * bsize: Cluster size (bytes)
 * blocks: Size of the entire FS (clusters) */
void fs_statfs(unsigned *tsize,unsigned *bsize,unsigned *blocks, unsigned *fbfree, unsigned *fbavail)
{
    *tsize = NFS_MAXDATA;
    *bsize = mnt_fs->blocksize;
    *blocks = mnt_fs->super->s_blocks_count;
    *fbfree = mnt_fs->super->s_free_blocks_count;
    *fbavail = mnt_fs->super->s_free_blocks_count - mnt_fs->super->s_r_blocks_count;
}

/* Get the file ID from the handle - in our case this is simple */
int fs_getfileid(const char *handle,unsigned *id)
{
    memcpy(id,handle,4);
    return 0;
}

/* Read data from a file
 * Return the number of bytes read or a negative error code */
unsigned long
fs_readdata(const char *handle,unsigned long offset,unsigned long len,void *dest)
{
    struct ext2_inode inode;
    errcode_t rv;
    struct ext2_file *fl;
    uint32_t sread;

    rv = ext2fs_read_inode(mnt_fs, *(ext2_ino_t *)handle, &inode);
    if(rv) {
        com_err("mount_ext2fs", rv, "while trying to read inode %u",
                *(uint32_t *)handle);
        if (rv == EXT2_ET_BAD_INODE_NUM)
            return (NFSERR_STALE);
        else
            return (NFSERR_IO);
    }

    if (LINUX_S_ISDIR(inode.i_mode))
        return (NFSERR_ISDIR);

    rv = ext2fs_file_open(mnt_fs, *(ext2_ino_t *)handle, 0, &fl);
    if (rv) {
        com_err("mount_ext2fs", rv, "while trying to open inode %u",
                *(uint32_t *)handle);
        return (NFSERR_IO);
    }

    if (offset > EXT2_I_SIZE(&inode)) {
        ext2fs_file_close(fl);
        return (NFSERR_IO);
    }
    fl->pos = offset;

    rv = ext2fs_file_read(fl, dest, len, &sread);
    ext2fs_file_close(fl);

    if (rv) {
        com_err("mount_ext2fs", rv, "while trying to read inode %u data",
                *(uint32_t *)handle);
        return (NFSERR_IO);
    }

    return (sread);
}

