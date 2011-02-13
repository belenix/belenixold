%define	with_python_version	2.6%{nil}
%define	with_apidocs		0%{nil}
%define popt_version            1.16

%global _usrlibrpm /usr/lib/rpm
%global _rpmhome /usr/lib/rpm

%define	__prefix	%{?_prefix}%{!?_prefix:/usr}
%{?!_lib: %define _lib lib}
%{expand: %%define __share %(if [ -d %{__prefix}/share/man ]; then echo /share ; else echo %%{nil} ; fi)}


Summary: The RPM package management system version 5
Name: rpm5
Version: 5.3.6
Release: 1%{?dist}
Group: System Environment/Base
URL: http://rpm5.org
Source0: http://rpm5.org/files/rpm/rpm-5.3/rpm-%{version}.tar.gz
Source1: http://rpm5.org/files/popt/popt-%{popt_version}.tar.gz
Source3: rpmmacros
Source4: find-info.sh
Source5: install-info.sh
Source6: drvtestadd
License: LGPL
#Requires: fileutils shadow-utils
#Requires: getconf(GNU_LIBPTHREAD_VERSION) = NPTL
Requires: %{name}-libs == %{version}-%{release}
Requires: %{name}-common

# XXX necessary only to drag in /usr/lib/libelf.a, otherwise internal elfutils.
#BuildRequires: elfutils-libelf
#BuildRequires: elfutils-devel
BuildRequires: zlib-devel

#BuildRequires: neon-devel
#BuildRequires: sqlite-devel

#BuildRequires: bzip2-devel >= 1.0
BuildRequires: xz-devel >= 4.999.8
%if "%{with_apidocs}" == "1"
#BuildRequires: doxygen
BuildRequires: graphviz
%endif
#BuildRequires: python-devel >= %{with_python_version}
#BuildRequires: perl >= 2:5.8.0

BuildRoot: %{_tmppath}/%{name}-root

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages. Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package libs
Summary:  Libraries for manipulating RPM packages.
Group: Development/Libraries
# XXX this Provides: is bogus, but getconf(...) needs to be bootstrapped.
#Provides: getconf(GNU_LIBPTHREAD_VERSION) = NPTL
#Requires: getconf(GNU_LIBPTHREAD_VERSION) = NPTL

%description libs
This package contains the RPM shared libraries.

%package devel
Summary:  Development files for manipulating RPM packages.
Group: Development/Libraries
Requires: rpm5 = %{version}-%{release}
Requires: rpm5-libs = %{version}-%{release}
#Requires: neon-devel
#Requires: sqlite-devel
#Requires: getconf(GNU_LIBPTHREAD_VERSION) = NPTL

%description devel
This package contains the RPM C library and header files. These
development files will simplify the process of writing programs that
manipulate RPM packages and databases. These files are intended to
simplify the process of creating graphical package managers or any
other tools that need an intimate knowledge of RPM packages in order
to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package common
Summary: Common RPM paths, scripts, documentation and configuration.
Group: Development/Tools

%description common
The rpm-common package contains paths, scripts, documentation
and configuration common between RPM Package Manager.

%package build
Summary: Scripts and executable programs used to build packages.
Group: Development/Tools
Requires: rpm5 = %{version}-%{release}
#Requires: patch >= 2.5
#Requires: getconf(GNU_LIBPTHREAD_VERSION) = NPTL

%description build
The rpm-build package contains the scripts and executable programs
that are used to build packages using the RPM Package Manager.

%package python
Summary: Python bindings for apps which will manipulate RPM packages.
Group: Development/Libraries
Requires: rpm5 = %{version}-%{release}
Requires: rpm5-libs = %{version}-%{release}
Requires: python >= %{with_python_version}

%description python
The rpm-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.

%prep
%bsetup
gunzip -c %{SOURCE1} | tar xvf - 

%build
PDIR=`pwd`
CFLAGS="%{optflags} -std=gnu99 -I${PDIR}/popt-%{popt_version} -I/usr/include -I/usr/include/mps -fPIC -DPIC"
CXXFLAGS="%{cxx_optflags} -I${PDIR}/popt-%{popt_version} -I/usr/include -I/usr/include/mps -fPIC -DPIC"

