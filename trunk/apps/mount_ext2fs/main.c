/*
 * Mount EXT2FS - Mount an EXT2FS file system
 * using the NFS file system and an NFS server
 * Copyright (c) 2006 by Martin Rosenau
 * Adapted for ext2fs by Moinak Ghosh
 *
 * This is free software; you can redistribute it and/or modify it under the
 * terms of the GNU General Public License, see the file COPYING.
 *
 * Main file
 */
#include "mount_ext2fs.h"
#include <signal.h>
#include <poll.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <limits.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <dirent.h>
#include <sys/mnttab.h>
#include <libgen.h>

static pid_t umount_pid;
static char *mountpoint=NULL;
static int partmode = 2;
static int nofork = 0;
static int regfile;
static int overlay = 0;
uint64_t fsoff = 0;
static char vdev[PATH_MAX];
static char devline[PATH_MAX];
static char pidfile[100];

#define PRTPART_BIN "/usr/bin/prtpart.bin -t"
#define TMP_PREFIX "/tmp"
#define LFS_PREFIX ".lfs_mount"
#define LFS_PREFIX_LEN 9

/* Handle the SIGTERM signal: Unmount the file system */
static void
handle_signal(int sig)
{
    if(!umount_pid)
    {
        umount_pid=fork();
        if(!umount_pid)
        {
            int ndev;

            setuid(0);
            ndev = open("/dev/null", O_WRONLY);
            if (ndev != -1) {
                dup2(ndev, fileno(stdout));
                dup2(ndev, fileno(stderr));
            }
            execl("/usr/lib/fs/nfs/umount","/usr/lib/fs/nfs/umount",mountpoint,NULL);
            exit(1);
        }
    }
}

