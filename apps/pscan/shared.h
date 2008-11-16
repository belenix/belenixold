/* shared.h - definitions used in all GRUB-specific code */
/*
 *  GRUB  --  GRand Unified Bootloader
 *  Copyright (C) 1999,2000,2001,2002,2003,2004  Free Software Foundation, Inc.
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */
/*
 * Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
 * Use is subject to license terms.
 */

/*
 *  Generic defines to use anywhere
 */

#ifndef GRUB_SHARED_HEADER
#define GRUB_SHARED_HEADER	1

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/* Add an underscore to a C symbol in assembler code if needed. */
#ifdef HAVE_ASM_USCORE
# define EXT_C(sym) _ ## sym
#else
# define EXT_C(sym) sym
#endif

/* ZFS will use the top 4 Meg of physical memory (below 4Gig) for sratch */
#define ZFS_SCRATCH_SIZE 0x400000

#define	MAXNAMELEN	256
#define MIN(x, y) ((x) < (y) ? (x) : (y))

/* Boot signature related defines for the findroot command */
#define	BOOTSIGN_DIR	"/boot/grub/bootsign"
#define	BOOTSIGN_ARGLEN	(MAXNAMELEN + 10)	/* (<sign>,0,d) */
#define	BOOTSIGN_LEN	(sizeof (BOOTSIGN_DIR) + 1 + BOOTSIGN_ARGLEN)
#define	BOOTSIGN_BACKUP	"/etc/bootsign"

/*
 *  Integer sizes
 */

#define MAXINT     0x7FFFFFFF

/* Maximum command line size. Before you blindly increase this value,
   see the comment in char_io.c (get_cmdline).  */
#define MAX_CMDLINE 1600
#define NEW_HEAPSIZE 1500
#define UNIQUE_BUFLEN MAX_CMDLINE

/*
 *  This is the filesystem (not raw device) buffer.
 *  It is 32K in size, do not overrun!
 */

#define FSYS_BUFLEN  0x8000
extern char *FSYS_BUF;

/*
 *  Linux setup parameters
 */

#define LINUX_MAGIC_SIGNATURE		0x53726448	/* "HdrS" */
#define LINUX_DEFAULT_SETUP_SECTS	4
#define LINUX_FLAG_CAN_USE_HEAP		0x80
#define LINUX_INITRD_MAX_ADDRESS	0x38000000
#define LINUX_MAX_SETUP_SECTS		64
#define LINUX_BOOT_LOADER_TYPE		0x71
#define LINUX_HEAP_END_OFFSET		(0x9000 - 0x200)

#define LINUX_BZIMAGE_ADDR		RAW_ADDR (0x100000)
#define LINUX_ZIMAGE_ADDR		RAW_ADDR (0x10000)
#define LINUX_OLD_REAL_MODE_ADDR	RAW_ADDR (0x90000)
#define LINUX_SETUP_STACK		0x9000

#define LINUX_FLAG_BIG_KERNEL		0x1

/* Linux's video mode selection support. Actually I hate it!  */
#define LINUX_VID_MODE_NORMAL		0xFFFF
#define LINUX_VID_MODE_EXTENDED		0xFFFE
#define LINUX_VID_MODE_ASK		0xFFFD

#define LINUX_CL_OFFSET			0x9000
#define LINUX_CL_END_OFFSET		0x90FF
#define LINUX_SETUP_MOVE_SIZE		0x9100
#define LINUX_CL_MAGIC			0xA33F

/*
 *  General disk stuff
 */

#define SECTOR_SIZE		0x200
#define SECTOR_BITS		9
#define BIOS_FLAG_FIXED_DISK	0x80

/* Not bad, perhaps.  */
#define NETWORK_DRIVE	0x20

#ifndef ASM_FILE
/*
 *  Below this should be ONLY defines and other constructs for C code.
 */

/* Error codes (descriptions are in common.c) */
typedef enum
{
  ERR_NONE = 0,
  ERR_BAD_FILENAME,
  ERR_BAD_FILETYPE,
  ERR_BAD_GZIP_DATA,
  ERR_BAD_GZIP_HEADER,
  ERR_BAD_PART_TABLE,
  ERR_BAD_VERSION,
  ERR_BELOW_1MB,
  ERR_BOOT_COMMAND,
  ERR_BOOT_FAILURE,
  ERR_BOOT_FEATURES,
  ERR_DEV_FORMAT,
  ERR_DEV_VALUES,
  ERR_EXEC_FORMAT,
  ERR_FILELENGTH,
  ERR_FILE_NOT_FOUND,
  ERR_FSYS_CORRUPT,
  ERR_FSYS_MOUNT,
  ERR_GEOM,
  ERR_NEED_LX_KERNEL,
  ERR_NEED_MB_KERNEL,
  ERR_NO_DISK,
  ERR_NO_PART,
  ERR_NUMBER_PARSING,
  ERR_OUTSIDE_PART,
  ERR_READ,
  ERR_SYMLINK_LOOP,
  ERR_UNRECOGNIZED,
  ERR_WONT_FIT,
  ERR_WRITE,
  ERR_BAD_ARGUMENT,
  ERR_UNALIGNED,
  ERR_PRIVILEGED,
  ERR_DEV_NEED_INIT,
  ERR_NO_DISK_SPACE,
  ERR_NUMBER_OVERFLOW,
  ERR_BAD_GZIP_CRC,
  ERR_FILESYSTEM_NOT_FOUND,
  ERR_NO_BOOTPATH,
  ERR_NEWER_VERSION,

  MAX_ERR_NUM
} grub_error_t;

extern unsigned long current_drive;
extern unsigned long current_partition;
extern char current_rootpool[MAXNAMELEN];
extern char current_bootfs[MAXNAMELEN];
extern char current_bootpath[MAXNAMELEN];
extern unsigned long long current_bootfs_obj;
extern char current_devid[MAXNAMELEN];
extern int is_zfs_mount;
extern unsigned long best_drive;
extern unsigned long best_part;
extern int find_best_root;

extern int fsys_type;

extern unsigned long part_start;
extern unsigned long part_length;

extern int current_slice;

/* these are the current file position and maximum file position */
extern int filepos;
extern int filemax;

/*
 *  Error variables.
 */

extern grub_error_t errnum;

/* one screen worth of messages 80x24 = 1920 chars -- more with newlines */
#define	SCREENBUF 2000

/* misc */
extern int devread(unsigned int sector, int byte_offset, int byte_len, char *buf);
extern int grub_read(char *buf, int len);
extern int substring (const char *s1, const char *s2);
extern void print_fsys_type (void);
extern void print_a_completion (char *name);

/* instrumentation variables */
extern void (*disk_read_hook) (unsigned int, int, int);
extern void (*disk_read_func) (unsigned int, int, int);

#endif /* ASM_FILE */

#endif /* ! GRUB_SHARED_HEADER */
