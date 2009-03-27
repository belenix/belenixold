/*
 * CDDL HEADER START
 *
 * The contents of this file are subject to the terms of the
 * Common Development and Distribution License (the "License").
 * You may not use this file except in compliance with the License.
 *
 * You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
 * or http://www.opensolaris.org/os/licensing.
 * See the License for the specific language governing permissions
 * and limitations under the License.
 *
 * When distributing Covered Code, include this CDDL HEADER in each
 * file and include the License file at usr/src/OPENSOLARIS.LICENSE.
 * If applicable, add the following below this CDDL HEADER, with the
 * fields enclosed by brackets "[]" replaced with your own identifying
 * information: Portions Copyright [yyyy] [name of copyright owner]
 *
 * CDDL HEADER END
 */

/*
 * Copyright 2006 Sun Microsystems, Inc.  All rights reserved.
 * Use is subject to license terms.
 */

/*
 * Author: Moinak.Ghosh@Sun.COM
 *
 * Portions of this file contains code derived from:
 * http://www.bolthole.com/solaris/getfdisk.c by Philip Brown
 *
 * Compile Using:
 * LFS_CFLAGS=`getconf LFS_CFLAGS`
 * /opt/SUNWspro/bin/cc -g $LFS_CFLAGS prtpart.c -o prtpart.bin
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
#include <sys/fs/pc_label.h>
#include <sys/vtoc.h>
#include <sys/dkio.h>
#include <errno.h>

#define PC_SAFESECSIZE	(PC_SECSIZE * 2)
#define INDENT(n) for (int _k=0; _k<n; _k++) printf(" ");
#define INDENT_INCREMENT 2
#define REPEAT(n, c) for (int _c=0; _c<n; _c++) printf("%s", c);
#define RGB_RESTORE "\033[00m"
#define RGB_YELLOW 

/*
 * Additional offset (in 512 byte blocks ) for Linux SWAP
 * LBA address to skip any signature pages.
 */
#define LINSWAP_OFFSET 4096

static char buffer[PC_SAFESECSIZE];
static int showlinswap = 0;
static int listdos = 0;
static int human = 0;
static int translate = 0;
static int absolute = 0;
static int graphic = 0;
static int ldevs = 0;
static int uscale = 3;
static int pnum = 0;
static int exnum = 4; /* Ext partition numbers will start from 5 */
static int cols = 0;
static int tpart = 0;
static int tfound = 0;

static char *dev;
static char *tdev;
static char dev_prefix[1024];
static char lastdosdrive = 'd';
static uint64_t KB = 1024L;
static uint64_t MB = 1048576L;
static uint64_t GB = 1073741824L;
static uint64_t capacity;

struct _pinfo {
	int ext;
	uint64_t pstart;
	uint64_t psize;
};

static struct _pinfo all_parts[50];

static char *suffix[] = {
	"B",	/* 0 */
	"KB",	/* 1 */
	"MB",	/* 2 */
	"GB"	/* 3 */
};

/*
 * Linux swap/Legacy Solaris partition ID.
 */
#define LINSWAP 130

/*
 * Complete list of all the 255 partition types. Some are unknown types
 * and some entries are known to be unused.
 *
 * Courtesy of http://www.win.tue.nl/~aeb/partitions/partition_types-1.html
 */
