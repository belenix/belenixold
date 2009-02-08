#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SUNWgmp
#
# includes module(s): GNU gmp
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

Name:                    SUNWsmagt
Summary:                 sun-netsnmp-port - System Management Agent files and libraries
Version:                 1.0
URL:                     http://www.net-snmp.org/
Source1:                 http://www.belenix.org/binfiles/sma1.0.tar.gz
Source2:                 http://www.belenix.org/binfiles/htmldoc.tar
Source3:                 net-snmp/init.sma
Source4:                 net-snmp/ltmain.sh
Source5:                 net-snmp/mib2c
Source6:                 net-snmp/run-tests
Source7:                 net-snmp/seaport.xml
Source8:                 net-snmp/sma.xml
Source9:                 net-snmp/snmpd.c
Source10:                net-snmp/snmpd.conf
Source11:                net-snmp/snmptrapd.c
Source12:                net-snmp/svc-sma

Patch1:                  net-snmp-01.kernel_sunos5.c.diff
Patch2:                  net-snmp-02.pkcs.c.diff
Patch3:                  net-snmp-03.proxy.c.diff
Patch4:                  net-snmp-04.hr_swrun.c.diff
Patch5:                  net-snmp-05.udpTable.diff
Patch6:                  net-snmp-06.sunHostPerf.c.diff
Patch7:                  net-snmp-07.sun-patchfile.diff
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWlibms
Requires:                SUNWlibmsr
Requires:                SUNWzlib

%package devel
Summary:                 sun-netsnmp-port-devel - System Management Agent development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name

%package -n SUNWsmcmd
Summary:                 sun-netsnmp-utils - System Management Agent applications and utilities
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name

%package -n SUNWsmmgr
Summary:                 sun-netsnmp-config - System Management Agent Startup scripts
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name

%package -n SUNWsmdoc
Summary:                 sun-netsnmp-doc - System Management Agent html documentation files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name


%prep
if [ "x`basename $CC`" = xgcc ]
then
	%error This spec file requires SUN Studio, set the CC and CXX env variables
fi

rm -rf %{name}-%{version}
mkdir -p %{name}-%{version}/sma
cd %{name}-%{version}/sma

gunzip -c %{SOURCE1} | gtar -xf - 
%ifarch amd64 sparcv9
cd ../
cp -pr sma sma-64
%endif

%build
cd %{name}-%{version}

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

MACH=`uname -p`
export MACH
if [ "$MACH" = "i386" ]
then
	MACH_TYPE=pc
	MACH32=i86
	MACH64=amd64
	XARCH="-m32 -xchip=pentium"
	XARCH64="-m64 -xarch=generic -Ui386 -U__i386"
	BUILDSUNISA32=32
	BUILDSUNISA64=amd64
	EXTRA_TARGETS="snmpd:%{SOURCE9} snmptrapd:%{SOURCE11}"
	SMADEFBITS=32
else
	MACH_TYPE=sun
	MACH32=sparcv7
	MACH64=sparcv9
	XARCH="-m32 -xarch=sparc"
	XARCH64="-m64 -xcode=abs64"
	BUILDSUNISA32=32
	BUILDSUNISA64=64
	EXTRA_TARGETS=""
	SMADEFBITS=64
fi
export MACH_TYPE MACH64 XARCH XARCH64
RELEASENUM=`uname -r | sed -e 's/[^.]*//'`
CONFIGTARGET=${MACH}-${MACH_TYPE}-solaris2${RELEASENUM}
TARGETNAME32=${CONFIGTARGET}_32
TARGETNAME64=${CONFIGTARGET}_64
TARGET32=targets/${TARGETNAME32}
TARGET64=targets/${TARGETNAME64}
PERLMAN3DIR=${RPM_BUILD_ROOT}/usr/perl5/5.8.4/man/man3
ccpath=`dirname $CC`
PATH="${ccpath}:/usr/perl5/bin:${PATH}"
export PATH

export LDFLAGS32="%_ldflags"
export LDFLAGS64="%_ldflags"

%ifarch amd64 sparcv9
LDFLAGS="$LDFLAGS64 ${XARCH64}"
CFLAGS="-Dsolaris_2 -xstrconst -Kpic ${XARCH64}"

