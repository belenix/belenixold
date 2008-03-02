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

#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#include <stddef.h>


/* Declarations
 */
#ifdef MAX
#undef MAX
#endif
#define MAX(a, b)  (((a) > (b)) ? (a) : (b))
#define LKCD_DH_4_2_VERSION 8

#define KL_UTS_LEN 65     /* do not change ... */


/* We have to distinc between HOST_ARCH_* and DUMP_ARCH_*. These two classes of
 * macros are used througout the code for conditional compilation.
 * Additional we have following macros for comparison and switch statements.
 */
#define KL_ARCH_UNKNOWN          0
#define KL_ARCH_ALPHA            1
#define KL_ARCH_ARM              2
#define KL_ARCH_I386             3
#define KL_ARCH_IA64             4
#define KL_ARCH_M68K             5
#define KL_ARCH_MIPS             6
#define KL_ARCH_MIPS64           7
#define KL_ARCH_PPC              8
#define KL_ARCH_S390             9
#define KL_ARCH_SH              10
#define KL_ARCH_SPARK           11
#define KL_ARCH_SPARK64         12
#define KL_ARCH_S390X           13
#define KL_ARCH_PPC64           14
#define KL_ARCH_X86_64          15
#define KL_ARCH_IA64_SN2        16
#define KL_ARCH_IA64_DIG        17
#define KL_ARCH_IA64_HPSIM      18
#define KL_ARCH_IA64_HPZX1      19

#define KL_LIVE_SYSTEM        1000

/* for endianess of dump and host arch
 */
#define KL_UNKNOWN_ENDIAN  0x00
#define KL_LITTLE_ENDIAN   0x01
#define KL_BIG_ENDIAN      0x02

/* macros for easier access to dump specific values */
#define KL_ARCH                 KLP->dump->arch.arch
#define KL_PTRSZ                KLP->dump->arch.ptrsz
#define KL_NBPW                 (KL_PTRSZ/8)
#define KL_BYTE_ORDER           KLP->dump->arch.byteorder
#define KL_PAGE_SHIFT           KLP->dump->arch.pageshift
#define KL_PAGE_SIZE            KLP->dump->arch.pagesize
#define KL_PAGE_MASK            KLP->dump->arch.pagemask
#define KL_PAGE_OFFSET          KLP->dump->arch.pageoffset
#define KL_STACK_OFFSET         KLP->dump->arch.kstacksize
#define IS_BIG_ENDIAN()         (KL_BYTE_ORDER == KL_BIG_ENDIAN)
#define IS_LITTLE_ENDIAN()      (KL_BYTE_ORDER == KL_LITTLE_ENDIAN)
#define KL_LINUX_RELEASE        KLP->dump->mem.linux_release
#define KL_KERNEL_FLAGS         KLP->dump->mem.kernel_flags

/* macros to access input files */
#define KL_MAP_FILE       KLP->dump->map
#define KL_DUMP_FILE      KLP->dump->dump
#define KL_KERNTYPES_FILE KLP->kerntypes

/* Generic dump header structure (the first three members of
 * dump_header and dump_header_asm are the same).
 */
typedef struct generic_dump_header_s {
        uint64_t        magic_number;
        uint32_t        version;
        uint32_t        header_size;
} generic_dump_header_t;

/* Some macros for making it easier to access the generic header
 * information in a dump_header or dump_header_asm stuct.
 */
#define DHP(dh)                 ((generic_dump_header_t*)(dh))
#define DH_MAGIC(dh)            DHP(dh)->magic_number
#define DH_VERSION(dh)          DHP(dh)->version
#define DH_HEADER_SIZE(dh)      DHP(dh)->header_size

/* header definitions for dumps from s390 standalone dump tools */
#define KL_DUMP_MAGIC_S390SA     0xa8190173618f23fdULL /* s390sa magic number */
#define KL_DUMP_HEADER_SZ_S390SA 4096

/* standard header definitions */
#define KL_DUMP_MAGIC_NUMBER  0xa8190173618f23edULL  /* dump magic number  */
#define KL_DUMP_MAGIC_LIVE    0xa8190173618f23cdULL  /* live magic number  */
#define KL_DUMP_MAGIC_ASM     0xdeaddeadULL  /* generic arch magic number  */
#define KL_DUMP_VERSION_NUMBER 0x8      /* dump version number             */
#define KL_DUMP_PANIC_LEN      0x100    /* dump panic string length        */

