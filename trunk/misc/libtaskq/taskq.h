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
 * Copyright 2009 Sun Microsystems, Inc.  All rights reserved.
 * Use is subject to license terms.
 */

#ifndef _SYS_TASKQ_H
#define	_SYS_TASKQ_H

#ifdef	__cplusplus
extern "C" {
#endif

#define	_SYS_MUTEX_H
#define	_SYS_RWLOCK_H
#define	_SYS_CONDVAR_H
#define	_SYS_SYSTM_H
#define	_SYS_DEBUG_H
#define	_SYS_T_LOCK_H

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdarg.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <strings.h>
#include <synch.h>
#include <thread.h>
#include <assert.h>
#include <alloca.h>
#include <umem.h>
#include <limits.h>
#include <atomic.h>
#include <dirent.h>
#include <time.h>
#include <sys/note.h>
#include <sys/types.h>
/*#include <sys/cred.h>*/
/*#include <sys/sysmacros.h>*/
/*#include <sys/bitmap.h>*/
/*#include <sys/resource.h>*/
#include <sys/byteorder.h>
#include <sys/list.h>
#include "libtaskq_defs.h"

/*
 * Debugging
 */

/*
 * Note that we are not using the debugging levels.
 */

#define	CE_CONT		0	/* continuation		*/
#define	CE_NOTE		1	/* notice		*/
#define	CE_WARN		2	/* warning		*/
#define	CE_PANIC	3	/* panic		*/
#define	CE_IGNORE	4	/* print nothing	*/

/*
 * TaskQ debugging
 */

#ifdef TASKQ_DEBUG
extern void dprintf_setup(int *argc, char **argv);
#define dprintf(fmt, ...) __dprintf(fmt, __VA_ARGS__)
#else
#define dprintf(fmt, ...)
#endif /* TASKQ_DEBUG */

extern void cmn_err(int, const char *, ...);
extern void vcmn_err(int, const char *, __va_list);
extern void panic(const char *, ...);
extern void vpanic(const char *, __va_list);

#define	fm_panic	panic

/* This definition is copied from assert.h. */
#if defined(__STDC__)
#if __STDC_VERSION__ - 0 >= 199901L
#define	verify(EX) (void)((EX) || \
	(__assert_c99(#EX, __FILE__, __LINE__, __func__), 0))
#else
#define	verify(EX) (void)((EX) || (__assert(#EX, __FILE__, __LINE__), 0))
#endif /* __STDC_VERSION__ - 0 >= 199901L */
#else
#define	verify(EX) (void)((EX) || (_assert("EX", __FILE__, __LINE__), 0))
#endif	/* __STDC__ */


#define	VERIFY	verify
#define	ASSERT	assert

extern void __assert(const char *, const char *, int);

#ifdef lint
#define	VERIFY3_IMPL(x, y, z, t)	if (x == z) ((void)0)
#else
/* BEGIN CSTYLED */
#define	VERIFY3_IMPL(LEFT, OP, RIGHT, TYPE) do { \
	const TYPE __left = (TYPE)(LEFT); \
	const TYPE __right = (TYPE)(RIGHT); \
	if (!(__left OP __right)) { \
		char *__buf = alloca(256); \
		(void) snprintf(__buf, 256, "%s %s %s (0x%llx %s 0x%llx)", \
			#LEFT, #OP, #RIGHT, \
			(u_longlong_t)__left, #OP, (u_longlong_t)__right); \
		__assert(__buf, __FILE__, __LINE__); \
	} \
_NOTE(CONSTCOND) } while (0)
/* END CSTYLED */
#endif /* lint */

#define	VERIFY3S(x, y, z)	VERIFY3_IMPL(x, y, z, int64_t)
#define	VERIFY3U(x, y, z)	VERIFY3_IMPL(x, y, z, uint64_t)
#define	VERIFY3P(x, y, z)	VERIFY3_IMPL(x, y, z, uintptr_t)

#ifdef NDEBUG
#define	ASSERT3S(x, y, z)	((void)0)
#define	ASSERT3U(x, y, z)	((void)0)
#define	ASSERT3P(x, y, z)	((void)0)
#else
#define	ASSERT3S(x, y, z)	VERIFY3S(x, y, z)
#define	ASSERT3U(x, y, z)	VERIFY3U(x, y, z)
#define	ASSERT3P(x, y, z)	VERIFY3P(x, y, z)
#endif

/*
 * Threads
 */
#define	curthread	((void *)(uintptr_t)thr_self())

typedef struct kthread kthread_t;

#define	thread_create(stk, stksize, func, arg, len, pp, state, pri)	\
	zk_thread_create(func, arg)
#define	thread_exit() thr_exit(NULL)

extern kthread_t *zk_thread_create(void (*func)(), void *arg);

#define	issig(why)	(FALSE)
#define	ISSIG(thr, why)	(FALSE)

/*
 * Mutexes
 */
typedef struct kmutex {
	void		*m_owner;
	boolean_t	initialized;
	mutex_t		m_lock;
} kmutex_t;

#define	MUTEX_DEFAULT	USYNC_THREAD
#undef MUTEX_HELD
#define	MUTEX_HELD(m) _mutex_held(&(m)->m_lock)

/*
 * Argh -- we have to get cheesy here because the kernel and userland
 * have different signatures for the same routine.
 */
extern int _mutex_init(mutex_t *mp, int type, void *arg);
extern int _mutex_destroy(mutex_t *mp);

#define	mutex_init(mp, b, c, d)		zmutex_init((kmutex_t *)(mp))
#define	mutex_destroy(mp)		zmutex_destroy((kmutex_t *)(mp))

extern void zmutex_init(kmutex_t *mp);
extern void zmutex_destroy(kmutex_t *mp);
extern void mutex_enter(kmutex_t *mp);
extern void mutex_exit(kmutex_t *mp);
extern int mutex_tryenter(kmutex_t *mp);
extern void *mutex_owner(kmutex_t *mp);

/*
 * RW locks
 */
typedef struct krwlock {
	void		*rw_owner;
	boolean_t	initialized;
	rwlock_t	rw_lock;
} krwlock_t;

typedef int krw_t;

#define	RW_READER	0
#define	RW_WRITER	1
#define	RW_DEFAULT	USYNC_THREAD

#undef RW_READ_HELD
#define	RW_READ_HELD(x)		_rw_read_held(&(x)->rw_lock)

#undef RW_WRITE_HELD
#define	RW_WRITE_HELD(x)	_rw_write_held(&(x)->rw_lock)

extern void rw_init(krwlock_t *rwlp, char *name, int type, void *arg);
extern void rw_destroy(krwlock_t *rwlp);
extern void rw_enter(krwlock_t *rwlp, krw_t rw);
extern int rw_tryenter(krwlock_t *rwlp, krw_t rw);
extern int rw_tryupgrade(krwlock_t *rwlp);
extern void rw_exit(krwlock_t *rwlp);
#define	rw_downgrade(rwlp) do { } while (0)

/*
 * Condition variables
 */
typedef cond_t kcondvar_t;

#define	CV_DEFAULT	USYNC_THREAD

extern void cv_init(kcondvar_t *cv, char *name, int type, void *arg);
extern void cv_destroy(kcondvar_t *cv);
extern void cv_wait(kcondvar_t *cv, kmutex_t *mp);
extern clock_t cv_timedwait(kcondvar_t *cv, kmutex_t *mp, clock_t abstime);
extern void cv_signal(kcondvar_t *cv);
extern void cv_broadcast(kcondvar_t *cv);

/*
 * Kernel memory
 */
#define	KM_SLEEP		UMEM_NOFAIL
#define	KM_PUSHPAGE		KM_SLEEP
#define	KM_NOSLEEP		UMEM_DEFAULT
#define	KMC_NODEBUG		UMC_NODEBUG
#define	kmem_alloc(_s, _f)	umem_alloc(_s, _f)
#define	kmem_zalloc(_s, _f)	umem_zalloc(_s, _f)
#define	kmem_free(_b, _s)	umem_free(_b, _s)
#define	kmem_cache_create(_a, _b, _c, _d, _e, _f, _g, _h, _i) \
	umem_cache_create(_a, _b, _c, _d, _e, _f, _g, _h, _i)
#define	kmem_cache_destroy(_c)	umem_cache_destroy(_c)
#define	kmem_cache_alloc(_c, _f) umem_cache_alloc(_c, _f)
#define	kmem_cache_free(_c, _b)	umem_cache_free(_c, _b)
#define	kmem_debugging()	0
#define	kmem_cache_reap_now(c)

typedef umem_cache_t kmem_cache_t;

/*
 * Task queues
 */
extern taskq_t	*taskq_create(const char *, int, pri_t, int, int, uint_t);
extern taskqid_t taskq_dispatch(taskq_t *, task_func_t, void *, uint_t);
extern void	taskq_destroy(taskq_t *);
extern void	taskq_wait(taskq_t *);
extern int	taskq_member(taskq_t *, void *);
extern void	system_taskq_init(void);

#define	XVA_MAPSIZE	3
#define	XVA_MAGIC	0x78766174

/*
 * Random stuff
 */
#define	lbolt	(gethrtime() >> 23)
#define	lbolt64	(gethrtime() >> 23)
#define	hz	119	/* frequency when using gethrtime() >> 23 for lbolt */

extern void delay(clock_t ticks);

#define	gethrestime_sec() time(NULL)
#define	max_ncpus	64

extern void libtaskq_init(int);
extern void libtaskq_fini(void);

#ifdef	__cplusplus
}
#endif

#endif	/* _SYS_TASKQ_H */
