#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License, Version 1.0 only
# (the "License").  You may not use this file except in compliance
# with the License.
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
# Copyright 2005 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# Author: Moinak.Ghosh@Sun.COM

#
# Try to find out whether this is Microsoft Virtual PC
# We search for a certain combination of PCI device
# ids as is found in Virtual PC.
#
# Intel Host Bridge: 8086,7192
# Intel PIIX4 ISA Bridge: 8086,7110
# Intel PIIX4 IDE interface: 8086,7111
# Intel PIIX4 ACPI: 8086,7113
# S3 Trio32/64/64V+: 5333,8811
# DECchip 21140 FastEthernet: 1011,9
#

xc=/usr/share/xconfigs
/usr/sbin/smbios -t 1 | /usr/bin/grep "Ferrari 4000" > /dev/null
if [ $? -eq 0 ]
then
	/usr/bin/cp ${xc}/xorg.conf.f4k /etc/X11/xorg.conf

else

/usr/bin/cat /.prtconf | nawk 'BEGIN { a=0; b=0; c=0; d=0; e=0; f=0;}
{
	if (match($0, /8086,7192/)) {
		a=1;
	} else if (match($0, /8086,7110/)) {
		b=1;
	} else if (match($0, /8086,7111/)) {
		c=1;
	} else if (match($0, /8086,7113/)) {
		d=1;
	} else if (match($0, /5333,8811/)) {
		e=1;
	} else if (match($0, /1011,9/)) {
		f=1;
	}
}
END {
	if (a == 1 && b == 1 && c == 1 && d == 1 && e == 1 && f == 1) {
		system("/usr/bin/cp ${xc}/xorg.conf.virtpc /etc/X11/xorg.conf");
	}
}'
fi

#rm -f /etc/xconfigs/*

[ -f /etc/X11/xorg.conf ] || exit 1