/* dump levels - type specific stuff added later -- add as necessary */
#define KL_DUMP_LEVEL_NONE        0x0   /* no dumping at all -- just bail   */
#define KL_DUMP_LEVEL_HEADER      0x1   /* kernel dump header only          */
#define KL_DUMP_LEVEL_KERN        0x2   /* dump header and kernel pages     */
#define KL_DUMP_LEVEL_USED        0x4   /* dump header, kernel/user pages   */
#define KL_DUMP_LEVEL_ALL_RAM     0x8   /* dump header, all RAM pages       */
#define KL_DUMP_LEVEL_ALL         0x10  /* dump all memory RAM and firmware */

/* Dump header offset changed from 4k to 64k to support multiple page sizes */
#define KL_DUMP_HEADER_OFFSET  (1ULL << 16)

typedef struct kl_dump_header_s {
        uint64_t magic_number; /* dump magic number, unique to verify dump */
        uint32_t version;      /* version number of this dump */
        uint32_t header_size;  /* size of this header */
        uint32_t dump_level;   /* level of this dump */
        /* FIXME: rename page_size to dump_page_size
         * The size of a hardware/physical memory page (DUMP_PAGE_SIZE).
         * NB: Not the configurable system page (PAGE_SIZE) (4K, 8K, 16K, etc.)
         */
/*      uint32_t             dh_dump_page_size; */
        uint32_t page_size;    /* page size (e.g. 4K, 8K, 16K, etc.) */
        uint64_t memory_size;  /* size of entire physical memory */
        uint64_t memory_start; /* start of physical memory */
        uint64_t memory_end;      /* end of physical memory */
#if DUMP_DEBUG >= 6
        uint64_t num_bytes; /* number of bytes in this dump */
#endif
        /* the number of dump pages in this dump specifically */
        uint32_t num_dump_pages;
        char panic_string[KL_DUMP_PANIC_LEN]; /* panic string, if available*/

        /* timeval depends on machine, two long values */
        struct {uint64_t tv_sec;
                uint64_t tv_usec;
        } time; /* the time of the system crash */

        /* the NEW utsname (uname) information -- in character form */
        /* we do this so we don't have to include utsname.h         */
        /* plus it helps us be more architecture independent        */
        char utsname_sysname[KL_UTS_LEN];
        char utsname_nodename[KL_UTS_LEN];
        char utsname_release[KL_UTS_LEN];
        char utsname_version[KL_UTS_LEN];
        char utsname_machine[KL_UTS_LEN];
        char utsname_domainname[KL_UTS_LEN];

        uint64_t current_task; /* fixme: better use uint64_t here */
        uint32_t dump_compress; /* compression type used in this dump */
        uint32_t dump_flags;       /* any additional flags */
        uint32_t dump_device;   /* any additional flags */
        uint64_t dump_buffer_size; /* version >= 9 */
} __attribute__((packed)) kl_dump_header_t;

/* This is the header used by the s390 standalone dump tools
 */
typedef struct kl_dump_header_s390sa_s {
        uint64_t magic_number; /* magic number for this dump (unique)*/
        uint32_t version;      /* version number of this dump */
        uint32_t header_size;  /* size of this header */
        uint32_t dump_level;   /* the level of this dump (just a header?) */
        uint32_t page_size;    /* page size of dumped Linux (4K,8K,16K etc.) */
        uint64_t memory_size;  /* the size of all physical memory */
        uint64_t memory_start; /* the start of physical memory */
        uint64_t memory_end;   /* the end of physical memory */
        uint32_t num_pages;    /* number of pages in this dump */
        uint32_t pad;          /* ensure 8 byte alignment for tod and cpu_id */
        uint64_t tod;          /* the time of the dump generation */
        uint64_t cpu_id;       /* cpu id */
        uint32_t arch_id;
        uint32_t build_arch_id;
#define KL_DH_ARCH_ID_S390X 2
#define KL_DH_ARCH_ID_S390  1
} __attribute__((packed))  kl_dump_header_s390sa_t;

/* CORE_TYPE indicating type of dump
 */
typedef enum {
        dev_kmem,   /* image of /dev/kmem, a running kernel */
        reg_core,   /* Regular (uncompressed) core file */
        s390_core,  /* s390 core file */
        cmp_core    /* compressed core file */
} CORE_TYPE;

