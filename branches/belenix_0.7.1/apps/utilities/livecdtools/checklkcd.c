/*
 * This file is derived from parts of libklib.
 * libklib is a library which provides access to Linux system kernel dumps.
 *
 * libklib Copyright notice
 * Created by Silicon Graphics, Inc.
 * Contributions by IBM, NEC, and others
 *
 * Copyright (C) 1999 - 2002, 2004 Silicon Graphics, Inc. All rights reserved.
 * Copyright (C) 2001, 2002 IBM Deutschland Entwicklung GmbH, IBM Corporation
 * Copyright 2000 Junichi Nomura, NEC Solutions <j-nomura@ce.jp.nec.com>
 *
 * This code is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser Public License as published by
 * the Free Software Foundation; either version 2.1 of the License, or
 * (at your option) any later version. See the file COPYING for more
 * information.
 */
/*
 * Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
 * Use is subject to license terms.
 */

#include "checklkcd.h"

static kl_dump_header_t kl_dump_header;
off_t dump_header_offset = 0;
void *G_dump_header = NULL;
void *G_dump_header_asm = NULL;

static unsigned int page_shift_bits = 12; /* Bits to shift for 4k PAGE_SIZE */
static unsigned long KL_DUMP_BUFFER_SIZE = (64*1024);  /* initialised to 64k */
static unsigned long KL_DUMP_HEADER_SIZE = (64*1024);
static int verbose = 0;

uint16_t
kl_get_swap_uint16(void *ptr)
{
	uint16_t t, rawval;

	memcpy(&rawval, ptr, 2);

	t =      (rawval << 8) & 0xff00;
	t = t | ((rawval >> 8) & 0x00ff);

	return t;
}

uint32_t
kl_get_swap_uint32(void *ptr)
{
	uint32_t t, rawval;

	memcpy(&rawval, ptr, 4);

	t =      (rawval << 24) & 0xff000000;
	t = t | ((rawval <<  8) & 0x00ff0000);
	t = t | ((rawval >>  8) & 0x0000ff00);
	t = t | ((rawval >> 24) & 0x000000ff);

	return t;
}

uint64_t
kl_get_swap_uint64(void *ptr)
{
	uint32_t l, h;
	uint64_t rawval;

	memcpy(&rawval, ptr, 8);

	h =      ((uint32_t)(rawval) << 24) & 0xff000000;
	h = h | (((uint32_t)(rawval) <<  8) & 0x00ff0000);
	h = h | (((uint32_t)(rawval) >>  8) & 0x0000ff00);
	h = h | (((uint32_t)(rawval) >> 24) & 0x000000ff);

	l =      ((rawval >> 32) << 24) & 0xff000000;
	l = l | (((rawval >> 32) <<  8) & 0x00ff0000);
	l = l | (((rawval >> 32) >>  8) & 0x0000ff00);
	l = l | (((rawval >> 32) >> 24) & 0x000000ff);

	return (uint64_t) h << 32 | (uint64_t) l;
}

/* 
 * kl_swap_dump_header_s390sa() - Byte swap all members of s390sa header
 */
void 
kl_swap_dump_header_s390sa(kl_dump_header_s390sa_t* dh)
{
	dh->magic_number = kl_get_swap_uint64(&dh->magic_number);
	dh->version	 = kl_get_swap_uint32(&dh->version);
	dh->header_size  = kl_get_swap_uint32(&dh->header_size);
	dh->dump_level	 = kl_get_swap_uint32(&dh->dump_level);
	dh->page_size	 = kl_get_swap_uint32(&dh->page_size);
	dh->memory_size  = kl_get_swap_uint64(&dh->memory_size);
	dh->memory_start = kl_get_swap_uint64(&dh->memory_start);
	dh->memory_end	 = kl_get_swap_uint64(&dh->memory_end);
	dh->num_pages	 = kl_get_swap_uint32(&dh->num_pages);
	dh->tod		 = kl_get_swap_uint64(&dh->tod);
	dh->cpu_id	 = kl_get_swap_uint64(&dh->cpu_id);
	dh->arch_id	 = kl_get_swap_uint32(&dh->arch_id);
	dh->build_arch_id =  kl_get_swap_uint32(&dh->build_arch_id);
}

static int 
_kl_check_s390sa_endmarker(int fh, kl_dump_header_s390sa_t* dh,
			   int swap)
{
	char em[16];
	uint64_t mem_size = dh->memory_size;
	uint64_t tod_em;
	int rc = 0;

	/* seek to endmarker (memsize + size of dump header) */
	if (lseek(fh, mem_size + 4096, SEEK_SET) < 0) {
		if (verbose)
			fprintf(stderr,
				"lseek failed! Perhaps dump not complete?\n");
		rc = 1; goto out;
	}
	/* read endmarker */
	if (read(fh, &em,sizeof(em)) != sizeof(em)) {
		if (verbose)
			fprintf(stderr,
				"read failed! Perhaps dump not complete?\n");
		rc = 1; goto out;
	}
	/* check endmarker */
	if (memcmp(em,"DUMP_END",8) != 0) {
		if (verbose)
			fprintf(stderr,
				"Dump not valid! No Endmarker found!\n");
		rc = 1; goto out;
	} 
	tod_em = *((uint64_t*)(em + 8));
	if (swap)
		tod_em = kl_get_swap_uint64(&tod_em);

	if (tod_em <= dh->tod) {
		if (verbose)
			fprintf(stderr,
				"Dump not vaild! Endmarker time <= dump time!\n");
		rc = 1; goto out;
	}
	if (verbose)
		fprintf(stderr, "End Marker found! Dump is valid!\n");
out:
	return rc;
}

