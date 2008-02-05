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


#ifndef lint
static char SCCSid[] =
	"@(#)pagein.c 1.2 06/01/03";
#endif

#include <sys/mman.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <libgen.h>

#define MAXPGS 16

static char *progname;

int
main(int argc, char *argv[])
{
    struct stat sb;
    char *addr, byt;
    char *eaddr;
    char *filename;
    int fd;
    int i, j;
    int pagesize = getpagesize();
    int pgincr;
    int errs = 0;
    char errbuf[1024];

    progname = basename(argv[0]);

    if (argc < 2) {
	(void) fprintf(stderr, "Usage: %s FILE [FILE...]\n", progname);
	exit(1);
    }

    for (i = 1; i < argc; i++) {
	filename = argv[i];
	if ((fd = open(filename, O_RDONLY)) < 0) {
	    (void) snprintf(errbuf, sizeof errbuf, "%s: %s: open",
			    progname, filename);
	    perror(errbuf);
	    errs++;
	    continue;
	}

	if (fstat(fd, &sb) < 0) {
	    (void) snprintf(errbuf, sizeof errbuf, "%s: %s: stat",
			    progname, filename);
	    perror(errbuf);
	    (void) close(fd);
	    errs++;
	    continue;
	}

	addr = mmap(NULL, sb.st_size, PROT_READ, MAP_SHARED, fd, 0);
	(void) close(fd);
	if (addr == MAP_FAILED) {
	    (void) snprintf(errbuf, sizeof errbuf, "%s: %s: mmap",
			    progname, filename);
	    perror(errbuf);
	    errs++;
	    continue;
	}
	
	pgincr = MAXPGS * pagesize;

	for (eaddr = addr + sb.st_size; addr < eaddr; addr += pgincr) {
	    int len = pgincr;
	    if (addr + len >= eaddr)
		len = eaddr - addr;
	    if (madvise((caddr_t) addr, len, MADV_WILLNEED) == -1) {
		(void) snprintf(errbuf, sizeof errbuf, "%s: %s: madvise",
				progname, filename);
		perror(errbuf);
		errs++;
		continue;
	    }
	    byt = addr[0];
/*
	    for (j=0; j<len; j+=(pagesize/2)) {
		byt = addr[j];
	    }
*/
	}
    }

    return(errs);
}