static char *part_types[] = {
	"Empty",			/* 0 */
	"FAT12",			/* 1 */
	"XENIX /",			/* 2 */
	"XENIX /usr",			/* 3 */
	"FAT16 (Upto 32M)",		/* 4 */
	"DOS Extended",			/* 5 */
	"FAT16 (>32M, HUGEDOS)",	/* 6 */
	"IFS: NTFS",			/* 7 */
	"AIX Boot/QNX(qny)",		/* 8 */
	"AIX Data/QNX(qnz)",		/* 9 */
	"OS/2 Boot/Coherent swap",	/* 10 */
	"WIN95 FAT32(Upto 2047GB)",	/* 11 */
	"WIN95 FAT32(LBA)",		/* 12 */
	"Unused",			/* 13 */
	"WIN95 FAT16(LBA)",		/* 14 */
	"WIN95 Extended(LBA)",		/* 15 */
	"OPUS",				/* 16 */
	"Hidden FAT12",			/* 17 */
	"Diagnostic",			/* 18 */
	"Unknown",			/* 19 */
	"Hidden FAT16(Upto 32M)",	/* 20 */
	"Unknown",			/* 21 */
	"Hidden FAT16(>=32M)",		/* 22 */
	"Hidden IFS: HPFS",		/* 23 */
	"AST SmartSleep Partition",	/* 24 */
	"Unused/Willowtech Photon",	/* 25 */
	"Unknown",			/* 26 */
	"Hidden FAT32",			/* 27 */
	"Hidden FAT32(LBA)",		/* 28 */
	"Unused",			/* 29 */
	"Hidden FAT16(LBA)",		/* 30 */
	"Unknown",			/* 31 */
	"Unused/OSF1",			/* 32 */
	"Reserved/FSo2(Oxygen FS)",	/* 33 */
	"Unused/(Oxygen EXT)",		/* 34 */
	"Reserved",			/* 35 */
	"NEC DOS 3.x",			/* 36 */
	"Unknown",			/* 37 */
	"Reserved",			/* 38 */
	"Unknown",			/* 39 */
	"Unknown",			/* 40 */
	"Unknown",			/* 41 */
	"AtheOS File System",		/* 42 */
	"SyllableSecure",		/* 43 */
	"Unknown",			/* 44 */
	"Unknown",			/* 45 */
	"Unknown",			/* 46 */
	"Unknown",			/* 47 */
	"Unknown",			/* 48 */
	"Reserved",			/* 49 */
	"NOS",				/* 50 */
	"Reserved",			/* 51 */
	"Reserved",			/* 52 */
	"JFS on OS/2",			/* 53 */
	"Reserved",			/* 54 */
	"Unknown",			/* 55 */
	"THEOS 3.2 2GB",		/* 56 */
	"Plan9/THEOS 4",		/* 57 */
	"THEOS 4 4GB",			/* 58 */
	"THEOS 4 Extended",		/* 59 */
	"PartitionMagic Recovery",	/* 60 */
	"Hidden NetWare",		/* 61 */
	"Unknown",			/* 62 */
	"Unknown",			/* 63 */
	"Venix 80286",			/* 64 */
	"MINIX/PPC PReP Boot",		/* 65 */
	"Win2K Dynamic Disk/SFS(DOS)",	/* 66 */
	"Linux+DRDOS shared",		/* 67 */
	"GoBack partition",		/* 68 */
	"Boot-US boot manager",		/* 69 */
	"EUMEL/Elan",			/* 70 */
	"EUMEL/Elan",			/* 71 */
	"EUMEL/Elan",			/* 72 */
	"Unknown",			/* 73 */
	"ALFS/THIN FS for DOS",		/* 74 */
	"Unknown",			/* 75 */
	"Oberon partition",		/* 76 */
	"QNX 4,x",			/* 77 */
	"QNX 4,x 2nd Part",		/* 78 */
	"QNX 4,x 3rd Part",		/* 79 */
	"OnTrack DM R/O, Lynx RTOS",	/* 80 */
	"OnTrack DM R/W, Novell",	/* 81 */
	"CP/M",				/* 82 */
	"Disk Manager 6.0 Aux3",	/* 83 */
	"Disk Manager 6.0 DDO",		/* 84 */
	"EZ-Drive",			/* 85 */
	"Golden Bow VFeature/AT&T MS-DOS",	/* 86 */
	"DrivePro",			/* 87 */
	"Unknown",			/* 88 */
	"Unknown",			/* 89 */
	"Unknown",			/* 90 */
	"Unknown",			/* 91 */
	"Priam EDisk",			/* 92 */
	"Unknown",			/* 93 */
	"Unknown",			/* 94 */
	"Unknown",			/* 95 */
	"Unknown",			/* 96 */
	"SpeedStor",			/* 97 */
	"Unknown",			/* 98 */
	"Unix SysV, Mach, GNU Hurd",	/* 99 */
	"PC-ARMOUR, Netware 286",	/* 100 */
	"Netware 386",			/* 101 */
	"Netware SMS",			/* 102 */
	"Novell",			/* 103 */
	"Novell",			/* 104 */
	"Netware NSS",			/* 105 */
	"Unknown",			/* 106 */
	"Unknown",			/* 107 */
	"Unknown",			/* 108 */
	"Unknown",			/* 109 */
	"Unknown",			/* 110 */
	"Unknown",			/* 111 */
	"DiskSecure Multi-Boot",	/* 112 */
	"Reserved",			/* 113 */
	"Unknown",			/* 114 */
	"Reserved",			/* 115 */
	"Scramdisk partition",		/* 116 */
	"IBM PC/IX",			/* 117 */
	"Reserved",			/* 118 */
	"M2FS/M2CS,Netware VNDI",	/* 119 */
	"XOSL FS",			/* 120 */
	"Unknown",			/* 121 */
	"Unknown",			/* 122 */
	"Unknown",			/* 123 */
	"Unknown",			/* 124 */
	"Unknown",			/* 125 */
	"Unused",			/* 126 */
	"Unused",			/* 127 */
	"MINIX until 1.4a",		/* 128 */
	"MINIX since 1.4b, early Linux",/* 129 */
	"Linux swap",			/* 130 */
	"Linux native",			/* 131 */
	"OS/2 hidden,Win Hibernation",	/* 132 */
	"Linux extended",		/* 133 */
	"Old Linux RAID,NT FAT16 RAID",	/* 134 */
	"NTFS volume set",		/* 135 */
	"Linux plaintext part table",	/* 136 */
	"Unknown",			/* 137 */
	"Linux Kernel Partition",	/* 138 */
	"Fault Tolerant FAT32 volume",	/* 139 */
	"Fault Tolerant FAT32 volume",	/* 140 */
	"Free FDISK hidden PDOS FAT12",	/* 141 */
	"Linux LVM partition",		/* 142 */
	"Unknown",			/* 143 */
	"Free FDISK hidden PDOS FAT16",	/* 144 */
	"Free FDISK hidden DOS EXT",	/* 145 */
	"Free FDISK hidden FAT16 Large",/* 146 */
	"Hidden Linux native, Amoeba",	/* 147 */
	"Amoeba Bad Block Table",	/* 148 */
	"MIT EXOPC Native",		/* 149 */
	"Unknown",			/* 150 */
	"Free FDISK hidden PDOS FAT32",	/* 151 */
	"Free FDISK hidden FAT32 LBA",	/* 152 */
	"DCE376 logical drive",		/* 153 */
	"Free FDISK hidden FAT16 LBA",	/* 154 */
	"Free FDISK hidden DOS EXT",	/* 155 */
	"Unknown",			/* 156 */
	"Unknown",			/* 157 */
	"VSTaFS(Extent based FS)",	/* 158 */
	"BSD/OS",			/* 159 */
	"Laptop hibernation",		/* 160 */
	"Laptop hibernate,HP SpeedStor",/* 161 */
	"Unknown",			/* 162 */
	"HP SpeedStor",			/* 163 */
	"HP SpeedStor",			/* 164 */
	"BSD/386,386BSD,NetBSD,FreeBSD",/* 165 */
	"OpenBSD,HP SpeedStor",		/* 166 */
	"NeXTStep",			/* 167 */
	"Mac OS-X",			/* 168 */
	"NetBSD",			/* 169 */
	"Olivetti FAT12 1.44MB Service",/* 170 */
	"Mac OS-X Boot",		/* 171 */
	"Unknown",			/* 172 */
	"Unknown",			/* 173 */
	"ShagOS filesystem",		/* 174 */
	"ShagOS swap",			/* 175 */
	"BootStar Dummy",		/* 176 */
	"HP SpeedStor",			/* 177 */
	"Unknown",			/* 178 */
	"HP SpeedStor",			/* 179 */
	"HP SpeedStor",			/* 180 */
	"Unknown",			/* 181 */
	"Corrupted FAT16 NT Mirror Set",/* 182 */
	"Corrupted NTFS NT Mirror Set",	/* 183 */
	"Old BSDI BSD/386 swap",	/* 184 */
	"Unknown",			/* 185 */
	"Unknown",			/* 186 */
	"Boot Wizard hidden",		/* 187 */
	"Unknown",			/* 188 */
	"Unknown",			/* 189 */
	"Solaris 8 boot",		/* 190 */
	"Solaris x86",			/* 191 */
	"REAL/32 or Novell DOS secured",/* 192 */
	"DRDOS/secured(FAT12)",		/* 193 */
	"Hidden Linux",			/* 194 */
	"Hidden Linux swap",		/* 195 */
	"DRDOS/secured(FAT16,< 32M)",	/* 196 */
	"DRDOS/secured(Extended)",	/* 197 */
	"NT corrupted FAT16 volume",	/* 198 */
	"NT corrupted NTFS volume",	/* 199 */
	"DRDOS8.0+",			/* 200 */
	"DRDOS8.0+",			/* 201 */
	"DRDOS8.0+",			/* 202 */
	"DRDOS7.04+ secured FAT32(CHS)",/* 203 */
	"DRDOS7.04+ secured FAT32(LBA)",/* 204 */
	"CTOS Memdump",			/* 205 */
	"DRDOS7.04+ FAT16X(LBA)",	/* 206 */
	"DRDOS7.04+ secure EXT DOS(LBA)",/* 207 */
	"REAL/32 secure big, MDOS",	/* 208 */
	"Old MDOS secure FAT12",	/* 209 */
	"Unknown",			/* 210 */
	"Unknown",			/* 211 */
	"Old MDOS secure FAT16 <32M",	/* 212 */
	"Old MDOS secure EXT",		/* 213 */
	"Old MDOS secure FAT16 >=32M",	/* 214 */
	"Unknown",			/* 215 */
	"CP/M-86",			/* 216 */
	"Unknown",			/* 217 */
	"Non-FS Data",			/* 218 */
	"CP/M,Concurrent DOS,CTOS",	/* 219 */
	"Unknown",			/* 220 */
	"Hidden CTOS memdump",		/* 221 */
	"Dell PowerEdge utilities(FAT)",/* 222 */
	"DG/UX virtual disk manager",	/* 223 */
	"ST AVFS(STMicroelectronics)",	/* 224 */
	"SpeedStor 12-bit FAT EXT",	/* 225 */
	"Unknown",			/* 226 */
	"SpeedStor",			/* 227 */
	"SpeedStor 16-bit FAT EXT",	/* 228 */
	"Tandy MSDOS",			/* 229 */
	"Storage Dimensions SpeedStor",	/* 230 */
	"Unknown",			/* 231 */
	"Unknown",			/* 232 */
	"Unknown",			/* 233 */
	"Unknown",			/* 234 */
	"BeOS BFS",			/* 235 */
	"SkyOS SkyFS",			/* 236 */
	"Unused",			/* 237 */
	"EFI Header Indicator",		/* 238 */
	"EFI Filesystem",		/* 239 */
	"Linux/PA-RISC boot loader",	/* 240 */
	"SpeedStor",			/* 241 */
	"DOS 3.3+ secondary",		/* 242 */
	"SpeedStor Reserved",		/* 243 */
	"SpeedStor Large",		/* 244 */
	"Prologue multi-volume",	/* 245 */
	"SpeedStor",			/* 246 */
	"Unused",			/* 247 */
	"Unknown",			/* 248 */
	"pCache",			/* 249 */
	"Bochs",			/* 250 */
	"VMware File System",		/* 251 */
	"VMware swap",			/* 252 */
	"Linux raid autodetect",	/* 253 */
	"NT Disk Administrator hidden",	/* 254 */
	"Xenix Bad Block Table"		/* 255 */
};