int
kl_valid_dump_header(uint64_t magic, uint64_t magic_swap, int fh)
{
	kl_dump_header_t dh;
	kl_dump_header_s390sa_t s390_dh;
	uint64_t magic_number;
	uint32_t dump_header_size;

	switch (magic) {
		case KL_DUMP_MAGIC_S390SA:
			lseek(fh,  0, SEEK_SET);
			if (read(fh, (char *)&s390_dh,
                		sizeof(s390_dh)) != sizeof(s390_dh)) {
				fprintf(stderr, "Cannot read() dump header: %s\n",
					strerror(errno));
				return (1);
			}
			return (_kl_check_s390sa_endmarker(fh, &s390_dh, 0));

		case KL_DUMP_MAGIC_LIVE:
			return (0);

		default:
			if (lseek(fh, KL_DUMP_HEADER_OFFSET + 
				offsetof (struct kl_dump_header_s,
				magic_number), SEEK_SET) < 0) {
				fprintf(stderr, "lseek() on dumpdev failed, %s\n",
					strerror(errno));
				return (1);
			}
			if (read(fh, &magic_number, sizeof(magic_number)) != 
				sizeof(magic_number)) {
				fprintf(stderr, "read() on dumpdev failed, %s\n",
					strerror(errno));
				return (1);
			}
			magic_number = kl_get_swap_uint64(&magic_number);

			if (magic_number != KL_DUMP_MAGIC_NUMBER) {
				fprintf(stderr, "Dump header invalid\n");
				return (1);
			}

			if (lseek(fh, KL_DUMP_HEADER_OFFSET +
				offsetof(struct kl_dump_header_s, header_size),
				SEEK_SET) < 0) {
				fprintf(stderr, "lseek() on dumpdev failed, %s\n",
					strerror(errno));
				return (1);
			}
			if (read(fh, &dump_header_size, sizeof(dump_header_size)) 
				!= sizeof(dump_header_size)) {
				fprintf(stderr, "read() on dumpdev failed, %s\n",
					strerror(errno));
				return (1);
			}
			dump_header_size = kl_get_swap_uint64(&dump_header_size);

			if (dump_header_size > sizeof(dh)) {
				fprintf(stderr, "Invalid dump header\n");
				return (1);
			}

		return(0);
	}

	switch (magic_swap) {
		case KL_DUMP_MAGIC_S390SA:
			lseek(fh,  0, SEEK_SET);
			if (read(fh, (char *)&s390_dh,
                		sizeof(s390_dh)) != sizeof(s390_dh)) {
				fprintf(stderr, "Cannot read() dump header: %s\n",
					strerror(errno));
				return (1);
			}
			kl_swap_dump_header_s390sa(&s390_dh);
			return(_kl_check_s390sa_endmarker(fh, &s390_dh, 1));

		case KL_DUMP_MAGIC_LIVE:
			return (0);

		default:
			if (lseek(fh, KL_DUMP_HEADER_OFFSET + 
				offsetof(struct kl_dump_header_s,
				magic_number), SEEK_SET) < 0) {
				fprintf(stderr, "lseek() on dumpdev failed, %s\n",
					strerror(errno));
				return (1);
			}
			if (read(fh, &magic_number, sizeof(magic_number)) != 
				sizeof(magic_number)) {
				fprintf(stderr, "read() on dumpdev failed, %s\n",
					strerror(errno));
				return (1);
			}
			

			if (magic_number != KL_DUMP_MAGIC_NUMBER) {
				fprintf(stderr, "Dump header invalid\n");
				return (1);
			}

			if (lseek(fh, KL_DUMP_HEADER_OFFSET +
				offsetof(struct kl_dump_header_s, header_size),
				SEEK_SET) < 0) {
				fprintf(stderr, "lseek() on dumpdev failed, %s\n",
					strerror(errno));
				return (1);
			}

			if (read(fh, &dump_header_size, sizeof(dump_header_size)) 
				!= sizeof(dump_header_size)) {
				fprintf(stderr, "read() on dumpdev failed, %s\n",
					strerror(errno));
				return (1);
			}
			if (dump_header_size > sizeof(dh)) {
				fprintf(stderr, "Invalid dump header\n");
				return (1);
			}
		return(0);
	}

	if (verbose)
		fprintf(stderr, "Invalid magic number. No dump header present.\n");
	return(1);
}

int
kl_read_dump_header(const char *dump) {
	int fh;
	uint64_t magic, magic_swap;
	int rc = 0;

	fh = open(dump, O_RDONLY);
	if (fh == -1) {
		if (verbose)
			fprintf(stderr, "open(\"%s\"): %s\n",
				dump, strerror(errno));
		rc = 1; goto out;
	}

	if (read(fh, (void*)&magic, sizeof (magic)) != sizeof (magic)) {
		fprintf(stderr, "Error: Read failed for %s: %s\n",
				dump, strerror(errno));
		rc = 1; goto out;
	}
	magic_swap = kl_get_swap_uint64(&magic);

	rc = kl_valid_dump_header(magic, magic_swap, fh);

out:
	return (rc);
}

int
main(int argc, char *argv[]) {
	int c;
	char *dumpfile = NULL;

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
		fprintf(stderr, "Usage: checklkcd -f <dumpfile> [-v]\n");
		return (1);
	}

	return (!kl_read_dump_header(dumpfile));
}