%if %{build_64bit}
CFLAGS="$CFLAGS -DHAVE_VA_COPY -DVA_COPY=va_copy"; export CFLAGS
LDFLAGS="-L${PDIR}/popt-%{popt_version}/.libs -m64 -L%{_libdir} -R%{_libdir} -L/usr/lib/mps/%{_arch64} -R/usr/lib/mps/%{_arch64}"

%if %{gcc_compiler}
cat <<EOT1 > gcc
#!/bin/sh
exec ${CC} -m64 "\$@"
EOT1

cat <<EOT2 > g++
#!/bin/sh
exec ${CXX} -m64 "\$@"
EOT2

chmod +x gcc g++
export CC=`pwd`/gcc
export CXX=`pwd`/g++
%endif

%else
LDFLAGS="-L${PDIR}/popt-%{popt_version}/.libs -L%{_libdir} -R%{_libdir} -L/usr/lib/mps -R/usr/lib/mps"
CFLAGS="${CFLAGS} `getconf LFS_CFLAGS`"
CXXFLAGS="${CXXFLAGS} `getconf LFS_CFLAGS`"
%endif

export CFLAGS CXXFLAGS LDFLAGS

cd popt-%{popt_version}
./configure --with-pic --enable-shared=no --enable-static=yes
gmake
cd ..
cd rpm-%{version}

./configure --verbose \
	--prefix=%{_prefix} \
        --bindir='%{_bindir}' \
        --infodir='%{_infodir}' \
        --libdir='%{_libdir}' \
        --localstatedir=%{_localstatedir} \
        --mandir='%{_mandir}' \
        --sysconfdir=%{_sysconfdir} \
        --with-file \
        --with-path-magic=%{_datadir}/misc/magic \
        --with-tcl \
        --with-lua=internal \
        --with-syck=internal \
        --without-readline \
        --without-augeas \
        --with-bzip2 \
        --with-xz \
        --with-zlib \
        --with-python=%{with_python_version} \
        --with-python-inc-dir=%{_includedir}/python2.6 \
        --with-python-lib-dir=%{_libdir32}/python2.6 \
        --without-pythonembed \
        --without-perl --without-perlembed \
        --with-db --with-dbsql --without-db-tools-integrated --without-sqlite \
        --with-beecrypt=internal --with-openssl --with-nss --with-gcrypt \
        --without-keyutils \
        --without-selinux --without-sepol --without-semanage \
        --without-libtasn1 \
        --without-pakchois \
        --without-gnutls \
        --with-neon=internal --without-libproxy --with-expat \
        --with-pcre \
        --enable-utf8 \
        --without-uuid \
        --without-xar \
        --with-xz \
        --with-popt=external \
        --with-pthreads \
        --without-cudf \
        --without-ficl \
        --without-aterm \
        --without-nix \
        --without-bash \
        --without-rc \
        --without-js \
        --without-gpsee \
        --without-ruby \
        --without-squirrel \
        --with-build-extlibdep \
        --with-build-maxextlibdep \
        --without-valgrind \
        --disable-openmp \
        --with-pic \
        --enable-build-pic \
        --enable-build-warnings

# Get rid of visibility for now
[ ! -f lua/luaconf.h.orig ] && cp lua/luaconf.h lua/luaconf.h.orig
cat lua/luaconf.h.orig | sed 's/__attribute__((visibility("hidden")))//' > lua/luaconf.h

#
# Fix dirfd handling in fts
#
[ ! -f rpmio/fts.c.orig ] && cp rpmio/fts.c rpmio/fts.c.orig
cat rpmio/fts.c.orig | sed '
s/#   define dirfd(dirp)                -1/#include <dirent.h>/' > rpmio/fts.c

[ ! -f tests/Makefile.orig ] && cp tests/Makefile tests/Makefile.orig
cat tests/Makefile.orig | sed '
s/check-local: check-init check-pubkeys/check-local: check-init /
s/check-build check-sign/check-build /' > tests/Makefile

[ ! -f lua/shadow/useradd.c.orig ] && cp lua/shadow/useradd.c lua/shadow/useradd.c.orig
cat lua/shadow/useradd.c.orig | sed '
s%/home%/export/home%' > lua/shadow/useradd.c