void prtextended(int indx, struct ipart *parts, int fd, int level, off_t prev_pos);
int isVTOC(int fd, off_t offset);
static int isDosDrive(uchar_t checkMe);
static int isDosExtended(unsigned char checkMe);

/*
 * Scale the given number upto a given higher unit
 */
int
convertup(uint64_t *val, int scale) {
	if (*val < KB || scale == 0) {
		return (0);

	} else if (*val < MB || scale == 1) {
		*val /= KB;
		return (1);

	} else if (*val < GB || scale == 2) {
		*val /= MB;
		return (2);
	}

	*val /= GB;
	return (3);
}

/*
 * Convert a given partition ID to an descriptive string.
 * Just an index into the above table.
 */
void
numtoOS(unsigned char ostype, char *buffer)
{
	strcpy(buffer, part_types[ostype]);
}

/*
 * isDosDrive()
 *      Boolean function.  Give it the systid field for an fdisk partition
 *      and it decides if that's a systid that describes a DOS drive.  We
 *      use systid values defined in sys/dktp/fdisk.h.
 */
static int
isDosDrive(uchar_t checkMe)
{
        return ((checkMe == DOSOS12) || (checkMe == DOSOS16) ||
            (checkMe == DOSHUGE) || (checkMe == FDISK_WINDOWS) ||
            (checkMe == FDISK_EXT_WIN) || (checkMe == FDISK_FAT95) ||
            (checkMe == DIAGPART));
}

