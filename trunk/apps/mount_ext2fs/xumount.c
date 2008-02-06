/*
 * Unmount local fs mounts served by the modified userland NFS server
 * Also terminates the NFS server attached to the mounted resource.
 * Copyright (C) 2006 Moinak Ghosh
 *
 * This is free software; you can redistribute it and/or modify it under the
 * terms of the GNU General Public License, see the file COPYING.
 */

#include <signal.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <dirent.h>
#include <sys/mnttab.h>

#define TMP_PREFIX "/tmp"
#define LFS_PREFIX ".lfs_mount"
#define LFS_PREFIX_LEN 9

char *mntpt;

void
usage(char *cmd) {
	printf( "Usage:\n  %s [-f] <device|mountpoint>\n", cmd);
}

int
parse_line(char *line, char **mpt, char **dev, int *fpid, char **fs, char **addr, char **ldev) {
    int num, i, j;
    size_t len = strlen(line);
    char *pidstr;

    num = 0;
    line[--len] = '\0'; /* Chomp */
    *mpt = &line[0];
    for (i=0; i<len; i++)
        if (line[i] == ',') {
            line[i] = '\0';
            if (num == 0)
                *dev = &line[i+1];
            else if (num == 1)
                pidstr = &line[i+1];
            else if (num == 2) {
                *fpid = atoi(pidstr);
                *fs = &line[i+1];
            } else if (num == 3)
                *addr = &line[i+1];
            else if (num == 4)
                *ldev = &line[i+1];

            num++;
        }
    if (num < 3)
        return (0);

    return (1);
}

int
search_unmount(char *mntpt, int force) {
    DIR *tmpdir;
    struct dirent *dent;
    struct mnttab mp;
    struct mnttab mreq;
    FILE *mf, *fh;
    struct flock lck_it;
    char lfs_file[100], *ulfs_file;
    char *mpt, *dev, *fs, *addr, *umpt = NULL, *ldev;
    int fpid, upid, umpid;
    size_t mlast;
    char line[1024];

    tmpdir = opendir(TMP_PREFIX);
    if (tmpdir == NULL) {
        perror("Unable to open temp dir");
        return (1);
    }

    mf = fopen("/etc/mnttab", "r");
    if (mf == NULL) {
        perror("Unable to open /etc/mnttab");
        closedir(tmpdir);
        return (1);
    }

    /* Remove any trailing / */
    mlast = strlen(mntpt)-1;
    if (mntpt[mlast] == '/')
        mntpt[mlast] = '\0';

    while ((dent = readdir(tmpdir)) != NULL) {
        if (strlen(dent->d_name) > LFS_PREFIX_LEN) {
            if (strncmp(dent->d_name, LFS_PREFIX, LFS_PREFIX_LEN) == 0) {

                snprintf(lfs_file, 100, "%s/%s", TMP_PREFIX, dent->d_name);
                fh = fopen(lfs_file, "r+");
                if (fh == NULL)
                    continue;

                /* Parse details for this entry */
                if (fgets(line, 1024, fh) == NULL) {
                    fclose(fh);
                    continue;
                }
                if (!parse_line(line, &mpt, &dev, &fpid, &fs, &addr, &ldev)) {
                    fclose(fh);
                    continue;
                }

                /* Now check whether the server is alive */
                lck_it.l_type = F_WRLCK;
                lck_it.l_whence = SEEK_SET;
                lck_it.l_start = 0;
                lck_it.l_len = 0;
                (void) fcntl(fileno(fh), F_SETLK, &lck_it);
                if (errno != EAGAIN) {
                    /* Server for this mntpt is not alive. Remove file */
                    fclose(fh);
                    unlink(lfs_file);

                    /* Issue a NFS umount just in case the server had died */
                    upid=fork();
                    if(!upid) {
                        int ndev;

                        setuid(0);
                        ndev = open("/dev/null", O_WRONLY);
                        if (ndev != -1) {
                            dup2(ndev, fileno(stdout));
                            dup2(ndev, fileno(stderr));
                        }
                        execl("/usr/lib/fs/nfs/umount","/usr/lib/fs/nfs/umount",mpt,NULL);
                        exit(0);
                    }
                    continue;
                }
                fclose(fh);

                /* Now search mnttab */
                mreq.mnt_special = NULL;
                mreq.mnt_mountp = mpt;
                mreq.mnt_fstype = "nfs";
                mreq.mnt_mntopts = NULL;
                mreq.mnt_time = NULL;
                if (getmntany(mf, &mp, &mreq) == 0) {
                    /*
                     * Mounted resource with server running
                     * Here we check if this resource is what
                     * is being passed by user and set unmount
                     * params. The semantic is that umount
                     * has to unmount the last matching entry.
                     */
                    if (strcmp(mntpt, mpt) == 0 || strcmp(mntpt, dev) == 0
                        || strcmp(mntpt, addr) == 0
                        || strcmp(mntpt, ldev) == 0) {
                        umpid = fpid;
                        if (umpt) {
                            free(umpt);
                            free(ulfs_file);
                        }
                        umpt = strdup(mpt);
                        ulfs_file = strdup(lfs_file);
                    }
                } else {
                    /*
                     * Server running but no mounted resource
                     * kill server.
                     */
                    (void) kill(fpid, SIGTERM);
                }
                resetmnttab(mf);
            }
        }
    }
    (void) closedir(tmpdir);
    (void) fclose(mf);

    if (umpt) {
        if (!force) {
            (void) kill(umpid, SIGTERM);

        } else {
            (void) kill(umpid, SIGKILL);
            upid=fork();
            if(!upid) {
                int ndev;

                setuid(0);
                ndev = open("/dev/null", O_WRONLY);
                if (ndev != -1) {
                    dup2(ndev, fileno(stdout));
                    dup2(ndev, fileno(stderr));
                }
                execl("/usr/lib/fs/nfs/umount","/usr/lib/fs/nfs/umount",umpt,NULL);
                exit(0);
            }
            (void) unlink(ulfs_file);
        }
    } else {
	fprintf(stderr, "No matching mounted resource\n");
	return (0);
    }

    return (1);
}

int
main(int argc, char **argv)
{
	int i, err;
	int opt;
	int force = 0;

	opt = 0;

	if (argc < 2) {
		usage(argv[0]);
		exit(1);
	}

	for (i=1,err=0; i<argc && !err; i++) {
		if (strcmp(argv[i], "-f") == 0) {
			force = 1;
		} else if (argv[i][0] == '-') {
			fprintf(stderr, "Invalid option %s\n", argv[i]);
			usage(argv[0]);
			exit(1);
		} else {
			if (opt) {
				fprintf(stderr, "Invalid arguments\n");
				usage(argv[0]);
				exit(1);
			}
			mntpt = argv[i];
 			opt = 1;
		}
	}

	if (!search_unmount(mntpt, force)) {
		fprintf(stderr, "Unmount failed\n");
		return (1);
	}
	return (0);
}
