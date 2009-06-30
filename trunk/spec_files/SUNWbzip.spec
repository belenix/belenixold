#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SUNWbzip
#
# includes module(s): Bzip2
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SUNWbzip
Summary:                 Bzip2 Compression utility and library
Version:                 1.0.5
URL:                     http://www.bzip.org
Source:                  http://www.bzip.org/%{version}/bzip2-%{version}.tar.gz
Source1:                 bzip2-mapfile
Source2:                 bzcat.1.sunman
Source3:                 bzcmp.1.sunman
Source4:                 bzdiff.1.sunman
Source5:                 bzegrep.1.sunman
Source6:                 bzfgrep.1.sunman
Source7:                 bzgrep.1.sunman
Source8:                 bzip2.1.sunman
Source9:                 bzip2recover.1.sunman
Source10:                bzless.1.sunman
Source11:                bzmore.1.sunman
Source12:                bzip2-oldapi.c
Source13:                bzip2-makefile.build
Source14:                libbz2.3.sunman
Source15:                bzip2-mapfile

Patch1:                  bzip2-01.diff
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -c -n %name-%version
cd bzip2-%{version}
%patch1 -p1
cp %{SOURCE12} ./oldapi.c
cd ..

%ifarch amd64 sparcv9
cp -pr bzip2-%{version} bzip2-%{version}-64
%endif

mv bzip2-%{version}/Makefile bzip2-%{version}/Makefile.dist
mv bzip2-%{version}-64/Makefile bzip2-%{version}-64/Makefile.dist


%build
%ifarch amd64 sparcv9
cd bzip2-%{version}-64
export PATH=/usr/ccs/bin:/usr/bin:/usr/sbin:/bin:/usr/sfw/bin:/opt/SUNWspro/bin
export CFLAGS="%optflags64 -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export INSTALL=/usr/ucb/install
export MAKE=/usr/bin/make
export LDFLAGS="-m64 -Wl,-z -Wl,defs -Wl,-z -Wl,text -Wl,-z -Wl,combreloc -L/usr/lib/%{_arch64} -R/usr/lib/%{_arch64} %{gnu_lib_path64}"

cat %{SOURCE13} | sed "{
    s#::cc#${CC}#
    s#::cflags#${CFLAGS}#
    s#::ldflags#${LDFLAGS}#
    s#::mapfile#%{SOURCE15}#
}" > Makefile

/usr/bin/make
cd ..
%endif

cd bzip2-%{version}
export PATH=/usr/ccs/bin:/usr/bin:/usr/sbin:/bin:/usr/sfw/bin:/opt/SUNWspro/bin
export CFLAGS="%optflags -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export INSTALL=/usr/ucb/install
export MAKE=/usr/bin/make
export LDFLAGS="-Wl,-z -Wl,defs -Wl,-z -Wl,text -Wl,-z -Wl,combreloc %{gnu_lib_path}"

cat %{SOURCE13} | sed "{
    s#::cc#${CC}#
    s#::cflags#${CFLAGS}#
    s#::ldflags#${LDFLAGS}#
    s#::mapfile#%{SOURCE15}#
}" > Makefile

/usr/bin/make
cd ..


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

ROOT=${RPM_BUILD_ROOT}
ROOTINCLUDEDIR=${ROOT}%{_includedir}
ROOTLIB=${RPM_BUILD_ROOT}%{_libdir}
ROOTLIB64=${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}
ROOTBIN=${RPM_BUILD_ROOT}%{_bindir}
ROOTBIN64=${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
ROOTMAN1DIR=${RPM_BUILD_ROOT}%{_mandir}/man1
ROOTMAN3DIR=${RPM_BUILD_ROOT}%{_mandir}/man3

%ifarch amd64 sparcv9
cd bzip2-%{version}-64
mkdir -p ${ROOTLIB64}
mkdir -p ${ROOTBIN64}

/usr/ucb/install -m 0755 libbz2.so.1 ${ROOTLIB64}/libbz2.so.1
(cd ${ROOTLIB64}
  ln -s libbz2.so.1 libbz2.so
)

rm -f bzgrep.tmp
sed \
        -e s,'^#!/bin/sh','#!/bin/ksh', \
        < bzgrep \
        > bzgrep.tmp

/usr/ucb/install -m 0555 bzgrep.tmp ${ROOTBIN64}/bzgrep
for e in bzip2 bzip2recover bzmore bzdiff
do
	/usr/ucb/install -m 0555 ${e} ${ROOTBIN64}/${e}
done

(cd ${ROOTBIN64}
 ln bzip2 bunzip2
 ln bzip2 bzcat
 ln bzgrep bzegrep
 ln bzmore bzless
 ln bzdiff bzcmp)

cd ..
%endif

cd bzip2-%{version}
mkdir -p ${ROOTINCLUDEDIR}
mkdir -p ${ROOTMAN1DIR}
mkdir -p ${ROOTMAN3DIR}

/usr/ucb/install -m 0755 libbz2.so.1 ${ROOTLIB}/libbz2.so.1
(cd ${ROOTLIB}
  ln -s libbz2.so.1 libbz2.so
)

rm -f bzgrep.tmp
sed \
        -e s,'^#!/bin/sh','#!/bin/ksh', \
        < bzgrep \
        > bzgrep.tmp

/usr/ucb/install -m 0555 bzgrep.tmp ${ROOTBIN}/bzgrep
for e in bzip2 bzip2recover bzmore bzdiff
do
	/usr/ucb/install -m 0555 ${e} ${ROOTBIN}/${e}
done

(cd ${ROOTBIN}
 ln bzip2 bunzip2
 ln bzip2 bzcat
 ln bzgrep bzegrep
 ln bzmore bzless
 ln bzdiff bzcmp)

#
# Commented till we get rid of SUNWsfman UGH
#

#for m in %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} \
#	%{SOURCE7} %{SOURCE8} %{SOURCE9} %{SOURCE10} %{SOURCE11}
#do
#	manpage=`basename $m .sunman`
#	/usr/ucb/install -m 0444 ${m} ${ROOTMAN1DIR}/${manpage}
#done

#manpage=`basename %{SOURCE14} .sunman`
#/usr/ucb/install -m 0444 %{SOURCE14} ${ROOTMAN3DIR}/${manpage}
/usr/ucb/install -m 0644 bzlib.h ${ROOTINCLUDEDIR}/bzlib.h
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Jun 30 2009 - moinakg@gmail.com
- Initial spec (migrated and modified from SFW gate).