/*
 * isDosExtended()
 *	Boolean function.  Give it the systid field for an fdisk partition
 *	and it decides if that's a systid that describes an extended DOS
 *	partition.
 */
static int
isDosExtended(unsigned char checkMe)
{
	return ((checkMe == EXTDOS) || (checkMe == FDISK_EXTLBA));
}

/*
 * Determine whether the specified offset in the raw disk contains a
 * valid Solaris VTOC. This is used to differentiate between a valid
 * Linux swap and a legacy Solaris partition. Current Solaris x86
 * partition ids use a systid (0xbf) which is different from Linux swap.
 */
int
isVTOC(int fd, off_t offset)
{
	struct vtoc *vtoc_1;
	int retval, vtsize;
	off_t startsect;
	char buf[PC_SECSIZE * 2];

	startsect = lseek(fd, offset, SEEK_SET);
	if (startsect != offset) {
		return (-1);
	}

	vtsize = PC_SECSIZE * 2;
	if (read(fd, buf, vtsize) == vtsize) {
		vtoc_1 = (struct vtoc *)buf;

		if (vtoc_1->v_sanity == VTOC_SANE)
			return (0);
	}
	return (1);
}

/*
 * Print the partition table
 */
void
prtpart(struct ipart *parts, int fd, int level, off_t prev_pos, off_t cur_pos)
{
	int fpart, dosext = 0;
	char namebuff[50];
	int extendedPart = -1; /* index of extended dos partition */
	uint64_t sz_bytes;
	int sz_human;
	int partnum;

	if (showlinswap == 0 && listdos == 0 && ldevs == 0) {
		puts(" ");
		INDENT(level);
		if (!human)
			puts("#  start block  # nblocks    startCylSecHd endCylSecHd   OSType");
		else
			puts("#  start posn      # size             OSType");
	}

	for(fpart=0; fpart<FD_NUMPART; fpart++){
		int altnumsec;
		off_t offset;
		int isvtoc = -1;

		/*
	 	 * Skip empty partitions
	 	 */
		if (parts[fpart].systid == 0)
			continue;

		if (showlinswap == 1 && parts[fpart].systid == LINSWAP) {

			/*
			 * First check whether this is a legacy Solaris
			 * partition since old Solaris partition systid
			 * clashed with Linux swap systid. We check for
			 * the existence of valid VTOC in sectors 2 & 3.
			 */
			if (level > 0) {
				offset = (dosext ?
				(prev_pos/PC_SECSIZE):(cur_pos/PC_SECSIZE));
			} else {
				offset = 0;
			}

			offset = (parts[fpart].relsect + 1 + offset) * PC_SECSIZE;
			isvtoc = isVTOC(fd, offset);

		} else {
			dosext = isDosExtended(parts[fpart].systid);
			if (dosext && level > 0) {
				if (human || ldevs)
					goto nextext;
			}
		}

		if (level == 0) {
			pnum++;
			partnum = pnum;

		} else if (!dosext) {
			exnum++;
			partnum = exnum;
		}
		if (graphic)
			all_parts[pnum-1].ext = dosext;

		if (showlinswap == 0 && listdos == 0) {
			numtoOS(parts[fpart].systid, namebuff);
			if (parts[fpart].systid == LINSWAP) {
				if (isvtoc == 0) {
					strcpy(namebuff, "Old Solaris x86");
				}
			}
			if (!ldevs)
				INDENT(level);

			if (!absolute && !ldevs) {
				printf("%2d: %.10d   %.10d",
				(dosext && level>0)?0:partnum,
				parts[fpart].relsect,
				parts[fpart].numsect);

			} else {
				if (level > 0) {
					offset = (dosext ?
					(prev_pos/PC_SECSIZE):(cur_pos/PC_SECSIZE));
				} else {
					offset = 0;
				}
				if (ldevs) {
					if (translate) {
						uint64_t pstart, psize;
						if (tpart != partnum)
							goto nextext;

						pstart = parts[fpart].relsect +
							offset;
						psize = parts[fpart].numsect;
						printf("%sp0 %llu %llu\n", dev_prefix,
							pstart, psize);
						tfound = 1;
					} else {
						printf("%sp%d\t%s\n", dev_prefix, partnum,
						namebuff);
					}
					goto nextext;
				}
				if (!human) {
					printf("%2d: %.10llu   %.10d",
					(dosext && level>0)?0:partnum,
					parts[fpart].relsect + offset,
					parts[fpart].numsect);
				} else {
					uint64_t pstart, psize;
					int typr, typn;

					pstart = (uint64_t)(parts[fpart].relsect +
						offset) * PC_SECSIZE;
					psize = (uint64_t)(parts[fpart].numsect)
						* PC_SECSIZE;

					if (graphic) {
						all_parts[pnum-1].pstart = pstart;
						all_parts[pnum-1].psize = psize;
					}
					typr = convertup(&pstart, uscale);
					typn = convertup(&psize, uscale);

					printf("%2d: %.10llu%3s   %.10llu%3s",
					(dosext && level>0)?0:partnum,
					pstart, suffix[typr],
					psize, suffix[typn]);
				}
			}

			if (!human) {
				printf("    %2x/%2x/%2x",
					parts[fpart].begcyl,
					parts[fpart].begsect,
					parts[fpart].beghead);
				printf("    %2x/%2x/%2x",
					parts[fpart].endcyl,
					parts[fpart].endsect,
					parts[fpart].endhead);
			}
			printf("      %s\n", namebuff);

			fflush(stdout);

		} else if (showlinswap == 1) {

			/*
			 * Print parameters for Linux SWAP such that it can used as
			 * Solaris swap also. Exxentially we take the logical block
			 * offset of the Linux SWAP partition for device /dev/dsk/c*p0
			 * add couple of MB to that to offset across any signature
			 * pages and use the remaining area.
			 */
			if (parts[fpart].systid == LINSWAP) {
				if (isvtoc == 1) {
					printf("%sp0 %llu %u\n", dev_prefix,
						offset / PC_SECSIZE + LINSWAP_OFFSET,
						parts[fpart].numsect - (LINSWAP_OFFSET * 2));
				}
			}
		} else if (listdos == 1 && isDosDrive(parts[fpart].systid)) {
			/*
			 * Are we in primary partition table ?
			 */
			if (level == 0) {
				printf("%sp%d\n", dev_prefix, fpart+1);
			} else {
				/*
				 * Print colon separated pcfs device label
				 */
				printf("%sp0:%c\n", dev_prefix, lastdosdrive);
				lastdosdrive++;
			}
		}

nextext:
		if ((extendedPart < 0) && dosext) {
			extendedPart = fpart;
			prtextended(fpart, parts, fd, level+INDENT_INCREMENT, prev_pos);
			if (level == 0)
				puts(" ");
		}
	}
}