cd sma-64
(cd net-snmp
 %patch1 -p1
 %patch2 -p1
 %patch3 -p1
 %patch4 -p1
 %patch5 -p1
)

(cd sun
 %patch6 -p1
 %patch7 -p1
)

cd net-snmp
mkdir -p targets
./maketarget ${TARGETNAME64}

(cd ../sun
 mkdir -p targets
 ../net-snmp/maketarget ${TARGETNAME64})

cd $TARGET64
./configure     --with-sys-contact=root \
                --with-sys-location="" \
                --with-logfile=/var/log/snmpd.log \
                --with-persistent-directory=/var/sma_snmp \
                --with-default-snmp-version=3 \
                --enable-shared=yes \
                --enable-developer=yes \
                --with-libs=-ldl \
                --with-defaults=no \
                --prefix="%{_basedir}" \
                --mandir="%{_mandir}" \
                --enable-ipv6 \
                --datadir=/etc/sma \
                --with-mibdirs=/etc/sma/snmp/mibs \
                --with-cc="${CC}" \
                --enable-agentx-dom-sock-only \
                --with-mib-modules="host disman/event-mib ucd-snmp/diskio" \
                --without-openssl \
                --with-transports="UDP UDPIPv6 TCPIPv6 TCP" \
                --with-cflags="${CFLAGS}" \
                --with-pkcs="%{_libdir}" \
                --with-ldflags="-R%{_libdir} ${LDFLAGS}" \
                --libdir="%{_libdir}"

/usr/bin/make

#
# Patch up DESTDIR support
#
find . -name Makefile | while read mf
do
	if [ ! -f ${mf}.orig ]
	then
		cp ${mf} ${mf}.orig
	fi
	cat ${mf}.orig | sed '{
	s|^prefix[ 	]*=[ ]*/usr|prefix = $(DESTDIR)/usr|
	s|^exec_prefix[ 	]*=[ ]*/usr|exec_prefix = $(DESTDIR)/usr|
	s|^libdir[ 	]*=[ ]*/usr|libdir = $(DESTDIR)/usr|
	s|^mandir[ 	]*=[ ]*/usr|mandir = $(DESTDIR)/usr|
	s|^datadir[ 	]*=[ ]*/etc|datadir = $(DESTDIR)/etc|
	s|^persistentdir[ 	]*=[ ]*/var|persistentdir = $(DESTDIR)/var|
	s|^PERSISTENT_DIRECTORY[ 	]*=[ ]*/var|PERSISTENT_DIRECTORY = $(DESTDIR)/var|
	s|^UCDPERSISTENT_DIRECTORY[ 	]*=[ ]*/var|UCDPERSISTENT_DIRECTORY = $(DESTDIR)/var|
	}' > ${mf}
done

t64=${RPM_BUILD_DIR}/%{name}-%{version}/sma-64/net-snmp/${TARGET64}
export LD_LIBRARY_PATH="${t64}/agent/.libs:${t64}/agent/helpers/.libs:${t64}/snmplib/.libs"
/usr/bin/make install DESTDIR=$RPM_BUILD_ROOT
unset LD_LIBRARY_PATH
/usr/ucb/install -m 0644 include/net-snmp/system/solaris2.11.h ${RPM_BUILD_ROOT}%{_includedir}/net-snmp/system

cd ../../../sun/${TARGET64}
/usr/bin/make CC=${CC} ARCH=${BUILDSUNISA64} ROOT=${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_basedir}/lib/sma_snmp
/usr/bin/make install CC=${CC} ARCH=${BUILDSUNISA64} ROOT=${RPM_BUILD_ROOT}

if [ -n "$EXTRA_TARGETS" ]
then
	/usr/ucb/install -d -m 0755 ${RPM_BUILD_ROOT}%{_sbindir}/%{_arch64}
fi

if [ "$MACH" = "i386" ]
then
	for trg in $EXTRA_TARGETS
	do
		outp=`echo $trg | cut -f1 -d":"`
		src=`echo $trg | cut -f2 -d":"`
		mv ${RPM_BUILD_ROOT}%{_sbindir}/${outp} ${RPM_BUILD_ROOT}%{_sbindir}/%{_arch64}
	done
