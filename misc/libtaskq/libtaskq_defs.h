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
 * Copyright 2010 Moinak Ghosh.
 */

#ifndef _LIBTASKQ_DEFS_H
#define _LIBTASKQ_DEFS_H

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Externally visible task queue interfaces.
 */
typedef struct taskq taskq_t;
typedef uintptr_t taskqid_t;
typedef void (task_func_t)(void *);

#define minclsyspri	60
#define maxclsyspri	99

extern taskq_t *system_taskq;

#define TASKQ_PREPOPULATE	0x0001
#define TASKQ_CPR_SAFE		0x0002	/* Use CPR safe protocol */
#define TASKQ_DYNAMIC		0x0004	/* Use dynamic thread scheduling */

#define TQ_SLEEP	0x0		/* Can block for memory */
#define TQ_NOSLEEP	0x01		/* cannot block for memory; may fail */
#define TQ_NOQUEUE	0x02		/* Do not enqueue if can't dispatch */

#ifdef __cplusplus
}
#endif

#endif /* _LIBTASKQ_DEFS_H */