/*
 * Print the extended partition table
 */
void
prtextended(int indx, struct ipart *parts, int fd, int level, off_t prev_pos)
{
	int lastseek = 0;
	off_t diskblk, startsect;
	off_t rel_pos;
	struct ipart eparts[10];
	struct mboot mb;

	diskblk = parts[indx].relsect;

	/*
	 * prev_pos should not be added for the first entended partition
	 * entry in the primary partition table (see below) as it specifies
	 * an absolute position.
	 * But prev_pos is 0 in this case so this is okay. For subsequent
	 * extended partition entries prev_pos will contain the first
	 * ext partition's start so the correct value will be generated
	 * by adding it to the relative sector number.
	 */
	rel_pos = diskblk*PC_SECSIZE + prev_pos;

	startsect = lseek(fd, rel_pos, SEEK_SET);
	if (startsect != rel_pos) {
		perror("Ext part seek failed");
		return;
	}

	if (read(fd, buffer, PC_SECSIZE) != PC_SECSIZE) {
		perror("Err reading ext part table");
		return;
	}

	/*
	 * Load first sector of partition and check signature
	 */
	memcpy(&mb, buffer, sizeof(struct mboot));
	if (mb.signature != MBB_MAGIC){
		/*fprintf(stderr,"\nExtended partition table NOT VALID, ignoring\n");*/
		return;
	}

	/*
	 * Each extended partition table is of the same structure as
	 * the primary partition and can contain upto 4 entries.
	 * However in practice extended partitions are arranged as
	 * linked lists with each extended partition table containing
	 * 2 entries - one logical disk partition and one extended
	 * entry pointing to the next extended partition table (if
	 * there is one).
	 */
	memcpy(eparts, mb.parts, sizeof(struct ipart)*FD_NUMPART);

	/*
	 * The first extended partition entry in the primary partition
	 * table specifies an absolute sector number starting from
	 * sector 0 to indicate it's starting position.
	 *
	 * The subsequent nested extended partitions specify their
	 * starting position using relative sector numbers that are
	 * relative to the position of the first extended partition.
	 */
	if (level <= INDENT_INCREMENT)
		prtpart(eparts, fd, level, rel_pos, rel_pos);
	else
		prtpart(eparts, fd, level, prev_pos, rel_pos);
}

