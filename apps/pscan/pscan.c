/* pscan.c - Main partition scanner program */
/*
 * Alternate OS Scanner utility for BeleniX. Scan other OSes in other
 * partitions and generate boot entries suitable for adding into GRUB's
 * menu.lst.
 */
/*
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

#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/termios.h>
#include <ctype.h>
#include <sys/dktp/fdisk.h>
#include <sys/dkio.h>
#include <errno.h>
#include <limits.h>

#include "filesys.h"
#include "shared.h"

#define INDENT(n) for (int _i=0; _i<n; _i++) printf(" ");

unsigned long current_drive = 1;
int current_slice = 0;
unsigned long current_partition = 0xFFFFFF;
static uint64_t KB = 1024L;
static uint64_t MB = 1048576L;
static uint64_t GB = 1073741824L;
static uint64_t capacity;
static char *dev;
static int do_completion = 0;
static int do_print = 0;
static int entry_found = 0;
static int unique = 0;
static char unique_string[UNIQUE_BUFLEN];

unsigned long part_start;
unsigned long part_length;
int cur_fd;
char *FSYS_BUF;

char current_rootpool[MAXNAMELEN];
char current_bootfs[MAXNAMELEN];
char current_bootpath[MAXNAMELEN];
unsigned long long current_bootfs_obj;
char current_devid[MAXNAMELEN];
int is_zfs_mount;
unsigned long best_drive;
unsigned long best_part;
int find_best_root;
int fsys_type;
int filepos = 0;
int filemax;
int print_possibilities = 1;
grub_error_t errnum;
int fsmax = MAXINT;

/* dummy instrumentation variables */
void (*disk_read_hook) (unsigned int, int, int) = NULL;
void (*disk_read_func) (unsigned int, int, int) = NULL;

struct fsys_entry fsys_table[NUM_FSYS + 1] =
{
# ifdef FSYS_NTFS
  {"ntfs", ntfs_mount, ntfs_read, ntfs_dir, 0, 0, OS_WINDOWS},
# endif
# ifdef FSYS_FAT
  {"fat", fat_mount, fat_read, fat_dir, 0, 0, OS_WINDOWS},
# endif
# ifdef FSYS_EXT2FS
  {"ext2fs", ext2fs_mount, ext2fs_read, ext2fs_dir, 0, 0, OS_LINUX},
# endif
# ifdef FSYS_MINIX
  {"minix", minix_mount, minix_read, minix_dir, 0, 0, OS_MINIX},
# endif
# ifdef FSYS_REISERFS
  {"reiserfs", reiserfs_mount, reiserfs_read, reiserfs_dir, 0, reiserfs_embed, OS_LINUX},
# endif
# ifdef FSYS_JFS
  {"jfs", jfs_mount, jfs_read, jfs_dir, 0, jfs_embed, OS_LINUX},
# endif
# ifdef FSYS_XFS
  {"xfs", xfs_mount, xfs_read, xfs_dir, 0, 0, OS_LINUX},
# endif
# ifdef FSYS_UFS
  {"ufs", ufs_mount, ufs_read, ufs_dir, 0, ufs_embed, OS_SOLARIS},
# endif
# ifdef FSYS_UFS2
  {"ufs2", ufs2_mount, ufs2_read, ufs2_dir, 0, ufs2_embed, OS_BSD},
# endif
# ifdef FSYS_ZFS
  {"zfs", zfs_mount, zfs_read, zfs_open, 0, zfs_embed, OS_SOLARIS},
# endif
# ifdef FSYS_ISO9660
  {"iso9660", iso9660_mount, iso9660_read, iso9660_dir, 0, 0, OS_GENERIC},
# endif
  /* XX FFS should come last as it's superblock is commonly crossing tracks
     on floppies from track 1 to 2, while others only use 1.  */
# ifdef FSYS_FFS
  {"ffs", ffs_mount, ffs_read, ffs_dir, 0, ffs_embed, OS_LINUX},
# endif
  {0, 0, 0, 0, 0, 0}
};

static void probe_linux(int partno);
static void probe_windows(int partno);

int
devread(unsigned int sector, int byte_offset, int byte_len, char *buf)
{
  off_t start_pos;
  off_t actual_pos;

  /*
   *  Check partition boundaries
   */
  if ((sector + ((byte_offset + byte_len - 1) >> SECTOR_BITS)) >= part_length)
    {
      errnum = ERR_OUTSIDE_PART;
      return 0;
    }

  /*
   *  Get the read to the beginning of a partition.
   */
  start_pos = (off_t)(part_start + sector) * (off_t)SECTOR_SIZE + byte_offset;
  actual_pos = lseek(cur_fd, start_pos, SEEK_SET);
  if (actual_pos != start_pos)
    {
      perror("(devread)Seek failed");
      errnum = ERR_READ;
      return (0);
    }

  if (read(cur_fd, buf, byte_len) < byte_len)
    {
      perror("(devread)Read failed");
      errnum = ERR_READ;
      return (0);
    }

  return (1);
}

