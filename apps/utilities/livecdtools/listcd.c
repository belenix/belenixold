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
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <libdevinfo.h>
#include <sys/sunddi.h>
#include <sys/types.h>
#include <limits.h>

/*
 * Tinny utility to traverse the device tree and dump
 * all the minor cdrom nodes.
 */

static int
dump_minor(di_node_t node, di_minor_t  minor,  void *arg)
{
	char *nt, *mnp;
	char mpath[PATH_MAX];

	nt = di_minor_nodetype(minor);
	if (nt == NULL)
		return (DI_WALK_CONTINUE);

	if (strcmp(nt, DDI_NT_CD_CHAN) == 0 || strcmp(nt, DDI_NT_CD) == 0) {
		mnp = di_devfs_minor_path(minor);
		if (mnp != NULL) {
			strcpy(mpath, "/devices");
			strlcat(mpath, mnp, PATH_MAX);

			if (strstr(mnp, ",raw")) {
				di_devfs_path_free(mnp);
				return (DI_WALK_CONTINUE);
			}
			strlcat(mpath, ",raw", PATH_MAX);
			printf("/devices%s %s\n", mnp, mpath);
			di_devfs_path_free(mnp);
		}
	}

	return (DI_WALK_CONTINUE);
}

int main(void) {
	di_node_t root_node;

	if ((root_node = di_init("/", DINFOCPYALL)) == DI_NODE_NIL) {
		return (1);
	}
	di_walk_minor(root_node, NULL, 0, NULL, dump_minor);
        di_fini(root_node);
	sync();

        return (0);
}