gmake -C lua clean || :
gmake -C python clean || :

gmake -j 2 INSTALLMAN3DIR="%{_mandir}/man3"

%if %{with_apidocs}
make apidocs
%endif

%install
rm -rf $RPM_BUILD_ROOT

cd rpm-%{version}
gmake DESTDIR="$RPM_BUILD_ROOT" install

mkdir -p $RPM_BUILD_ROOT/etc/rpm
mkdir -p $RPM_BUILD_ROOT/var/spool/repackage
mkdir -p $RPM_BUILD_ROOT/var/lib/rpm
for dbi in \
	Basenames Conflictname Dirnames Group Installtid Name Packages \
	Providename Provideversion Requirename Requireversion Triggername \
	Filemd5s Pubkeys Sha1header Sigmd5 \
	__db.001 __db.002 __db.003 __db.004 __db.005
do
    touch $RPM_BUILD_ROOT/var/lib/rpm/$dbi
done

(cd ${RPM_BUILD_ROOTT}%{_usrlibrpm}
 cp macros macros.tmp
 cat macros.tmp | sed 's/^%_repackage_all_erasures	1/%_repackage_all_erasures	0/' > macros
 cp macros.rpmbuild macros.rpmbuild.tmp
 cat macros.rpmbuild.tmp | sed 's/^#%_binary_payload	w9.gzdio/%_binary_payload	w6.xzio/' > macros.rpmbuild
 rm -f macros.tmp macros.rpmbuild.tmp)

mkdir -p %{_usrlibrpm}/%{_arch}-solaris2.11/
cp %{SOURCE3} %{_usrlibrpm}/%{_arch}-solaris2.11/macros
cp %{SOURCE4} %{_usrlibrpm}
cp %{SOURCE5} %{_usrlibrpm}
cp %{SOURCE6} %{_usrlibrpm}

chmod a+x %{_usrlibrpm}/find-info.sh %{_usrlibrpm}/install-info.sh %{_usrlibrpm}/drvtestadd

%find_lang rpm

