#!/usr/bin/bash
#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

#
# Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# This script pulls in binaries from various locations and builds
# a complete bootable CD and memory based filesystem image of
# OpenSolaris. Finally it generates an iso image that can be burned
# onto the CDROM to get a bootable BeleniX Live CD/DVD.
#

PATH=/usr/bin:/usr/X11/bin:/usr/sbin:/sbin:/usr/sfw/bin:/usr/gnu/bin
export PATH

id | grep "uid=[0-9](" >/dev/null
if [ $? -ne 0 ] ; then
	echo "You must run this script as root"
	exit 0
fi

# Path of the BeleniX Constructor kit.

D=`dirname $0`
TOOLS=`(cd $D; cd ../tools; pwd)`
SRC=`(cd $D; pwd)`

echo $SRC

if [ $# != "1" ] ; then
	echo "You must specify a path to the configuration file"
	echo "build_dist <configuration file>"
	exit 1
fi
source $SRC/build_dist.lib

source $1  #read the configuration file passed in

if [ "$DIST_PKGS_TYPE" = "IPS" ]
then
	source $SRC/pkg_retrieve_ips.lib
fi
if [ "$DIST_PKGS_TYPE" = "SVR4" ]
then
	source $SRC/pkg_retrieve_svr4.lib
fi

#Verify the validity of the values specified in the configuration file
#and make sure all required values are specified.
verify_conf

TMPDIR=/tmp/distro_tool.$$
ADMIN_FILE=$TMPDIR/admin
BOOT_ARCHIVE=$DIST_PROTO/boot/x86.microroot
MICROROOT=$DIST_PROTO/bootcd_microroot
#RAMDISK_SIZE=88700
RAMDISK_SIZE=110000
DIST_MICROROOT_LIST=$SRC/microroot_list

# Set up root of the proto area
[ -d $DIST_PROTO ] || mkdir $DIST_PROTO

rm -rf $TMPDIR
# Create a temporary directory
mkdir $TMPDIR

(
echo "=== $0 started at `date`"

#
# Handle IPS packages
#
if [ "$DIST_PKGS_TYPE" = "IPS" ]
then

pkg_retrieve_init $DIST_PKG_SERVER $DIST_PROTO
if [ $? -ne 0 ] ; then
	echo "Error in pkg init for proto area."
	if [ "$QUIT_ON_PKG_FAILURES" = "yes" ] ; then
		exit 1
	fi
fi

pkg_list_verify $DIST_PKG_LIST
if [ $? -ne 0 ] ; then
	echo "Error in pkg list verify.  Pkgs missing from repository?"
	if [ "$QUIT_ON_PKG_FAILURES" = "yes" ] ; then
		exit 1
	fi
fi

# Add each of the packages specified for the product into the proto area
pkg_retrieve $DIST_PKG_LIST
if [ $? -ne 0 ] ; then
	echo "Error retrieving packages for proto area."
	if [ "$QUIT_ON_PKG_FAILURES" = "yes" ] ; then
		exit 1
	fi
fi

fi

#
# Handle SVR4 packages
#
if [ "$DIST_PKGS_TYPE" = "SVR4" ]
then

echo "Processing SVR4 Packages ..."
if [ -n "${SPKG_REPO}" ]
then
	spkg_add ${SPKG_REPO} ${SPKG_CLUSTER} ${DIST_PROTO} ${SRC}
	if [ $? -ne 0 ] ; then
		echo "Error adding packages to proto area"
		if [ "$QUIT_ON_PKG_FAILURES" = "yes" ] ; then
			exit 1
		fi
	fi
else
	#pkg_list_verify $DIST_PKG_LIST $DIST_PKG_DIR
	#if [ $? -ne 0 ] ; then
	#	echo "Error in pkg list verify.  Pkgs missing from the directory?"
	#	if [ "$QUIT_ON_PKG_FAILURES" = "yes" ] ; then
	#		exit 1
	#	fi
	#fi

	# Add each of the packages specified for the product into the proto area
	pkg_add $DIST_PKG_LIST $DIST_PKG_DIR $DIST_PROTO
	if [ $? -ne 0 ] ; then
		echo "Error adding packages to proto area"
		if [ "$QUIT_ON_PKG_FAILURES" = "yes" ] ; then
			exit 1
		fi
	fi
fi
fi

#
# Calculate the image size and write to the .image_info file
#
IMAGE_SIZE=`/bin/du -sk $DIST_PROTO | awk '{print $1}'`

echo IMAGE_SIZE=$IMAGE_SIZE > $DIST_PROTO/.image_info

#
# Pre-configure Gnome databases
#

echo "Running GNOME postrun scripts"
if [ "$DIST_PKGS_TYPE" = "IPS" ]
then
	echo "Configuring Gnome in PROTO area"
	cp -r $SRC/postrun_scripts ${PROTO}
	#chroot $PROTO /postrun_scripts/exec_postrun
	do_chroot $PROTO /postrun_scripts/exec_postrun

	#Remove the scripts after finish executing them so the image is
	#not polluted with temporary files.
	/bin/rm -rf ${PROTO}/postrun_scripts
else
	mount -F lofs /proc $PROTO/proc
	#[ -x $PROTO/var/lib/postrun/postrun-runq ] && chroot $PROTO /var/lib/postrun/postrun-runq
	[ -x $PROTO/var/lib/postrun/postrun-runq ] && do_chroot $PROTO /var/lib/postrun/postrun-runq
	umount $PROTO/proc
fi

#
# Create the boot archive. This is a UFS filesystem image in a file
# that is loaded into RAM by Grub. A file is created using mkfile
# and is added as a block device using lofiadm. newfs is then used
# to create a UFS filesystem on the lofi device and then it is
# mounted and all the files required for a minimal root fs are
# copied.
#
initialize_root_archive 

populate_root_archive $DIST_PROTO

# Perform special processing to create Live CD
livemedia_processing $DIST_PROTO $MICROROOT $TMPDIR

# If additonal special processing is provided in the tar file
# by the user, execute it.
if [ "$DIST_ADDITIONAL_MOD" != "" ] ; then
	# Extract the post processing archive into the temp dir
	# Assuming the archive is a tar file.

	cd $TMPDIR
	/bin/tar -xf $DIST_ADDITIONAL_MOD
	if [ $? -ne 0 ] ; then
		echo "FAILURE: Error in untarring $DIST_ADDITIONAL_MOD"
		fatal_exit	
	fi
	# This needs to be changed so it's not hardcoded.
	POST_PROCESS_SCRIPT=post_process
	#Make sure the post-process script is there
	if [ -f $POST_PROCESS_SCRIPT  -a -x $POST_PROCESS_SCRIPT ] ; then 
		./$POST_PROCESS_SCRIPT $DIST_PROTO $MICROROOT $TMPDIR
		if [ $? -ne 0 ] ; then
			echo "FAILURE: Fatal error running $POST_PROCESS_SCRIPT"
			fatal_exit	
		fi
	else
		echo "Post process script not found in archive"
		echo "Modification is not done"
	fi
fi

#
# Unmount the lofi device and remove it. Then gzip the file
# containing the root fs image. Grub will decompress it while
# loading.
#
echo "Archiving Boot Archive"

rm -rf $MICROROOT
 
7za a -tGzip -mx=7 ${TMPDIR}/x86.microroot.gz ${TMPDIR}/x86.microroot
mv ${TMPDIR}/x86.microroot.gz $BOOT_ARCHIVE
chmod a+r $BOOT_ARCHIVE

create_iso

# Generate USB image if requested
if [ "$DIST_USB" != "" ] ; then
	/usr/bin/bash $TOOLS/usbgen $DIST_ISO $DIST_USB $TOOLS $TMPDIR
fi

cleanup

exit 0

) 2>&1 | tee $SRC/$0.log
