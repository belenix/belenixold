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
 * Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
 * Use is subject to license terms.
 */


#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#include <syslog.h>
#include <stropts.h>
#include <sys/mem.h>
#include <sys/statvfs.h>
#include <sys/dumphdr.h>
#include <sys/sysmacros.h>

static char 	progname[9] = "checkcore";
static char	*dumpfile;		/* source of raw crash dump */
static long	pagesize;		/* dump pagesize */
static int	dumpfd = -1;		/* dumpfile descriptor */
static dumphdr_t corehdr, dumphdr;	/* initial and terminal dumphdrs */
static offset_t	endoff;			/* offset of end-of-dump header */
static int	verbose;		/* chatty mode */
static int	disregard_valid_flag;	/* disregard valid flag */

/*
 * System call / libc wrappers that exit on error.
 */
static int
Open(const char *name, int oflags, mode_t mode)
{
	int fd;

	if ((fd = open64(name, oflags, mode)) == -1)
		if (verbose)
			fprintf(stderr, "open(\"%s\"): %s\n",
		    		name, strerror(errno));
	return (fd);
}

static void
Pread(int fd, void *buf, size_t size, offset_t off)
{
	if (pread64(fd, buf, size, off) != size)
		if (verbose)
			fprintf(stderr, "pread: %s\n", strerror(errno));
}

/*
 * returncode = 0: It is okay to use this swap device, there is no dump
 * returncode = 1: Do not use this swap device there is a possible dump
 */
static int
read_dumphdr(void)
{
	int returncode = 1;
	dumpfd = Open(dumpfile, O_RDONLY, 0644);

	if (dumpfd == -1)
		exit(1);

	endoff = llseek(dumpfd, -DUMP_OFFSET, SEEK_END) & -DUMP_OFFSET;
	Pread(dumpfd, &dumphdr, sizeof (dumphdr), endoff);

	pagesize = dumphdr.dump_pagesize;

	if ((dumphdr.dump_flags & DF_VALID) == 0) {
		if (verbose)
			printf("dump already processed\n");
		returncode = 0;
	}

	if (dumphdr.dump_magic != DUMP_MAGIC) {
		if (verbose)
			printf("bad magic number %x\n", dumphdr.dump_magic);
		returncode = 0;
	}

	if (dumphdr.dump_version != DUMP_VERSION)
		if (verbose)
			printf("dump version (%d) != %s version (%d)\n",
		    	dumphdr.dump_version, progname, DUMP_VERSION);

	if (verbose)
		printf("dump is from %u-bit kernel\n",
		    	dumphdr.dump_wordsize, DUMP_WORDSIZE);
	/*
	 * Read the initial header, clear the valid bits, and compare headers.
	 * The main header may have been overwritten by swapping if we're
	 * using a swap partition as the dump device.
	 */
	Pread(dumpfd, &corehdr, sizeof (dumphdr_t), dumphdr.dump_start);

	corehdr.dump_flags &= ~DF_VALID;
	dumphdr.dump_flags &= ~DF_VALID;

	if (memcmp(&corehdr, &dumphdr, sizeof (dumphdr_t)) != 0) {
		returncode = 0;
		if (verbose)
			printf("initial dump header corrupt\n");
	}

	return (returncode);
}

int
main(int argc, char *argv[])
{
	int c;

	while ((c = getopt(argc, argv, "vf:")) != EOF) {
		switch (c) {
		case 'v':
			verbose++;
			break;
		case 'f':
			dumpfile = optarg;
			break;
		}
	}

	if (dumpfile == NULL) {
		fprintf(stderr, "Usage: checkcore -f <dump file/device> [-v]\n");
		return (1);
	}

	return (read_dumphdr());
}