%if %{with_apidocs}
gzip -9n apidocs/man/man*/* || :
%endif

# Get rid of unpackaged files
{ cd $RPM_BUILD_ROOT

  rm -f .%{_rpmhome}/{Specfile.pm,cpanflute,cpanflute2,rpmdiff,rpmdiff.cgi,sql.prov,sql.req,tcl.req,trpm}

  rm -f .%{_mandir}/man8/rpmcache.8*
  rm -f .%{_mandir}/man8/rpmgraph.8*
  rm -f .%{_mandir}/ja/man8/rpmcache.8*
  rm -f .%{_mandir}/ja/man8/rpmgraph.8*
  rm -f .%{_mandir}/pl/man8/rpmcache.8*
  rm -f .%{_mandir}/pl/man8/rpmgraph.8*
  rm -rf .%{_mandir}/{fr,ko}

  rm -f .%{_includedir}/popt.h
  rm -f .%{_libdir}/libpopt.*
  rm -f .%{_libdir}/pkgconfig/popt.pc
  rm -f .%{_datadir}/locale/*/LC_MESSAGES/popt.mo
  rm -f .%{_mandir}/man3/popt.3

  rm -f .%{_mandir}/man1/xar.1*
  rm -f .%{_bindir}/xar
  rm -rf .%{_includedir}/xar
  rm -f .%{_libdir}/libxar*

  rm -f .%{_bindir}/lz*
  rm -f .%{_bindir}/unlzma
  rm -f .%{_bindir}/unxz
  rm -f .%{_bindir}/xz*
  rm -rf .%{_includedir}/lzma*
  rm -f .%{_mandir}/man1/lz*.1
  rm -f .%{_libdir}/pkgconfig/liblzma*

  rm -f .%{_libdir}/python%{with_python_version}/site-packages/*.{a,la}
  rm -f .%{_libdir}/python%{with_python_version}/site-packages/rpm/*.{a,la}
}

%clean
rm -rf $RPM_BUILD_ROOT

%define	rpmattr		%attr(0755, root, bin)
%define	rpmdbattr %attr(0644, root, bin) %verify(not md5 size mtime) %ghost %config(missingok,noreplace)

%files
%pubkey pubkeys/JBJ-GPG-KEY

%rpmattr	%{_bindir}/rpm
%rpmattr	%{_bindir}/rpmconstant

%rpmattr %dir	%{_rpmhome}
%rpmattr	%{_rpmhome}/rpm.*
%rpmattr	%{_rpmhome}/tgpg
%attr(0644, root, bin)	%{_rpmhome}/macros
%attr(0644, root, bin)	%{_rpmhome}/rpmpopt

%rpmattr	%{_rpmhome}/rpmdb_loadcvt
###%rpmattr	%{_rpmhome}/magic
###%rpmattr	%{_rpmhome}/magic.mgc
###%rpmattr	%{_rpmhome}/magic.mime
###%rpmattr	%{_rpmhome}/magic.mime.mgc
%rpmattr	%{_rpmhome}/rpm2cpio
%rpmattr	%{_rpmhome}/vcheck

%rpmattr	%{_rpmhome}/helpers

%rpmattr	%{_rpmhome}/qf

%rpmattr	%{_rpmhome}/cpuinfo.yaml

%rpmattr %dir	%{_rpmhome}/bin
###%rpmattr	%{_rpmhome}/bin/db_*
###%rpmattr	%{_rpmhome}/bin/grep
%rpmattr	%{_rpmhome}/bin/mtree
%rpmattr	%{_rpmhome}/bin/rpmkey
%rpmattr	%{_rpmhome}/bin/rpmrepo
%rpmattr	%{_rpmhome}/bin/rpmspecdump
%rpmattr	%{_rpmhome}/bin/wget

%rpmattr %dir	%{_rpmhome}/lib

%files common -f rpm.lang
%doc CHANGES doc/manual/[a-z]*
%rpmattr	%{_bindir}/rpm2cpio
%rpmattr	%{_bindir}/gendiff
%dir			/etc/rpm
%attr(0755, root, bin)	%dir /var/lib/rpm
%rpmdbattr		/var/lib/rpm/*
%attr(0755, root, bin)	%dir /var/spool/repackage

%attr(0755, root, bin)	%dir %{_usrlibrpm}
%ifarch i386 i486 i586 i686 athlon pentium3 pentium4 x86_64
%attr(-, root, bin)		%{_usrlibrpm}/i[3456]86*
%attr(-, root, bin)		%{_usrlibrpm}/athlon*
%attr(-, root, bin)		%{_usrlibrpm}/pentium*
%attr(-, root, bin)		%{_usrlibrpm}/x86_64*
%endif
%ifarch alpha alphaev5 alphaev56 alphapca56 alphaev6 alphaev67
%attr(-, root, bin)		%{_usrlibrpm}/alpha*
%endif
%ifarch sparc sparcv8 sparcv9 sparc64
%attr(-, root, bin)		%{_usrlibrpm}/sparc*
%endif
%ifarch ia64
%attr(-, root, bin)		%{_usrlibrpm}/ia64*
%endif
%ifarch powerpc ppc ppciseries ppcpseries ppcmac ppc64
%attr(-, root, bin)		%{_usrlibrpm}/ppc*
%endif
%ifarch s390 s390x
%attr(-, root, bin)		%{_usrlibrpm}/s390*
%endif
%ifarch armv3l armv4b armv4l
%attr(-, root, bin)		%{_usrlibrpm}/armv[34][lb]*
%endif
%ifarch armv5teb armv5tel
%attr(-, root, bin)		%{_usrlibrpm}/armv[345]*
%endif
%ifarch mips mipsel
%attr(-, root, bin)		%{_usrlibrpm}/mips*
%endif

%attr(-, root, bin)		%{_usrlibrpm}/noarch*

%dir %{__prefix}/src/rpm
%dir %{__prefix}/src/rpm/BUILD
%dir %{__prefix}/src/rpm/SPECS
%dir %{__prefix}/src/rpm/SOURCES
%dir %{__prefix}/src/rpm/SRPMS
%dir %{__prefix}/src/rpm/RPMS
%{__prefix}/src/rpm/RPMS/*

%{_mandir}/man8/rpm.8*
%{_mandir}/man8/rpm2cpio.8*
%lang(ja)	%{_mandir}/ja/man8/rpm.8*
%lang(ja)	%{_mandir}/ja/man8/rpm2cpio.8*
#%lang(ko)	%{_mandir}/ko/man8/rpm.8*
#%lang(ko)	%{_mandir}/ko/man8/rpm2cpio.8*
%lang(pl)	%{_mandir}/pl/man8/rpm.8*
%lang(pl)	%{_mandir}/pl/man8/rpm2cpio.8*
%lang(ru)	%{_mandir}/ru/man8/rpm.8*
%lang(ru)	%{_mandir}/ru/man8/rpm2cpio.8*
%lang(sk)	%{_mandir}/sk/man8/rpm.8*

%{_mandir}/man1/gendiff.1*
%{_mandir}/man1/rpmgrep.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmconstant.8*
###%{_mandir}/man8/rpmcache.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmmtree.8*
#%lang(ja)	%{_mandir}/ja/man1/gendiff.1*
%lang(ja)	%{_mandir}/ja/man8/rpmbuild.8*
#%lang(ja)	%{_mandir}/ja/man8/rpmdeps.8*
#%lang(ko)	%{_mandir}/ko/man1/gendiff.1*
#%lang(ko)	%{_mandir}/ko/man8/rpmbuild.8*
#%lang(ko)	%{_mandir}/ko/man8/rpmdeps.8*
%lang(pl)	%{_mandir}/pl/man1/gendiff.1*
%lang(pl)	%{_mandir}/pl/man8/rpmbuild.8*
%lang(pl)	%{_mandir}/pl/man8/rpmdeps.8*
#%lang(ru)	%{_mandir}/ru/man1/gendiff.1*
#%lang(ru)	%{_mandir}/ru/man8/rpmbuild.8*
#%lang(ru)	%{_mandir}/ru/man8/rpmdeps.8*
#%lang(sk)	%{_mandir}/sk/man1/gendiff.1*
#%lang(sk)	%{_mandir}/sk/man8/rpmbuild.8*
#%lang(sk)	%{_mandir}/sk/man8/rpmdeps.8*

%files libs
%{_libdir}/librpm-5.3.so
%{_libdir}/librpmconstant-5.3.so
%{_libdir}/librpmdb-5.3.so
%{_libdir}/librpmio-5.3.so
%{_libdir}/librpmmisc-5.3.so
%{_libdir}/librpmbuild-5.3.so

###%{_rpmhome}/lib/libxar.so.*
###%{_rpmhome}/lib/libjs.so.*
###%{_rpmhome}/lib/librpmjsm.so.*
###%{_rpmhome}/lib/rpmjsm.so

%files build
%rpmattr	%{_bindir}/rpmbuild

%rpmattr	%{_rpmhome}/brp-*
%rpmattr	%{_rpmhome}/check-files
%rpmattr	%{_rpmhome}/cross-build
%rpmattr	%{_rpmhome}/find-debuginfo.sh
%rpmattr	%{_rpmhome}/find-lang.sh
%rpmattr	%{_rpmhome}/find-prov.pl
%rpmattr	%{_rpmhome}/find-provides.perl
%rpmattr	%{_rpmhome}/find-req.pl
%rpmattr	%{_rpmhome}/find-requires.perl
%rpmattr	%{_rpmhome}/getpo.sh
%rpmattr	%{_rpmhome}/http.req
%rpmattr	%{_rpmhome}/javadeps.sh
%rpmattr	%{_rpmhome}/mono-find-provides
%rpmattr	%{_rpmhome}/mono-find-requires

%rpmattr	%{_rpmhome}/executabledeps.sh
%rpmattr	%{_rpmhome}/libtooldeps.sh
%rpmattr	%{_rpmhome}/osgideps.pl
%rpmattr	%{_rpmhome}/perldeps.pl
%rpmattr	%{_rpmhome}/perl.prov
%rpmattr	%{_rpmhome}/perl.req
%rpmattr	%{_rpmhome}/php.prov
%rpmattr	%{_rpmhome}/php.req
%rpmattr	%{_rpmhome}/pkgconfigdeps.sh
%rpmattr	%{_rpmhome}/pythondeps.sh

%rpmattr	%{_rpmhome}/gem_helper.rb

%rpmattr	%{_rpmhome}/bin/debugedit
%rpmattr	%{_rpmhome}/bin/rpmcache
%rpmattr	%{_rpmhome}/bin/rpmcmp
%rpmattr	%{_rpmhome}/bin/rpmdeps
%rpmattr	%{_rpmhome}/bin/rpmdigest
%rpmattr	%{_rpmhome}/bin/abi-compliance-checker.pl
%rpmattr	%{_rpmhome}/bin/api-sanity-autotest.pl
%rpmattr	%{_rpmhome}/bin/chroot
%rpmattr	%{_rpmhome}/bin/cp
%rpmattr	%{_rpmhome}/bin/dbsql
%rpmattr	%{_rpmhome}/bin/find
%rpmattr	%{_rpmhome}/bin/install-sh
%rpmattr	%{_rpmhome}/bin/lua
%rpmattr	%{_rpmhome}/bin/luac
%rpmattr	%{_rpmhome}/bin/mkinstalldirs
%rpmattr	%{_rpmhome}/bin/rpmlua
%rpmattr	%{_rpmhome}/bin/rpmluac
%rpmattr	%{_rpmhome}/bin/sqlite3

%rpmattr	%{_rpmhome}/lib/liblua.a
%rpmattr	%{_rpmhome}/lib/liblua.la

%rpmattr %dir	%{_rpmhome}/macros.d
%rpmattr	%{_rpmhome}/macros.d/cmake
%rpmattr	%{_rpmhome}/macros.d/java
%rpmattr	%{_rpmhome}/macros.d/libtool
%rpmattr	%{_rpmhome}/macros.d/mandriva
%rpmattr	%{_rpmhome}/macros.d/mono
%rpmattr	%{_rpmhome}/macros.d/perl
%rpmattr	%{_rpmhome}/macros.d/php
%rpmattr	%{_rpmhome}/macros.d/pkgconfig
%rpmattr	%{_rpmhome}/macros.d/python
%rpmattr	%{_rpmhome}/macros.d/ruby
%rpmattr	%{_rpmhome}/macros.d/selinux
%rpmattr	%{_rpmhome}/macros.d/tcl
%rpmattr	%{_rpmhome}/macros.rpmbuild

#%rpmattr	%{_rpmhome}/symclash.*
%rpmattr	%{_rpmhome}/u_pkg.sh
%rpmattr	%{_rpmhome}/vpkg-provides.sh
%rpmattr	%{_rpmhome}/vpkg-provides2.sh

%files python
%{_libdir}/python%{with_python_version}/site-packages/rpm

%files devel
%if %{with_apidocs}
%doc 
%endif
%{_includedir}/rpm
%{_libdir}/librpm.a
%{_libdir}/librpm.la
%{_libdir}/librpm.so
%{_libdir}/librpmconstant.a
%{_libdir}/librpmconstant.la
%{_libdir}/librpmconstant.so
%{_libdir}/librpmdb.a
%{_libdir}/librpmdb.la
%{_libdir}/librpmdb.so
%{_libdir}/librpmio.a
%{_libdir}/librpmio.la
%{_libdir}/librpmio.so
%{_libdir}/librpmmisc.a
%{_libdir}/librpmmisc.la
%{_libdir}/librpmmisc.so
%{_libdir}/librpmbuild.a
%{_libdir}/librpmbuild.la
%{_libdir}/librpmbuild.so
%{_libdir}/pkgconfig/rpm.pc

###%{_rpmhome}/lib/libxar.a
###%{_rpmhome}/lib/libxar.la
###%{_rpmhome}/lib/libxar.so
###%{_rpmhome}/lib/libjs.a
###%{_rpmhome}/lib/libjs.la
###%{_rpmhome}/lib/libjs.so
###%{_rpmhome}/lib/librpmjsm.a
###%{_rpmhome}/lib/librpmjsm.la
###%{_rpmhome}/lib/librpmjsm.so

%changelog
* Sat Oct 23 2010 Jeff Johnson <jbj@rpm5.org> - 5.3.5-0.1
- resurrect rpm.spec.

* Tue Jan 22 2008 Jeff Johnson <jbj@rpm5.org> - 5.1-0.1
- resurrect rpm.spec.