static void
parse_options(char *opts)
{
	char *tok, *tok1;

	if ((tok=strtok(opts, ",")) != NULL) {
		do {
			if (strcmp(tok, "partition") == 0)
				partmode = 1;
			else if (strcmp(tok, "nopartition") == 0)
				partmode = 0;
			else if (strcmp(tok, "nofork") == 0)
				nofork = 1;
			else if (strncmp(tok, "offset", 6) == 0) {
				tok1 = strchr(tok, '=');
				if (tok1 != NULL)
					fsoff = strtoll(tok1+1, 0, 0);
			} else if (strncmp(tok, "soffset", 7) == 0) {
				tok1 = strchr(tok, '=');
				if (tok1 != NULL)
					fsoff = ((uint64_t)strtoll(tok1+1, 0, 0))
						* 512;
			}
		} while ((tok= strtok(NULL, ",")) != NULL);
	}
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

void
register_mount(const char *mntpt, char *device, pid_t pid, char *fs,
    char *addr, char *ldev) {
    struct flock lck_it;
    char line[1024];

    snprintf(pidfile, 100, "%s/%s_%u", TMP_PREFIX, LFS_PREFIX, pid);
    regfile = open(pidfile, O_WRONLY | O_TRUNC | O_CREAT | O_SYNC);
    if (regfile == -1) {
        perror("Error opening registry file");
        fprintf(stderr, "To unmount the file system type \"kill %u\".\n", pid);
        return;
    }
 
    lck_it.l_type = F_WRLCK;
    lck_it.l_whence = SEEK_SET;
    lck_it.l_start = 0;
    lck_it.l_len = 0;
 
    snprintf(line, sizeof (line), "%s,%s,%d,%s,%s,%s\n",
             mntpt, device, pid, fs, addr, ldev);
    while (write(regfile, line, strlen(line)) == -1 &&
             errno == EINTR);

    (void) fcntl(regfile, F_SETLK, &lck_it);
    /* Hold the registry file open since we also need to hold the lock */
}

void
unregister_mount(const char *mntpt, char *device, pid_t pid)
{
    close(regfile);
    unlink(pidfile);
}

int
search_mntpt(char *mntpt) {
    DIR *tmpdir;
    struct dirent *dent;
    struct mnttab mp;
    struct mnttab mreq;
    FILE *mf, *fh;
    struct flock lck_it;
    char lfs_file[100];
    char *mpt, *dev, *fs, *addr, *ldev;
    int fpid;
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
                int upid;

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
                     * Fail if overlay mount was not specified
                     */
                    if (strcmp(mpt, mntpt) == 0 && !overlay) {
                        (void) closedir(tmpdir);
                        (void) fclose(mf);
                        return (0);
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

    return (1);
}

/* The main program */
int main(int argc,char **argv)
{
    int sock,port,i,nopts,err,mount_pid;
    char *image = NULL, *ldev;
    struct sockaddr_in soa;
    char nfs_mount_opts[1000]="";
    char *mount_opts[100];
    char *ppos;
    union {
        int for_propper_alignment;
        char buf[8192];
    } buf;
    struct pollfd pfd;
    int partnum;
    int fstyp_mode = 0;

    /* Get all the arguments */
    mount_opts[0]="/usr/sbin/mount";
    mount_opts[1]="-F";
    mount_opts[2]="nfs";
    mount_opts[3]="-r";
    nopts=4;
    for(i=1,err=0;i<argc && !err;i++)
    {
        if(!strcmp(argv[i],"-no") && i+1<argc)
        {
            strcat(nfs_mount_opts,argv[++i]);
            strcat(nfs_mount_opts,",");
        }
        else if(!strcmp(argv[i],"-m") && i+1<argc)
            mount_opts[nopts++]=argv[++i];
        else if(!strcmp(argv[i],"-O") && i+1<argc) {
            overlay = 1;
            mount_opts[nopts++]=argv[i];
        } else if(!strcmp(argv[i],"-pt")) partmode=1;
        else if(!strcmp(argv[i],"-nf")) nofork=1;
        else if(!strcmp(argv[i],"-npt")) partmode=0;
        else if(!strcmp(argv[i],"-off") && i+1<argc)
            fsoff=strtoll(argv[++i],0,0);
        else if(!strcmp(argv[i],"-sec") && i+1<argc)
            fsoff=((uint64_t)strtoll(argv[++i],0,0))*512;
	else if (strcmp(argv[i],"-o") == 0) parse_options(argv[++i]);
        else if(argv[i][0]=='-') err=1;
        else if(!image) image=argv[i];
        else if(!mountpoint) mountpoint = strdup(argv[i]);
        else err=1;
    }

    /* Check for access rights */
    if(getuid() && geteuid())
    {
        fprintf(stderr,"Only root may run this program.\n");
        return (1);
    }

    /*
     * Just try to access and detect ext2 filesystem if called as fstyp
     */
    if (strcmp(basename(argv[0]), "fstyp") == 0) {
        fstyp_mode = 1;
        if (!image) {
            fprintf(stderr,"\nSyntax: fstyp image [options]\n\n"
            "image        File system image or rdsk device (/dev/rdsk/xxx)\n"
            "-pt          Image/disk has an x86 partition table with only one partition\n"
            "-npt         Image/disk is EXT2FS itself / no partition table\n"
            "-off number  The image begins at byte offset number (nnn, 0ooo, 0xHHH)\n"
            "-sec number  The image begins at byte offset number*512 (sector)\n");
            return (1);
        }
    } else {
        if(err || !mountpoint || !image)
        {
            fprintf(stderr,"\nSyntax: mount_ext2fs image mountpoint [options]\n\n"
            "image        File system image or rdsk device (/dev/rdsk/xxx)\n"
            "mountpoint   Mount point (see mount)\n"
            "-no nfsopt   Mount option to be passed in the \"-o\" option of mount_nfs\n"
            "-o options   Mount options equivalent for -pt, -npt, -off, -sec, and -nf\n"
	    "-O           Overlay mount\n"
            "-pt          Image/disk has an x86 partition table with only one partition\n"
            "-npt         Image/disk is EXT2FS itself / no partition table\n"
            "-off number  The image begins at byte offset number (nnn, 0ooo, 0xHHH)\n"
            "-sec number  The image begins at byte offset number*512 (sector)\n"
            "-nf          Do not fork into background\n\n");
            return 1;
        }

        /* Check for existing mounts and cleanup dangling servers/mounts */
        if (!search_mntpt(mountpoint)) {
            fprintf(stderr, "%s already in use\n", mountpoint);
            return (1);
        }
    }

    ldev = image;
    /* Check for virtual device names */
    ppos = strrchr(image, 'p');
    if (ppos != NULL) {
        ppos++;
	partnum = atoi(ppos);

	/* p5 and greater indicate logical devices */
	if (partnum > 4) {
            char *s;
	    char buf[PATH_MAX];

	    /*
	     * Check whether we have device link for logical device
	     */
	    if (readlink(image, buf, PATH_MAX) != -1)
		goto devline_ok;

            /* Translate virtual device to physical p0 device and offset */
            snprintf(vdev, PATH_MAX, "%s %s", PRTPART_BIN, image);
            FILE *fh = popen(vdev, "r");
            if (fh == NULL) {
                perror("Cannot translate device name");
                exit(1);
            }
            s = fgets(devline, PATH_MAX, fh);
            if (s == NULL) {
                perror("Cannot translate device name");
                fclose(fh);
                exit(1);
            }
            fclose(fh);

            s = strchr(devline, ' ');
            if (s == NULL) {
                fprintf(stderr, "Wrong output from prtpart: %s\n", devline);
                exit(1);
            }
            image = devline;
            *s++ = '\0';
            fsoff = ((uint64_t)strtoull(s,0,0));
        } else {
devline_ok:
            strcpy(devline, image);
        }
    }
        
    /* Initialize the EXT2FS access */
    i=ext2_initialize(image, fsoff, partmode, fstyp_mode == 1 ? 0:1);
    if(i) return i;

    if (fstyp_mode) {
        puts("ext2fs");
        return (0);
    }

    /* Initialize signal handling */
    umount_pid=(pid_t)-1;
    signal(SIGINT,handle_signal);
    signal(SIGTERM,handle_signal);

    /* Create the UDP socket */
    sock=socket(PF_INET,SOCK_DGRAM,IPPROTO_UDP);
    soa.sin_family=AF_INET;
    soa.sin_addr.s_addr=htonl(0x7F000001);
    soa.sin_port=0;
    bind(sock,(struct sockaddr *)&soa,sizeof(soa));
    port=sizeof(soa);
    getsockname(sock,(struct sockaddr *)&soa,&port);
    port=ntohs(soa.sin_port);

    /* Mount the NFS file system */
    sprintf(buf.buf,"port=%u,public,vers=2,proto=udp",port);
    strcat(nfs_mount_opts,buf.buf);
    mount_opts[nopts++]="-o";
    mount_opts[nopts++]=&(nfs_mount_opts[0]);
    mount_opts[nopts++]="127.0.0.1:/";
    mount_opts[nopts++]=(char *)mountpoint;
    mount_opts[nopts++]=NULL;
    mount_pid=fork();
    if(!mount_pid)
    {
        execv(mount_opts[0],mount_opts);
        fprintf(stderr,"Could not start mount.\n");
        exit(1);
    }

    /* Now handle incoming packets */
    umount_pid=0;
    while(1)
    {
        /* Unmount by kill done */
        if(umount_pid) if(waitpid(umount_pid,NULL,WNOHANG)>0)
        {
            close(sock);
            unregister_mount(mountpoint, devline, getpid());
            return 1;
        }
        /* Get the status of the "Mount" command
         * Cancel if mount was not successful
         * Fork into the background otherwise */
        if (mount_pid) if(waitpid(mount_pid,&i,WNOHANG)>0)
        {
            if(i&0xFF00) {
                close(sock);
                return 1;
            }
            signal(SIGINT,handle_signal);
            signal(SIGTERM,handle_signal);
            if(!nofork) {
                sigignore(SIGHUP);
                i=fork();
                if(i) {
                    /* printf("To unmount the file system type \"kill %u\".\n",i); */
                    return 0;
                } else {
                    if (strcmp(devline, ldev) == 0 && fsoff > 0) {
                        char img[PATH_MAX];

                        snprintf(img, PATH_MAX, "%s:%llu", image, fsoff);
                        register_mount(mountpoint, devline, getpid(),
                            "ext2fs", "127.0.0.1:/", img);
                    } else {
                        register_mount(mountpoint, devline, getpid(),
                            "ext2fs", "127.0.0.1:/", ldev);
                    }
                }
                mount_pid = 0;
            }
        }
        /* Handle incoming data packets */
        pfd.events=POLLIN;
        pfd.fd=sock;
        pfd.revents=0;
        poll(&pfd,1,1000);
        if(pfd.revents&POLLIN)
        {
            i=sizeof(soa);
            i=recvfrom(sock,buf.buf,sizeof(buf.buf),0,(struct sockaddr *)&soa,&i);
            if(i>0) {
                handle_nfs_packet(sock,&soa,buf.buf,i);
            }
        }
    }

    /* Should never get here */
    return 0;
}

