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

#ifndef _LIBTASKQ_H
#define _LIBTASKQ_H

#ifdef __cplusplus
extern "C" {
#endif

#include <libtaskq_defs.h>

/*
 * Externally visible task queue interfaces.
 */
extern taskq_t  *taskq_create(const char *, int, pri_t, int, int, uint_t);
extern taskqid_t taskq_dispatch(taskq_t *, task_func_t, void *, uint_t);
extern void     taskq_destroy(taskq_t *);
extern void     taskq_wait(taskq_t *);
extern int      taskq_member(taskq_t *, void *);
extern void     system_taskq_init(void);

#ifdef __cplusplus
}
#endif

#endif /* _LIBTASKQ_H */