void
drawgraphic() {
	int part, scol, ssize, i;
	uint64_t cblock;
	struct winsize win;

	/*
	 * Get terminal info for Graphic depiction
	 */
	if (isatty(1)) {
		if (ioctl(1, TIOCGWINSZ, &win) < 0) {
			perror("stty: TIOCGWINSZ");
			return;

		} else {
			/*
	 		* How much disk space one character represents ?
	 		* Depends on terminal size;
	 		*/
			cblock = ((long double)capacity)/((long double)win.ws_col);
		}
	}

	printf("\nRelative Partition Sizes");
	printf("\n");
	REPEAT(win.ws_col, "=");
	printf("\n\n");
	REPEAT(win.ws_col, "=");
	printf("\n\033[A\033[A");

	for (part=0; part < pnum; part++) {
		scol = all_parts[part].pstart / cblock;

		if (all_parts[part].ext) {
			ssize = all_parts[part].psize / cblock;
			ssize--;

			printf("\n\n");
			REPEAT(scol, "\033[C");
			printf("|\n");
			REPEAT(scol, "\033[C");
			printf("%d", part+1);
			REPEAT(ssize, "-");
			printf("'\033[A\b|\n");
			printf("\n\033[A\033[A\033[A\033[A");
		} else {
			REPEAT(scol, "\033[C");
			printf("|\b\033[B%d\033[A", part+1);
			REPEAT(scol, "\b");
		}
	}
	printf("\n\n\n\n");
}

static int
is_lpart(char *dev) {
	if (strncmp(dev, "/dev", 4) != 0) {
		return (0);
	} else {
		size_t pos = strlen(dev)-1;
		while (isdigit(dev[pos])) pos--;
		if (dev[pos] != 'p')
			return (0);
		tpart = atoi(dev+pos+1);
	}
	return (1);
}