int
grub_read (char *buf, int len)
{
	/* Make sure "filepos" is a sane value */
	if ((filepos < 0) || (filepos > filemax))
		filepos = filemax;

	/* Make sure "len" is a sane value */
	if ((len < 0) || (len > (filemax - filepos)))
		len = filemax - filepos;

	/* if target file position is past the end of
	the supported/configured filesize, then
	there is an error */
	if (filepos + len > fsmax)
	{
		errnum = ERR_FILELENGTH;
		return 0;
	}

	return (*(fsys_table[fsys_type].read_func)) (buf, len);
}

int
grub_open(char *filename)
{
  /* if any "dir" function uses/sets filepos, it must
     set it to zero before returning if opening a file! */
  filepos = 0;

  /* This accounts for partial filesystem implementations. */
  fsmax = MAXINT;
  if (!errnum && fsys_type == NUM_FSYS)
    errnum = ERR_FSYS_MOUNT;

  /* set "dir" function to open a file */
  print_possibilities = 0;

  if (!errnum && (*(fsys_table[fsys_type].dir_func)) (filename))
    {
      return 1;
    }

  return 0;
}

int
dir(char *dirname)
{
  if (*dirname != '/')
    errnum = ERR_BAD_FILENAME;

  if (fsys_type == NUM_FSYS)
    errnum = ERR_FSYS_MOUNT;

  if (errnum)
    return 0;

  /* set "dir" function to list completions */
  print_possibilities = 1;

  return (*(fsys_table[fsys_type].dir_func))(dirname);
}


void
print_fsys_type (void)
{
  if (! do_completion)
    {
      printf(" Filesystem type ");

      if (fsys_type != NUM_FSYS)
        printf("is %s, ", fsys_table[fsys_type].name);
      else
        printf("unknown, ");

      if (current_partition == 0xFFFFFF)
        printf("using whole disk\n");
      else
        printf("partition type 0x%x\n", current_slice & 0xFF);
    }
}

/* If DO_COMPLETION is false, just print NAME. Otherwise save the unique
   part into UNIQUE_STRING.  */
void
print_a_completion (char *name)
{
  /* If NAME is "." or "..", do not count it.  */
  if (strcmp(name, ".") == 0 || strcmp(name, "..") == 0)
    return;

  if (do_completion)
    {
      char *buf = unique_string;

      if (! unique)
        while ((*buf++ = *name++))
          ;
      else
        {
          while (*buf && (*buf == *name))
            {
              buf++;
              name++;
            }
          /* mismatch, strip it.  */
          *buf = '\0';
        }
    }
  else
    {
      if (do_print)
        {
          printf (" %s", name);
        }
      else
        {
          printf (" %s\n", name);
          entry_found++;
        }
    }

  unique++;
}

int
substring (const char *s1, const char *s2)
{
  while (*s1 == *s2)
    {
      /* The strings match exactly. */
      if (! *(s1++))
        return 0;
      s2 ++;
    }

  /* S1 is a substring of S2. */
  if (*s1 == 0)
    return -1;

  /* S1 isn't a substring. */
  return 1;
}

void *
grub_memmove (void *to, const void *from, int len)
{
  return (memmove(to, from, len));
}

void *
grub_memset (void *start, int c, int len)
{
  return (memset(start, c, len));
}

void
scan_fsys(void)
{
	int i;
	unsigned long o_part_start;
	unsigned long o_part_length;
	unsigned long o_current_partition;

	o_part_start = part_start;
	o_part_length = part_length;
	o_current_partition = current_partition;

	for (i=0; i < NUM_FSYS; i++) {
		if ((*(fsys_table[i].mount_func))()) {
			fprintf(stderr, "Partition: %ld, Filesystem %s mounted successfully.\n",
			    current_partition, fsys_table[i].name);
			fsys_type = i;
			errnum = 0;

			if (fsys_table[i].os_plat == OS_LINUX) {
				probe_linux(current_partition);

			} else if (fsys_table[i].os_plat == OS_WINDOWS) {
				probe_windows(current_partition);
			}
			return;
		}
		part_start = o_part_start;
		part_length = o_part_length;
		current_partition = o_current_partition;
	}
}

