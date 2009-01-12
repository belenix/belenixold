/*
 * Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
 * Use is subject to license terms.
 */

#pragma ident	"@(#)handlelocalfs.c	1.1	07/10/03 SMI"

#include <stdlib.h>
#include <unistd.h>
#include <strings.h>
#include <libscf.h>

#define	MAX_TRY	15
static boolean_t fs_temporarily_enabled = B_FALSE;
char svm_core_svcs[] = "system/filesystem/local:default";

/*
 * Name:	enable_local_fs
 * Description: If the SMF service system/filesystem/local:default is not
 *		enabled, then this function enables the service, so that,
 *		all the local filesystems are mounted.
 * Arguments:	None
 * Returns:	B_TRUE on success; B_FALSE on error.
 */
boolean_t
enable_local_fs(void)
{
	char *cur_smf_state;
	int i;
	boolean_t fs_enabled_here = B_FALSE;

	if (fs_temporarily_enabled)  {
		return (B_TRUE);
	}

	if ((cur_smf_state = smf_get_state(svm_core_svcs)) != NULL) {
		if (strcmp(cur_smf_state, SCF_STATE_STRING_DISABLED) == 0) {
			if (smf_enable_instance(svm_core_svcs, SMF_TEMPORARY)
				!= 0) {
				free(cur_smf_state);
				return (B_FALSE);
			}

			fs_enabled_here = B_TRUE;

		} else if (strcmp(cur_smf_state, SCF_STATE_STRING_ONLINE)
				== 0) {
			free(cur_smf_state);
			return (B_TRUE);
		} else if (strcmp(cur_smf_state, SCF_STATE_STRING_OFFLINE)
				!= 0) {
			free(cur_smf_state);
			return (B_FALSE);
		}

		free(cur_smf_state);

	} else {
		return (B_FALSE);
	}

	for (i = 0; i < MAX_TRY; i++) {
		if ((cur_smf_state = smf_get_state(svm_core_svcs)) != NULL) {
			if (strcmp(cur_smf_state, SCF_STATE_STRING_ONLINE)
				== 0) {
				free(cur_smf_state);
				if (fs_enabled_here) {
					fs_temporarily_enabled = B_TRUE;
				}
				return (B_TRUE);
			} else if ((strcmp(cur_smf_state,
				SCF_STATE_STRING_OFFLINE) == 0) ||
		(strcmp(cur_smf_state, SCF_STATE_STRING_DISABLED) == 0)) {
				(void) sleep(1);
				free(cur_smf_state);
			} else {
				free(cur_smf_state);
				return (B_FALSE);
			}
		} else {
			return (B_FALSE);
		}
	}

	return (B_FALSE);
}

/*
 * Name:	restore_local_fs
 * Description: If the SMF service system/filesystem/local:default was
 *		enabled using enable_local_fs(), then this function disables
 *		the service.
 * Arguments:	None
 * Returns:	B_TRUE on success; B_FALSE on error.
 */
boolean_t
restore_local_fs(void)
{
	int i;
	char *cur_smf_state;

	if (!fs_temporarily_enabled) {
		return (B_TRUE);
	}

	if (smf_disable_instance(svm_core_svcs, SMF_TEMPORARY) != 0) {
		return (B_FALSE);
	}

	for (i = 0; i < MAX_TRY; i++) {
		if ((cur_smf_state = smf_get_state(svm_core_svcs)) != NULL) {
			if (strcmp(cur_smf_state, SCF_STATE_STRING_DISABLED)
				== 0) {
				fs_temporarily_enabled = B_FALSE;
				free(cur_smf_state);
				break;
			}
			(void) sleep(1);

			free(cur_smf_state);
		} else {
			return (B_FALSE);
		}
	}

	return (!fs_temporarily_enabled);
}