static void
usage() {
	printf( "\nUsage:\n prtpart\n"
		" prtpart -help\n"
		" prtpart <physical disk>\n"
		" prtpart <physical disk> <-lswap|-fat|-graph|-ldevs|-h[m|k]|-abs>\n"
		" prtpart -t <logical device>\n\n"
		"<physical disk> - The device name referring to the entire physical\n"
		"                  harddisk. On Solaris x86 this is of the form\n"
		"                  /dev/dsk/c<...>p0 where c<...> can be c<Num>d<Num>\n"
		"                  for an IDE disk or c<Num>d<Num>t<Num> for SCSI disk.\n\n"
		"<logical device> - This refers to a primary or logical partition on\n"
		"                  the harddisk.\n\n"
		"Invoking prtpart without any arguments lists all the devices names of\n"
		"the disk devices in the system. These device names can be used in the\n"
		"second and third forms of the command\n\n"
		"prtpart <physical disk> dumps the entire partition table (including all\n"
		"extended partitions exactly as it is on the disk\n\n"
		"-lswap - Lists the absolute Logical Block Addresses (LBA), and sizes of\n"
		"         all the Linux Swap partitions on the disk. The LBA computed is\n"
		"         a bit more than the actual beginning of the partition such that\n"
		"         these values can be passed to '/usr/sbin/swap -a' on a 64-bit\n"
		"         kernel to allow using Linux Swap without corrupting it\n\n"
		"-fat   - Lists the PCFS device names for all FAT/FAT32 partitions on\n"
		"         the disk. This removes confusion with PCFS device nomenclature\n"
		"         for extended FAT partitions\n\n"
		"-graph - Dumps the partition table (including extended partitions) and\n"
		"         displays a pictorial view of the partitions\n\n"
		"-ldevs - Lists logical device names for all the partitions on the disk\n"
		"         including the extended partitions. The extended partition\n"
		"         device names are non-standard virtual names for accessing\n"
		"         other filesystems, namely NTFS and EXT2FS\n\n"
		"-h[m|k] - Round off the LBA values to the nearest GB (-h), MB (-hm)\n"
		"         or KB (-hk). This suppresses printing of some details like\n"
		"         CHS and partition table links to make the output more user\n"
		"         friendly.\n\n"
		"-abs   - Translate all partition table LBA values to absolute LBA\n"
		"         values from the beginning of the disk. Normally these values\n"
		"         for extended partitions are relative.\n\n"
		"-t <logical device> - Translate the logical device name obtained using\n"
		"         -ldevs option. This output is of the form:\n"
		"         /dev/dsk/c<...>p0 <absolute LBA> <size>\n"
		"         where <absolute LBA> is the starting offset and <size> is the\n"
		"         size in blocks of the partition. This used internally to access\n"
		"         NTFS and EXT2FS on extended partitions\n\n"
		"-help  - Prints this help\n\n");
}

