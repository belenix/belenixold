/*
 * List local fs mounts served by the modified userland NFS server
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
	printf( "Usage:\n  %s\n", cmd);
}

int
parse_line(char *line, char **mpt, char **dev, int *fpid, char **fs, char **addr, char **ldev){
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
list_mounts() {
    DIR *tmpdir;
    struct dirent *dent;
    struct mnttab mp;
    struct mnttab mreq;
    FILE *mf, *fh;
    struct flock lck_it;
    char lfs_file[100], *ulfs_file;
    char *mpt, *dev, *fs, *addr, *umpt = NULL, *ldev;
    int fpid, upid, umpid;
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
                     * print all the details.
                     */
                    printf("%17s %30s %7s %6d %12s %s\n", dev, ldev, fs, fpid, addr, mpt);
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

    return (1);
}

int
main(int argc, char **argv)
{
	if (argc != 1 ) {
		usage(argv[0]);
		exit(1);
	}

        printf("%17s %30s %7s %6s %12s %s\n", "PHYSICAL DEVICE", "LOGICAL DEVICE",
               "FS", "PID", "ADDR", "Mounted on");
	list_mounts();
	return (0);
}
