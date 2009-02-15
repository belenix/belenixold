#ident	"@(#)sslconf.sed	1.8	07/12/04 SMI"
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
# Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.

/^#SSLRandomSeed startup file:\/dev\/urandom 512/c\
SSLRandomSeed startup file:/dev/urandom 512
/^#SSLRandomSeed connect file:\/dev\/urandom 512/c\
SSLRandomSeed connect file:/dev/urandom 512\
SSLCryptoDevice pkcs11
/^ServerName/c\
ServerName 127.0.0.1:443
/^SSLCipherSuite/c\
#   AES with keylengths > 128 bit is not supported by default on Solaris.\
#   To operate with AES256 you must install the SUNWcry and SUNWcryr\
#   packages from the Solaris 10 Data Encryption Kit.\
SSLCipherSuite ALL:!ADH:!EXPORT56:-AES256-SHA:-DHE-RSA-AES256-SHA:-DHE-DSS-AES256-SHA:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP:+eNULL\

