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

# ifdef FSYS_EXT2FS
extern int ext2fs_mount(void);
extern int ext2fs_read (char *buf, int len);
extern int ext2fs_dir (char *dirname);
# endif

struct fsys_entry fsys_table[NUM_FSYS + 1] =
{
  /* TFTP should come first because others don't handle net device.  */
# ifdef FSYS_TFTP
  {"tftp", tftp_mount, tftp_read, tftp_dir, tftp_close, 0},
# endif
# ifdef FSYS_FAT
  {"fat", fat_mount, fat_read, fat_dir, 0, 0},
# endif
# ifdef FSYS_EXT2FS
  {"ext2fs", ext2fs_mount, ext2fs_read, ext2fs_dir, 0, 0},
# endif
# ifdef FSYS_MINIX
  {"minix", minix_mount, minix_read, minix_dir, 0, 0},
# endif
# ifdef FSYS_REISERFS
  {"reiserfs", reiserfs_mount, reiserfs_read, reiserfs_dir, 0, reiserfs_embed},
# endif
# ifdef FSYS_VSTAFS
  {"vstafs", vstafs_mount, vstafs_read, vstafs_dir, 0, 0},
# endif
# ifdef FSYS_JFS
  {"jfs", jfs_mount, jfs_read, jfs_dir, 0, jfs_embed},
# endif
# ifdef FSYS_XFS
  {"xfs", xfs_mount, xfs_read, xfs_dir, 0, 0},
# endif
# ifdef FSYS_UFS
  {"ufs", ufs_mount, ufs_read, ufs_dir, 0, ufs_embed},
# endif
# ifdef FSYS_UFS2
  {"ufs2", ufs2_mount, ufs2_read, ufs2_dir, 0, ufs2_embed},
# endif
# ifdef FSYS_ZFS
  {"zfs", zfs_mount, zfs_read, zfs_open, 0, zfs_embed},
# endif
# ifdef FSYS_ISO9660
  {"iso9660", iso9660_mount, iso9660_read, iso9660_dir, 0, 0},
# endif
  /* XX FFS should come last as it's superblock is commonly crossing tracks
     on floppies from track 1 to 2, while others only use 1.  */
# ifdef FSYS_FFS
  {"ffs", ffs_mount, ffs_read, ffs_dir, 0, ffs_embed},
# endif
  {0, 0, 0, 0, 0, 0}
};

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
	sector += byte_offset >> SECTOR_BITS;
	byte_offset &= SECTOR_SIZE - 1;
	 */

	start_pos = (off_t)(part_start + sector) * (off_t)SECTOR_SIZE + byte_offset;
	actual_pos = lseek(cur_fd, start_pos, SEEK_SET);
	if (actual_pos != start_pos) {
		perror("(devread)Seek failed");
		errnum = ERR_READ;
		return (0);
	}
	if (read(cur_fd, buf, byte_len) < byte_len) {
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

/* If DO_COMPLETION is true, just print NAME. Otherwise save the unique
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
    printf (" %s", name);

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

void
scan_parts(char *sec, int fd, int nest_level, off_t pext_part_pos, off_t this_ext_start) {
	int partno;
	off_t ext_start, actual_start;
	char *embr[SECTOR_SIZE];
	unsigned long part_off;
	char dir[PATH_MAX];
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
			if (ext_start > capacity) {
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
				scan_parts((char *)embr, fd, nest_level + 1, ext_start, this_ext_start);
			} else {
				scan_parts((char *)embr, fd, nest_level + 1, pext_part_pos, this_ext_start);
			}
		} else {
			
			part_start = PC_SLICE_START(sec, partno) + this_ext_start;
			part_length = PC_SLICE_LENGTH(sec, partno);
			cur_fd = fd;
			if (nest_level > 0) {
				current_partition = partno + 4;
			} else {
				current_partition = partno;
			}
			if (ext2fs_mount()) {
				printf("Ext2fs mounted successfully.\n");
				strcpy(dir, "/lib/modules/");
				ret = ext2fs_dir(dir);
				printf("\n ret = %d\n", ret);
			}
		}
	}
}

int
main(int argc, char *argv[]) {
	int fd, len;
	struct dk_minfo dkmi;
	char *pos, mbr[SECTOR_SIZE];

	if (argc < 2) {
		fprintf(stderr, "pscan: /dev/rdsk/c...p0\n\n");
		exit(1);
	}

	dev = strdup(argv[1]);
	pos = strstr(dev, "rdsk");
	if (pos == NULL) {
		fprintf(stderr, "Please specify a raw disk device.\n");
		exit(1);
	}

	len = strlen(dev);
	len--;
	if (dev[len] != '0' || dev[len-1] != 'p') {
		fprintf(stderr, "Please specify a physical disk device (/dev/rdsk/c...p0)\n");
		exit(1);
	}

	fd = open(dev, O_RDONLY);
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
		exit(1);
	}

	capacity = dkmi.dki_capacity * (uint64_t)dkmi.dki_lbsize;
	if (read(fd, mbr, SECTOR_SIZE) != SECTOR_SIZE) {
		perror("Error reading MBR");
		close(fd);
		exit(1);
	}

	if (!PC_MBR_CHECK_SIG(mbr)) {
		fprintf(stderr, "Invalid MBR/Fdisk table.\n");
		close(fd);
		exit(1);
	}

	FSYS_BUF = (char *)malloc(FSYS_BUFLEN);
	scan_parts((char *)mbr, fd, 1, 0, 0);
	free(FSYS_BUF);
	return (0);
}

