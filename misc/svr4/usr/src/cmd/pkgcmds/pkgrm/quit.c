/*
 * CDDL HEADER START
 *
 * The contents of this file are subject to the terms of the
 * Common Development and Distribution License (the "License").
 * You may not use this file except in compliance with the License.
 *
 * You can obtain a copy of the license at src/OPENSOLARIS.LICENSE
 * or http://www.opensolaris.org/os/licensing.
 * See the License for the specific language governing permissions
 * and limitations under the License.
 *
 * When distributing Covered Code, include this CDDL HEADER in each
 * file and include the License file at src/OPENSOLARIS.LICENSE.
 * If applicable, add the following below this CDDL HEADER, with the
 * fields enclosed by brackets "[]" replaced with your own identifying
 * information: Portions Copyright [yyyy] [name of copyright owner]
 *
 * CDDL HEADER END
 */

/*
 * Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
 * Use is subject to license terms.
 */

/* Copyright (c) 1984, 1986, 1987, 1988, 1989 AT&T */
/* All Rights Reserved */

#pragma ident	"@(#)quit.c	1.16	07/10/03 SMI"

#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <locale.h>
#include <libintl.h>
#include <pkgdev.h>
#include <pkglib.h>
#include <spmizones_api.h>
#include <libadm.h>
#include <libinst.h>
#include <messages.h>
#include "quit.h"

/*
 * imported global variables
 */

/* imported from main.c */

extern struct pkgdev pkgdev;	/* holds info about the installation device */

extern int	npkgs;		/* the number of packages yet to be installed */
extern int	admnflag;	/* != 0 if any pkgop admin setting failed (4) */
extern int	doreboot;	/* != 0 if reboot required after installation */
extern int	failflag;	/* != 0 if fatal error has occurred (1) */
extern int	intrflag;	/* != 0 if user selected quit (3) */
extern int	ireboot;	/* != 0 if immediate reboot required */
extern int	nullflag;	/* != 0 if admin interaction required (5) */
extern int	warnflag;	/* != 0 if non-fatal error has occurred (2) */

/*
 * forward declarations
 */

static ckreturnFunc_t	*ckreturnFunc = (ckreturnFunc_t *)NULL;
static intfRelocFunc_t	*intfRelocFunc = (intfRelocFunc_t *)NULL;
static char		*zoneTempDir = (char *)NULL;
static void		trap(int signo);
static zoneList_t	zoneList = (zoneList_t)NULL;
static int		trapEntered = 0;

/*
 * exported functions
 */

void		quit(int retcode);
void		quitSetCkreturnFunc(ckreturnFunc_t *a_ckreturnFunc);
void		quitSetZoneName(char *a_zoneName);
void		quitSetZoneTmpdir(char *z_zoneTempDir);
void		quitSetZonelist(zoneList_t a_zlst);
sighdlrFunc_t	*quitGetTrapHandler(void);

/*
 * *****************************************************************************
 * global external (public) functions
 * *****************************************************************************
 */

/*
 * Name:	quitGetTrapHandler
 * Description:	return address of this modules "signal trap" handler
 * Arguments:	void
 * Returns:	sighdlrFunc_t
 *			The address of the trap handler that can be passed to
 *			the signal() type system calls
 */

sighdlrFunc_t *
quitGetTrapHandler()
{
	return (&trap);
}

/*
 * Name:	quitSetIntfReloc
 * Description:	set the "intf_reloc" interface to run when quit() is called
 * Arguments:	a_intfReloc - pointer to function to call when quit() is called
 * Returns:	void
 * NOTE:	When quit() is called, if an "intf_reloc" function is set, quit
 *		will call that function to perform whatever operations it needs
 *		to perform - typically this is needed to run "intf_reloc" when
 *		pre-SVR4 packages have been removed
 */

void
quitSetIntfReloc(intfRelocFunc_t *a_intfReloc)
{
	intfRelocFunc = a_intfReloc;
}

/*
 * Name:	quitSetCkreturnFunc
 * Description:	set the ckreturn() interface to call when quit() is called
 * Arguments:	a_ckreturnFunc - pointer to function to call when quit() is
 *			called
 * Returns:	void
 * NOTE:	When quit() is called if a "ckreturnfunc" is set, then the first
 *		action quit() takes is to call the "ckreturnfunc" specified with
 *		the value passed to quit as the first argument. Quit will then
 *		set the final return code to be used when exit() is called based
 *		on the contents of these global variables:
 *		 - admnflag - != 0 if any pkgop admin setting failed (4)
 *		 - doreboot - != 0 if reboot required after installation
 *		 - failflag - != 0 if fatal error has occurred (1)
 *		 - intrflag - != 0 if user selected quit (3)
 *		 - ireboot - != 0 if immediate reboot required
 *		 - nullflag - != 0 if admin interaction required (5)
 *		 - warnflag - != 0 if non-fatal error has occurred (2)
 */

void
quitSetCkreturnFunc(ckreturnFunc_t *a_ckreturnFunc)
{
	ckreturnFunc = a_ckreturnFunc;
}