int
main(int argc, char *argv[]){
	int fd, i, len, typ;
	char *pos;
	struct dk_cinfo	dkc;
	struct dk_minfo dkmi;
	struct ipart parts[10];
	struct mboot *mbootptr,mboot;
	uint64_t hcap;
	size_t ppos;
	int retval = 0;
	
	if(argc<2){
		usage();
		exit(1);
	}

	tdev = NULL;
	dev = NULL;
	if (argc >= 2) {
		/*
		 * Parse options
		 */
		for (i=1; i<argc; i++) {
			if (strcmp(argv[i], "-help") == 0) {
				usage();
				exit(0);

			} else if (strcmp(argv[i], "-lswap") == 0) {
				if (listdos == 1) {
					printf("-lswap and -fat are mutually exclusive\n");
					exit (1);
				}
				showlinswap = 1;

			} else if (strcmp(argv[i], "-fat") == 0) {
				if (showlinswap == 1) {
					printf("-lswap and -fat are mutually exclusive\n");
					exit (1);
				}
				listdos = 1;
			} else if (strcmp(argv[i], "-graph") == 0) {
				graphic = 1;
				human = 1;
				absolute = 1;

			} else if (strcmp(argv[i], "-ldevs") ==0) {
				ldevs = 1;

			} else if (strcmp(argv[i], "-h") == 0) {
				human = 1;
				absolute = 1;

			} else if (strcmp(argv[i], "-hk") == 0) {
				human = 1;
				absolute = 1;
				uscale = 1;

			} else if (strcmp(argv[i], "-hm") == 0) {
				human = 1;
				absolute = 1;
				uscale = 2;

			} else if (strcmp(argv[i], "-abs") == 0) {
				absolute = 1;

			} else if (strcmp(argv[i], "-t") == 0) {
				if (i+1 < argc) {
					if (!is_lpart(argv[i+1])) {
						printf("-t option requires a virtual");
						printf(" device name\n");
						retval = 1;
						goto done;
					}
				} else {
					printf("-t option requires a virtual");
					printf(" device name\n");
					retval = 1;
					goto done;
				}
				translate = 1;
				ldevs = 1;
				tdev = strdup(argv[i+1]);
				i++;
			}
		}
	}

	if (listdos == 1)
		graphic = 0;

	if (ldevs == 1) {
		listdos = 0;
		graphic = 0;
	}

	if (!translate)
		dev = strdup(argv[1]);
	else
		dev = strdup(tdev);

	pos = strstr(dev, "rdsk");
	if (pos == NULL) {
		char *ndev;

		ndev = (char *)malloc(strlen(dev) + 2);
		strcpy(ndev, dev);
		pos = strstr(dev, "dsk");
		if (pos == NULL) {
			printf("Must specify a disk device: /dev/dsk/... or /dev/rdsk/...\n");
			retval = 1;
			goto done;
		}
		strncpy(ndev, dev, pos-dev);
		ndev[pos-dev] = 'r';
		strcpy(ndev+(pos-dev)+1, pos);

		free(dev);
		dev = ndev;
	}

	len = strlen(dev);
	strcpy(dev_prefix, dev);
	ppos = len-1;
	while(isdigit(dev_prefix[ppos])) ppos--;
	if (dev_prefix[ppos] != 'p') {
		printf("The device name must end with pN where N is the\n");
		printf("partition number\n");

		retval = 1;
		goto done;
	}
	dev_prefix[ppos] = '\0';
	pos = strstr(dev_prefix, "rdsk");
	strcpy(pos, pos+1);

	if (translate) {
		dev[ppos+1] = '0';
		dev[ppos+2] = '\0';
	}

	fd=open(dev,O_RDONLY);
	if(fd <0){
		perror("cannot open file");
		retval = 1;
		goto done;
	}

	/*
	 * Get disk parameters
	 */
	if (ioctl(fd, DKIOCINFO, &dkc) < 0) {
		perror("Failed to query device ");
		retval = 1;
		goto done;
	}

	/*
	 * Get media information
	 */
	if (ioctl(fd, DKIOCGMEDIAINFO, &dkmi) < 0) {
		perror("Failed to query device ");
		retval = 1;
		goto done;
	}

	capacity = dkmi.dki_capacity * (uint64_t)dkmi.dki_lbsize;
	hcap = capacity;
	typ = convertup(&hcap, 3);

	if(read(fd, buffer, PC_SECSIZE) != PC_SECSIZE){
		perror("err reading initial sector");
		retval = 1;
		goto done;
	}

	if (showlinswap == 0 && listdos == 0 && translate == 0) {
		printf("\nFdisk information for device %s\n",argv[1]);
		if (!human && !ldevs)
			printf("\nBlock Size : %d bytes\n", PC_SECSIZE);

		if (absolute) {
			printf("All values are absolute from beginning of physical disk\n\n");
		}
	}

	/*
	 * Print disk parameters
	 */
	if (listdos == 0 && showlinswap == 0 && ldevs == 0) {
		printf("Controller          : %s\n", dkc.dki_cname);
		printf("Disk                : %s\n", dkc.dki_dname);
		printf("Formatted Capacity  : %llu %2s\n", hcap, suffix[typ]);
	}

	if (ldevs && translate == 0) {
		printf("\n** NOTE **\n");
		printf("%sp0      - Physical device referring to entire physical disk\n",
					dev_prefix);
		printf("%sp1 - p4 - Physical devices referring to the 4 primary partitions\n",
					dev_prefix);
		printf("%sp5 ...  - Virtual devices referring to logical partitions\n",
					dev_prefix);
		printf("\nVirtual device names can be used to access EXT2 and NTFS on logical");
		printf(" partitions\n\n");
	}
	memcpy(&mboot,buffer,sizeof(struct mboot));
	mbootptr=&mboot;

	if(mbootptr->signature!= MBB_MAGIC){
		fprintf(stderr,"FDISK table NOT VALID\n");
		fprintf(stderr,"Reminder: dont forget to use either 'p0' or 'D0' device\n");

		retval = 1;
		goto done;
	}

	memcpy(parts, mbootptr->parts, sizeof(struct ipart)*FD_NUMPART);

	/*
	 * Now print the primary partition table and any extended
	 * partition chains.
	 */
	prtpart(parts, fd, 0, 0, 0);
	if (translate && !tfound) {
		printf("Logical partition name does not exist\n");
		retval = 1;
	}

	if (graphic)
		drawgraphic();

done:
	if (tdev)
		free(tdev);
	if (dev)
		free(dev);

	close(fd);
	return (retval);
}
