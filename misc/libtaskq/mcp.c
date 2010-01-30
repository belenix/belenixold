#include <sys/stat.h>
#include <stdio.h>
#include <fcntl.h>
#include <locale.h>
#include <string.h>
#include <strings.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <libtaskq.h>

/* Copy in units of 256K */
#define SEGSIZE 262144

struct cp_args {
	char *fromf;
	char *tof;
	uint64_t pos;
	uint64_t sz;
	int rv;
	int cnum;
};

static int errorflag = 0;

/*
 * Copy the given segment of a file to the target file.
 */
void
do_copy(void *arg) {
	struct cp_args *carg = (struct cp_args *)arg;
	int from_fd, to_fd, rv;
	size_t rbytes, wbytes, sz;
	char *segment;
	uint64_t bytes_to_copy;

	carg->rv = 0;
	from_fd = open(carg->fromf, O_RDONLY);
	if (from_fd == -1) {
		fprintf(stderr, "Failed to open %s: %s\n", carg->fromf,
		    strerror(errno));
		carg->rv = 1;
		return;
	}

	to_fd = open(carg->tof, O_WRONLY | O_CREAT,
	    S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
	if (to_fd == -1) {
		fprintf(stderr, "Failed to open %s: %s\n", carg->tof,
		    strerror(errno));
		(void) close(from_fd);
		carg->rv = 1;
		return;
	}

	if (lseek(from_fd, carg->pos, SEEK_SET) == -1) {
		fprintf(stderr, "Seek failed on %s: %s\n", carg->fromf,
		    strerror(errno));
		(void) close(from_fd);
		(void) close(to_fd);
		carg->rv = 1;
		return;
	}

	if (lseek(to_fd, carg->pos, SEEK_SET) == -1) {
		fprintf(stderr, "Seek failed on %s: %s\n", carg->tof,
		    strerror(errno));
		(void) close(from_fd);
		(void) close(to_fd);
		carg->rv = 1;
		return;
	}

	segment = (char *)malloc(SEGSIZE);
	if (segment == NULL) {
		fprintf(stderr, "Memory allocation failure.\n");
		(void) close(from_fd);
		(void) close(to_fd);
		carg->rv = 1;
		return;
	}

	rv = 0;
	rbytes = wbytes = 0;
	bytes_to_copy = carg->sz;
	for (;;) {
		if (errorflag)
			break;

		sz = bytes_to_copy > SEGSIZE ? SEGSIZE: bytes_to_copy;
		rbytes = read(from_fd, segment, sz);
		if (rbytes <= 0)
			break;

		wbytes = write(to_fd, segment, rbytes);
		if (wbytes != rbytes) {
			fprintf(stderr, "Segment %d write failed: %s\n", carg->cnum,
			    strerror(errno));
			errorflag = 1;
			break;
		}

		if (bytes_to_copy <= 0)
			break;
	}

	(void) close(from_fd);
	(void) close(to_fd);
	free(segment);
}

int
main(int argc, char *argv[]) {
	int from_fd, to_fd, i;
	struct stat statbuf;
	uint64_t span, rem, pos;
	struct cp_args *carg;
	taskq_t *tq;
	int nthreads = 0;
	char *from, *to;

	if (argc < 3) {
		printf("Usage: mcp <from file> <to file>\n\n");
		return (1);
	}

	from = argv[1];  to = argv[2];
	from_fd = open(from, O_RDONLY);
	if (from_fd == -1) {
		fprintf(stderr, "Failed to open %s: %s\n", from,
		    strerror(errno));
		return (1);
	}

	to_fd = open(to, O_WRONLY | O_CREAT | O_TRUNC,
	    S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
	if (to_fd == -1) {
		fprintf(stderr, "Failed to open %s: %s\n", to,
		    strerror(errno));
		(void) close(to_fd);
		return (1);
	}
	(void) close(to_fd);

	if (fstat(from_fd, &statbuf) == -1) {
		fprintf(stderr, "Failed to get attributes for %s: %s\n", from,
		    strerror(errno));
		(void) close(from_fd);
		(void) close(to_fd);
		return (1);
	}
	(void) close(from_fd);

	if (statbuf.st_size == 0) {
		fprintf(stderr, "Nothing to copy!\n");
		return (1);
	}

	/*
	 * Number of copy threads == num cores * 2 upto a max of 16.
	 */
	nthreads = sysconf(_SC_NPROCESSORS_ONLN) * 2;
	if (nthreads > 16)
		nthreads = 16;
	span = statbuf.st_size / nthreads;
	rem = statbuf.st_size % nthreads;
	pos = 0;

	tq = taskq_create("copy_taskg", nthreads, minclsyspri, 4, nthreads+2,
	    TASKQ_DYNAMIC | TASKQ_PREPOPULATE);

	for (i = 0; i < nthreads; i++) {
		carg = (struct cp_args *)malloc(sizeof (struct cp_args));
		carg->fromf = from;
		carg->tof = to;
		carg->pos = pos;
		if (i == nthreads - 1)
			carg->sz = span + rem;
		else
			carg->sz = span;

		if (taskq_dispatch(tq, do_copy, (void *)carg, TQ_SLEEP) == 0) {
			fprintf(stderr, "taskq_dispatch failed.\n");
			taskq_wait(tq);
			return (1);
		}
	}

	taskq_wait(tq);
	return (0);
}