fi

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

mkdir -p ${RPM_BUILD_ROOT}/usr/sfw/bin
mv ${RPM_BUILD_ROOT}%{_basedir}/bin/net-snmp-config ${RPM_BUILD_ROOT}%{_basedir}/bin/net-snmp-config-64
chmod 0755 ${RPM_BUILD_ROOT}%{_basedir}/bin/net-snmp-config-64
(cd ${RPM_BUILD_ROOT}/usr/sfw/bin
 ln -s ../../..%{_basedir}/bin/net-snmp-config-64)

%endif

LDFLAGS="${LDFLAGS32} ${XARCH}"
CFLAGS="-xstrconst -Kpic ${XARCH}"

cd ${RPM_BUILD_DIR}/%{name}-%{version}/sma
(cd net-snmp
 %patch1 -p1
 %patch2 -p1
 %patch3 -p1
 %patch4 -p1
 %patch5 -p1
)

(cd sun
 %patch6 -p1
 %patch7 -p1
)

cd net-snmp
mkdir -p targets
./maketarget ${TARGETNAME32}

(cd ../sun
 mkdir -p targets
 ../net-snmp/maketarget ${TARGETNAME32})

cd $TARGET32
./configure     --with-sys-contact=root \
                --with-sys-location="" \
                --with-logfile=/var/log/snmpd.log \
                --with-persistent-directory=/var/sma_snmp \
                --with-default-snmp-version=3 \
                --enable-shared=yes \
                --enable-developer=yes \
                --with-libs=-ldl \
                --with-defaults=no \
                --prefix="%{_basedir}" \
                --mandir="%{_mandir}" \
                --enable-ipv6 \
                --datadir=/etc/sma \
                --with-mibdirs=/etc/sma/snmp/mibs \
                --with-cc="${CC}" \
                --enable-agentx-dom-sock-only \
                --with-mib-modules="host disman/event-mib ucd-snmp/diskio" \
                --without-openssl \
                --with-transports="UDP UDPIPv6 TCPIPv6 TCP" \
                --with-cflags="${CFLAGS}" \
                --with-ldflags="-R%{_libdir} ${LDFLAGS}" \
                --with-perl-modules=yes

/usr/bin/make

#
# Patch up DESTDIR support
#
find . -name Makefile | while read mf
do
	if [ ! -f ${mf}.orig ]
	then
		cp ${mf} ${mf}.orig
	fi
	cat ${mf}.orig | sed '{
	s|^prefix[ 	]*=[ ]*/usr|prefix = $(DESTDIR)/usr|
	s|^exec_prefix[ 	]*=[ ]*/usr|exec_prefix = $(DESTDIR)/usr|
	s|^libdir[ 	]*=[ ]*/usr|libdir = $(DESTDIR)/usr|
	s|^mandir[ 	]*=[ ]*/usr|mandir = $(DESTDIR)/usr|
	s|^datadir[ 	]*=[ ]*/etc|datadir = $(DESTDIR)/etc|
	s|^persistentdir[ 	]*=[ ]*/var|persistentdir = $(DESTDIR)/var|
	s|^PERSISTENT_DIRECTORY[ 	]*=[ ]*/var|PERSISTENT_DIRECTORY = $(DESTDIR)/var|
	s|^UCDPERSISTENT_DIRECTORY[ 	]*=[ ]*/var|UCDPERSISTENT_DIRECTORY = $(DESTDIR)/var|
	s|^DESTDIR = |DESTDIR = $(DSTDIR)|
	}' > ${mf}
done

t32=${RPM_BUILD_DIR}/%{name}-%{version}/sma/net-snmp/${TARGET32}
export LD_LIBRARY_PATH="${t32}/agent/.libs:${t32}/agent/helpers/.libs:${t32}/snmplib/.libs"

if [ "$MACH" = "i386" ]
then
	/usr/bin/make install DESTDIR=$RPM_BUILD_ROOT DSTDIR=$RPM_BUILD_ROOT