void
scan_parts(char *sec, int fd, int nest_level, off_t pext_part_pos,
    off_t this_ext_start, int partn)
{
	int partno;
	off_t ext_start, actual_start;
	char *embr[SECTOR_SIZE];
	unsigned long part_off;
	int ret;

	for (partno = 0; partno < FD_NUMPART; partno++) {
		current_slice = PC_SLICE_TYPE(sec, partno);

		if (current_slice == 0)
			continue;

		INDENT(nest_level);
		printf("%3d\n", current_slice);

		if (IS_PC_SLICE_TYPE_EXTENDED(current_slice)) {
			this_ext_start = PC_SLICE_START(sec, partno) + (pext_part_pos / SECTOR_SIZE);
			ext_start = (off_t)PC_SLICE_START(sec, partno) * (off_t)SECTOR_SIZE + pext_part_pos;
			if (ext_start > capacity)
			{
				fprintf(stderr, "WARNING: Extended partition beyond device size!\n");
				continue;
			}

			actual_start = lseek(fd, ext_start, SEEK_SET);
			if (actual_start != ext_start) {
				perror("WARNING: Ext part seek failed.\n");
				continue;
			}

			if (read(fd, embr, SECTOR_SIZE) != SECTOR_SIZE) {
				perror("WARNING: Error reading ext part table.\n");
				continue;
			}
			if (pext_part_pos == 0) {
				scan_parts((char *)embr, fd, nest_level + 1, ext_start,
				    this_ext_start, 0);
			} else {
				scan_parts((char *)embr, fd, nest_level + 1, pext_part_pos,
				    this_ext_start, partn+1);
			}
		} else {
			part_start = PC_SLICE_START(sec, partno) + this_ext_start;
			part_length = PC_SLICE_LENGTH(sec, partno);

			if (pext_part_pos == 0) {
				current_partition = partno;
			} else {
				current_partition = partn + 4;
			}

			scan_fsys();
		}
	}
}

int
main(int argc, char *argv[]) {
	int fd, len;
	struct dk_minfo dkmi;
	char *pos, mbr[SECTOR_SIZE];
	char *bdev;

	if (argc < 2) {
		fprintf(stderr, "pscan: /dev/rdsk/c...p0 /dev/dsk/c...p0\n\n");
		exit(1);
	}

	dev = strdup(argv[1]);
	bdev = strdup(argv[2]);
	pos = strstr(dev, "rdsk");
	if (pos == NULL) {
		pos = strstr(dev, "raw");
		if (pos == NULL) {
			fprintf(stderr, "Please specify a raw disk device.\n");
			exit(1);
		}
	}

	len = strlen(dev);
	len--;
	if (dev[len] != '0' || dev[len-1] != 'p') {
		fprintf(stderr, "Please specify a physical disk device (/dev/rdsk/c...p0)\n");
		exit(1);
	}

	/*
	 * Open Raw Device for ioctls and partition table reading.
	 */
	fd = open(dev, O_RDONLY);
	if (fd < 0) {
		perror("Cannot open device");
		exit(1);
	}

	/*
	 * Open Block Device for general filesystem access.
	 */
	cur_fd = open(bdev, O_RDONLY);
	if (fd < 0) {
		perror("Cannot open device");
		exit(1);
	}

	/*
	 * Fetch media information.
	 */
	if (ioctl(fd, DKIOCGMEDIAINFO, &dkmi) < 0) {
		perror("DKIOCGMEDIAINFO failed on device");
		close(fd);
		close(cur_fd);
		exit(1);
	}

	capacity = dkmi.dki_capacity * (uint64_t)dkmi.dki_lbsize;
	if (read(fd, mbr, SECTOR_SIZE) != SECTOR_SIZE) {
		perror("Error reading MBR");
		close(fd);
		close(cur_fd);
		exit(1);
	}

	if (!PC_MBR_CHECK_SIG(mbr)) {
		fprintf(stderr, "Invalid MBR/Fdisk table.\n");
		close(fd);
		close(cur_fd);
		exit(1);
	}

	FSYS_BUF = (char *)malloc(FSYS_BUFLEN);
	scan_parts((char *)mbr, fd, 1, 0, 0, 0);
	free(FSYS_BUF);
	close(fd);
	close(cur_fd);
	return (0);
}


int
read_line(char *buf, int len)
{
	char c;
	int i, cnt;

	len--;
	c = 0; i = 0;
	cnt = 0;
	while (grub_read(&c, 1) && i < len) {
		cnt++;
		if (c != '\n')
			buf[i++] = c;
		else
			break;
	}
	buf[i] = '\0';

	return (cnt);
}

/*
 * Start OS heuristics functions. These try to detect a bootable OS
 * slice for the given OS type.
 */

void
probe_linux(int partno)
{
	char path[PATH_MAX];
	char fbuf[1024];

	/*
         * Check if we have /lib/modules.
         */
	entry_found = 0;
	strcpy(path, "/lib/modules/");
	dir(path);

	if (entry_found > 0) {
		/*
		 * This is a Linux root. Try to fetch the menu.lst
		 */
		strcpy(path, "/boot/grub/menu.lst");
		if (grub_open(path)) {
			while (read_line(fbuf, 1024) > 0) {
				printf("%s\n", fbuf);
			}
		}
	}
}

void
probe_windows(int partno)
{
	char path[PATH_MAX];
	char fbuf[1024];

	/*
	 * Check if there is WINDOWS
         */
	entry_found = 0;
	strcpy(path, "/WINDOWS/tsoc.log");
	if (grub_open(path)) {
		while (read_line(fbuf, 1024) > 0) {
			printf("%s\n", fbuf);
		}
	}
}