/*
 * Name:	quitSetZonelist
 * Description:	set the list of zones that are "locked" so that the zones can
 *		be unlocked if quit() is called to exit
 * Arguments:	a_zlst - list of zones that are "locked"
 * Returns:	void
 * NOTE:	When quit() is called, if this list is set, then z_unlock_zones
 *		is called to unlock all of the zones in the list. If this list
 *		is NOT set, then z_unlock_this_zone is called to unlock this
 *		zone.
 */

void
quitSetZonelist(zoneList_t a_zlst)
{
	zoneList = a_zlst;
}

/*
 * Name:	quitSetZoneName
 * Description:	set the zone name the program is running in
 * Arguments:	a_zoneName - pointer to string representing the name of the zone
 *			that the program is running in
 * Returns:	void
 */

/* ARGSUSED */
void
quitSetZoneName(char *a_zoneName)
{
}

/*
 * Name:	quitSetZoneTmpdir
 * Description:	set the path to the "zone temporary directory" in use
 * Arguments:	a_zoneTempDir - pointer to string representing the full path to
 *			the temporary directory used to hold files used during
 *			zone operations
 * Returns:	void
 * NOTE:	If a zone temporary directory is set when quit() is called, the
 *		directory is recursively removed before quit() calls exit
 */

void
quitSetZoneTmpdir(char *a_zoneTempDir)
{
	zoneTempDir = a_zoneTempDir;
}

/*
 * Name:	quit
 * Description:	cleanup and exit
 * Arguments:	a_retcode - the code to use to determine final exit status;
 *			if this is NOT "99" and if a "ckreturnFunc" is
 *			set, then that function is called with a_retcode
 *			to set the final exit status.
 *		Valid values are:
 *		0 - success
 *		1 - package operation failed (fatal error)
 *		2 - non-fatal error (warning)
 *		3 - user selected quit (operation interrupted)
 *		4 - admin settings prevented operation
 *		5 - interaction required and -n (non-interactive) specified
 *		"10" is added to indicate "immediate reboot required"
 *		"20" is be added to indicate "reboot after install required"
 *		99 - do not interpret the code - just exit "99"
 * Returns:	<<this function does not return - calls exit()>>
 */

void
quit(int retcode)
{
	/* disable interrupts */

	(void) signal(SIGINT, SIG_IGN);
	(void) signal(SIGHUP, SIG_IGN);

	if (!restore_local_fs) {
		progerr(ERR_CANNOT_RESTORE_LOCAL_FS);
	}

	/* process return code if not quit(99) */

	if (retcode != 99) {
		if (ckreturnFunc != (ckreturnFunc_t *)NULL) {
			(ckreturnFunc)(retcode);
		}
		if (failflag) {
			retcode = 1;
		} else if (warnflag) {
			retcode = 2;
		} else if (intrflag) {
			retcode = 3;
		} else if (admnflag) {
			retcode = 4;
		} else if (nullflag) {
			retcode = 5;
		} else {
			retcode = 0;
		}
		if (ireboot) {
			retcode += 20;
		}
		if (doreboot) {
			retcode += 10;
		}
	}

	if (doreboot || ireboot) {
		ptext(stderr, gettext(MSG_REBOOT));
	}

	if (pkgdev.mount) {
		(void) chdir("/");
		(void) pkgumount(&pkgdev);
	}

	/* if set remove zone temporary directory */

	if (zoneTempDir != (char *)NULL) {
		echoDebug(DBG_REMOVING_ZONE_TMPDIR, zoneTempDir);
		(void) rrmdir(zoneTempDir);
		zoneTempDir = (char *)NULL;
	}

	/*
	 * issue final exit message depending on number of packages left
	 * to process
	 */

	if (npkgs == 1) {
		echo(MSG_1_PKG_NOT_PROCESSED);
	} else if (npkgs) {
		echo(MSG_N_PKGS_NOT_PROCESSED, npkgs);
	}

	/* call intf_reloc function if registered */

	if (intfRelocFunc != (intfRelocFunc_t *)NULL) {
		(intfRelocFunc)();
	}

	/* if a zone list exists, unlock all zones */

	if (zoneList != (zoneList_t)NULL) {
		(void) z_unlock_zones(zoneList, ZLOCKS_ALL);
	} else {
		(void) z_unlock_this_zone(ZLOCKS_ALL);
	}

	/* final exit debugging message */

	echoDebug(DBG_EXIT_WITH_CODE, retcode);

	exit(retcode);
	/* NOTREACHED */
}

/*
 * *****************************************************************************
 * static internal (private) functions
 * *****************************************************************************
 */

/*
 * Name:	trap
 * Description:	signal handler connected via quitGetTrapHandler()
 * Arguments:	signo - [RO, *RO] - (int)
 *			Integer representing the signal that caused the trap
 *			to this function to occur
 * Returns:	<< NONE >>
 * NOTE:	This function exits the program after doing mandatory cleanup.
 * NOTE:	Even though quit() should NOT return, there is a call to _exit()
 *		put after each call to quit() just in case quit() ever returned
 *		by mistake.
 */

static void
trap(int signo)
{
	/* prevent reentrance */

	if (trapEntered++ != 0) {
		return;
	}

	if ((signo == SIGINT) || (signo == SIGHUP)) {
		quit(3);
		_exit(3);
	}
	quit(1);
	_exit(1);
}