else
	/usr/bin/make installlibs DESTDIR=$RPM_BUILD_ROOT DSTDIR=$RPM_BUILD_ROOT
	/usr/ucb/install -m 0755 net-snmp-config ${RPM_BUILD_ROOT}%{_bindir}
fi
unset LD_LIBRARY_PATH

/usr/ucb/install -m 0444 perl/blib/man3/* ${PERLMAN3DIR}
cd ../../../sun/${TARGET32}
/usr/bin/make CC=${CC} ARCH=${BUILDSUNISA32} ROOT=${RPM_BUILD_ROOT}
/usr/bin/make install CC=${CC} ARCH=${BUILDSUNISA32} ROOT=${RPM_BUILD_ROOT}

if [ "$MACH" = "i386" ]
then
	/usr/bin/make install CC=${CC} ARCH=${BUILDSUNISA32} ROOT=${RPM_BUILD_ROOT}
	/usr/ucb/install -d -m 0755 ${RPM_BUILD_ROOT}%{_sbindir}/${MACH32}
	for trg in $EXTRA_TARGETS
	do
		outp=`echo $trg | cut -f1 -d":"`
		src=`echo $trg | cut -f2 -d":"`
		mv ${RPM_BUILD_ROOT}%{_sbindir}/${outp} ${RPM_BUILD_ROOT}%{_sbindir}/${MACH32}/${outp}
		${CC} ${CFLAGS} -o ${outp} ${src}
		/usr/ucb/install -m 0555 ${outp} ${RPM_BUILD_ROOT}%{_sbindir}
	done
fi

mkdir -p ${RPM_BUILD_ROOT}/lib/svc/method
mkdir -p ${RPM_BUILD_ROOT}/etc/sma/snmp
mkdir -p ${RPM_BUILD_ROOT}/etc/init.d
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/application/management
/usr/ucb/install -m 0555 %{SOURCE12} ${RPM_BUILD_ROOT}/lib/svc/method
/usr/ucb/install -m 0600 %{SOURCE10} ${RPM_BUILD_ROOT}/etc/sma/snmp
/usr/ucb/install -m 0444 %{SOURCE8} ${RPM_BUILD_ROOT}/var/svc/manifest/application/management
/usr/ucb/install -m 0444 %{SOURCE7} ${RPM_BUILD_ROOT}/var/svc/manifest/application/management
/usr/ucb/install -m 0444 %{SOURCE3} ${RPM_BUILD_ROOT}/etc/init.d
mv ${RPM_BUILD_ROOT}%{_basedir}/bin/mib2c ${RPM_BUILD_ROOT}%{_basedir}/bin/mib2c.perl
chmod 0555 ${RPM_BUILD_ROOT}%{_basedir}/bin/mib2c.perl
/usr/ucb/install -m 0555 %{SOURCE5} ${RPM_BUILD_ROOT}%{_basedir}/bin

mv ${RPM_BUILD_ROOT}%{_basedir}/bin/net-snmp-config ${RPM_BUILD_ROOT}%{_basedir}/bin/net-snmp-config-32
chmod 0755 ${RPM_BUILD_ROOT}%{_basedir}/bin/net-snmp-config-32
(cd ${RPM_BUILD_ROOT}/usr/sfw/bin
 ln -s ../../..%{_basedir}/bin/net-snmp-config-32)

(cd ${RPM_BUILD_ROOT}%{_basedir}/bin
 ln -s net-snmp-config-${SMADEFBITS} net-snmp-config
 ln -s snmptrap snmpinform)

mkdir -p ${RPM_BUILD_ROOT}/usr/sfw/sbin/${MACH64}
mkdir -p ${RPM_BUILD_ROOT}/usr/sfw/sbin/${MACH32}
(cd ${RPM_BUILD_ROOT}/usr/sfw/sbin
 ln -s ../../..%{_basedir}/sbin/snmpd
 ln -s ../../..%{_basedir}/sbin/snmptrapd
 cd ${MACH32}
 ln -s ../../../..%{_basedir}/sbin/${MACH32}/snmpd
 ln -s ../../../..%{_basedir}/sbin/${MACH32}/snmptrapd
 cd ../${MACH64}
 ln -s ../../../..%{_basedir}/sbin/${MACH64}/snmpd
 ln -s ../../../..%{_basedir}/sbin/${MACH64}/snmptrapd)

(cd ${RPM_BUILD_ROOT}/usr/sfw/bin
 for prg in mib2c mib2c.perl snmpdelta snmptable snmptest fixproc snmpbulkget \
     snmpbulkwalk snmpconf snmpdf snmpget snmpgetnext snmpinform snmpnetstat \
     snmpset snmpstatus snmptranslate snmptrap snmpusm snmpvacm snmpwalk
 do
 	ln -s ../../..%{_basedir}/bin/$prg
 done)

mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/sma_snmp/html
(cd ${RPM_BUILD_ROOT}%{_docdir}/sma_snmp/html
 tar xf %{SOURCE2}
 chmod 0644 *)

rm -f ${RPM_BUILD_ROOT}%{_basedir}/lib/*.a
rm -f ${RPM_BUILD_ROOT}%{_basedir}/lib/*.la
mv ${RPM_BUILD_ROOT}%{_basedir}/perl5/site_perl ${RPM_BUILD_ROOT}%{_basedir}/perl5/vendor_perl
 
find ${RPM_BUILD_ROOT} -name perllocal.pod | xargs rm -f

%install
echo "Build and install done in same SPEC target 'build'."

%clean
rm -rf $RPM_BUILD_ROOT

%iclass initd -f i.initd
%iclass preserve -f i.preserve

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_sbindir}
%dir %attr (0755, root, bin) %{_basedir}/sfw
%dir %attr (0755, root, bin) %{_basedir}/sfw/sbin
%dir %attr (0755, root, bin) %{_sbindir}/i86
%dir %attr (0755, root, bin) %{_basedir}/sfw/sbin/i86
%attr (0755, root, bin) %{_sbindir}/i86/snmpd
%attr (0755, root, bin) %{_sbindir}/i86/snmptrapd
%attr (0755, root, bin) %{_sbindir}/snmpd
%attr (0755, root, bin) %{_sbindir}/snmptrapd
%attr (0755, root, bin) %{_basedir}/sfw/sbin/snmpd
%attr (0755, root, bin) %{_basedir}/sfw/sbin/snmptrapd
%attr (0755, root, bin) %{_basedir}/sfw/sbin/i86/snmpd
%attr (0755, root, bin) %{_basedir}/sfw/sbin/i86/snmptrapd

%dir %attr (0755, root, bin) %{_basedir}/lib
%attr (0755, root, bin) %{_basedir}/lib/libnetsnmp.so.5.0.9
%attr (0755, root, bin) %{_basedir}/lib/libnetsnmpagent.so.5.0.9
%attr (0755, root, bin) %{_basedir}/lib/libnetsnmphelpers.so.5.0.9
%attr (0755, root, bin) %{_basedir}/lib/libnetsnmpmibs.so.5.0.9
%attr (0755, root, bin) %{_basedir}/lib/libnetsnmp.so
%attr (0755, root, bin) %{_basedir}/lib/libnetsnmp.so.5
%attr (0755, root, bin) %{_basedir}/lib/libnetsnmpagent.so
%attr (0755, root, bin) %{_basedir}/lib/libnetsnmpagent.so.5
%attr (0755, root, bin) %{_basedir}/lib/libnetsnmphelpers.so
%attr (0755, root, bin) %{_basedir}/lib/libnetsnmphelpers.so.5
%attr (0755, root, bin) %{_basedir}/lib/libnetsnmpmibs.so
%attr (0755, root, bin) %{_basedir}/lib/libnetsnmpmibs.so.5
%attr (0755, root, bin) %{_basedir}/lib/libseaProxy.so
%attr (0755, root, bin) %{_basedir}/lib/libseaExtensions.so

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_basedir}/lib/%{_arch64}
%dir %attr (0755, root, bin) %{_sbindir}/%{_arch64}
%dir %attr (0755, root, bin) %{_basedir}/sfw/sbin/%{_arch64}
%attr (0755, root, bin) %{_sbindir}/%{_arch64}/snmpd
%attr (0755, root, bin) %{_sbindir}/%{_arch64}/snmptrapd
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libnetsnmp.so.5.0.9
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libnetsnmpagent.so.5.0.9
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libnetsnmphelpers.so.5.0.9
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libnetsnmpmibs.so.5.0.9
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libseaProxy.so
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libseaExtensions.so
%attr (0755, root, bin) %{_basedir}/sfw/sbin/%{_arch64}/snmpd
%attr (0755, root, bin) %{_basedir}/sfw/sbin/%{_arch64}/snmptrapd
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libnetsnmp.so
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libnetsnmp.so.5
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libnetsnmpagent.so
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libnetsnmpagent.so.5
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libnetsnmphelpers.so
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libnetsnmphelpers.so.5
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libnetsnmpmibs.so
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libnetsnmpmibs.so.5
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/net-snmp
%{_includedir}/net-snmp/*

%files -n SUNWsmcmd
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_basedir}/bin
%dir %attr (0755, root, bin) %{_basedir}/sfw
%dir %attr (0755, root, bin) %{_basedir}/sfw/bin
%dir %attr (0755, root, bin) %{_basedir}/lib
%dir %attr (0755, root, bin) %{_basedir}/lib/sma_snmp
%dir %attr (0755, root, bin) %{_basedir}/perl5
%dir %attr (0755, root, bin) %{_basedir}/perl5/vendor_perl
%dir %attr (0755, root, bin) %{_basedir}/perl5/vendor_perl/5.8.4
%dir %attr (0755, root, bin) %{_basedir}/perl5/5.8.4
%dir %attr (0755, root, bin) %{_basedir}/perl5/5.8.4/man
%dir %attr (0755, root, bin) %{_basedir}/perl5/5.8.4/man/man3
%dir %attr (0755, root, bin) %{_basedir}/perl5/5.8.4/lib
%dir %attr (0755, root, bin) %{_basedir}/perl5/5.8.4/lib/i86pc-solaris-64int
%dir %attr (0755, root, bin) %{_basedir}/lib/%{_arch64}

%{_basedir}/lib/sma_snmp/*
%{_basedir}/perl5/5.8.4/man/man3/*
%attr (0755, root, bin) %{_basedir}/bin/mib2c
%attr (0755, root, bin) %{_basedir}/bin/mib2c.perl
%attr (0755, root, bin) %{_basedir}/bin/snmpdelta
%attr (0755, root, bin) %{_basedir}/bin/snmptable
%attr (0755, root, bin) %{_basedir}/bin/snmptest
%attr (0755, root, bin) %{_basedir}/bin/fixproc
%attr (0755, root, bin) %{_basedir}/bin/net-snmp-config-32
%attr (0755, root, bin) %{_basedir}/bin/net-snmp-config-64
%attr (0755, root, bin) %{_basedir}/bin/snmpbulkget
%attr (0755, root, bin) %{_basedir}/bin/snmpbulkwalk
%attr (0755, root, bin) %{_basedir}/bin/snmpconf
%attr (0755, root, bin) %{_basedir}/bin/snmpdf
%attr (0755, root, bin) %{_basedir}/bin/snmpget
%attr (0755, root, bin) %{_basedir}/bin/snmpgetnext
%attr (0755, root, bin) %{_basedir}/bin/snmpnetstat
%attr (0755, root, bin) %{_basedir}/bin/snmpset
%attr (0755, root, bin) %{_basedir}/bin/snmpstatus
%attr (0755, root, bin) %{_basedir}/bin/snmptranslate
%attr (0755, root, bin) %{_basedir}/bin/snmptrap
%attr (0755, root, bin) %{_basedir}/bin/snmpusm
%attr (0755, root, bin) %{_basedir}/bin/snmpvacm
%attr (0755, root, bin) %{_basedir}/bin/snmpwalk
%attr (0755, root, bin) %{_basedir}/bin/traptoemail
%attr (0755, root, bin) %{_basedir}/bin/encode_keychange
%attr (0755, root, bin) %{_basedir}/bin/snmpcheck
%attr (0755, root, bin) %{_basedir}/bin/ipf-mod.pl
%attr (0755, root, bin) %{_basedir}/bin/tkmib
%attr (0755, root, bin) %{_basedir}/lib/libentity.so
%attr (0755, root, bin) %{_basedir}/lib/%{_arch64}/libentity.so
%{_basedir}/bin/snmpinform
%{_basedir}/bin/net-snmp-config

%{_basedir}/sfw/bin/mib2c
%{_basedir}/sfw/bin/mib2c.perl
%{_basedir}/sfw/bin/snmpdelta
%{_basedir}/sfw/bin/snmptable
%{_basedir}/sfw/bin/snmptest
%{_basedir}/sfw/bin/fixproc
%{_basedir}/sfw/bin/net-snmp-config-32
%{_basedir}/sfw/bin/net-snmp-config-64
%{_basedir}/sfw/bin/snmpbulkget
%{_basedir}/sfw/bin/snmpbulkwalk
%{_basedir}/sfw/bin/snmpconf
%{_basedir}/sfw/bin/snmpdf
%{_basedir}/sfw/bin/snmpget
%{_basedir}/sfw/bin/snmpgetnext
%{_basedir}/sfw/bin/snmpnetstat
%{_basedir}/sfw/bin/snmpset
%{_basedir}/sfw/bin/snmpstatus
%{_basedir}/sfw/bin/snmptranslate
%{_basedir}/sfw/bin/snmptrap
%{_basedir}/sfw/bin/snmpusm
%{_basedir}/sfw/bin/snmpvacm
%{_basedir}/sfw/bin/snmpwalk
%{_basedir}/sfw/bin/snmpinform

%ifarch i386 amd64
%dir %attr (0755, root, bin) %{_basedir}/perl5/vendor_perl/5.8.4/i86pc-solaris-64int
%{_basedir}/perl5/vendor_perl/5.8.4/i86pc-solaris-64int/*
%else
%dir %attr (0755, root, bin) %{_basedir}/perl5/vendor_perl/5.8.4/sun4-solaris-64int
%{_basedir}/perl5/vendor_perl/5.8.4/sun4-solaris-64int/*
%endif

%files -n SUNWsmmgr
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/init.d
%dir %attr (0755, root, bin) %{_sysconfdir}/sma
%dir %attr (0755, root, bin) %{_sysconfdir}/sma/snmp
%dir %attr (0755, root, bin) %{_sysconfdir}/sma/snmp/mibs
%dir %attr (0755, root, bin) %{_sysconfdir}/sma/snmp/snmpconf-data
%dir %attr (0755, root, bin) %{_sysconfdir}/sma/snmp/snmpconf-data/snmp-data
%dir %attr (0755, root, bin) %{_sysconfdir}/sma/snmp/snmpconf-data/snmpd-data
%dir %attr (0755, root, bin) %{_sysconfdir}/sma/snmp/snmpconf-data/snmptrapd-data
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application/management
%dir %attr (0755, root, sys) /lib
%dir %attr (0755, root, sys) /lib/svc
%dir %attr (0755, root, sys) /lib/svc/method
%class(initd) %attr (0755, root, sys) %{_sysconfdir}/init.d/init.sma
%config %class(preserve) %attr (0600, root, bin) %{_sysconfdir}/sma/snmp/snmpd.conf
%{_sysconfdir}/sma/snmp/mib2c*
%{_sysconfdir}/sma/snmp/mibs/*
%{_sysconfdir}/sma/snmp/snmpconf-data/snmp-data/*
%{_sysconfdir}/sma/snmp/snmpconf-data/snmpd-data/*
%{_sysconfdir}/sma/snmp/snmpconf-data/snmptrapd-data/*
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/application/management/sma.xml
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/application/management/seaport.xml
%attr (0555, root, bin) /lib/svc/method/svc-sma

%files -n SUNWsmdoc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/sma_snmp
%dir %attr (0755, root, bin) %{_docdir}/sma_snmp/html
%{_docdir}/sma_snmp/html/*

%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man5
%dir %attr (0755, root, bin) %{_mandir}/man8
%dir %attr (0755, root, bin) %{_mandir}/man1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Sun Feb 08 2009 - moinakg@gmail.com
- Fix 64Bit file lists.
* Thu Jan 29 2009 - moinakg@gmail.com
- Initial spec (migrated from SFW gate).

