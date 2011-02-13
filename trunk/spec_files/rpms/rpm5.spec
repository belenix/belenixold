%define	with_python_version	2.6%{nil}
%define	with_apidocs		0%{nil}
%define popt_version            1.16

%global __usrlibrpm /usr/lib/rpm
%global __rpmhome /usr/lib/rpm

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
        --with-python-inc-dir=%{_includedir}/python%{with_python_version} \
        --with-python-lib-dir=%{_libdir32}/python%{with_python_version}/vendor-packages \
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

(cd ${RPM_BUILD_ROOT}%{__usrlibrpm}
 cp macros macros.tmp
 cat macros.tmp | sed 's/^%%_repackage_all_erasures	1/%%_repackage_all_erasures	0/' > macros
 cp macros.rpmbuild macros.rpmbuild.tmp
 cat macros.rpmbuild.tmp | sed 's/^#%%_binary_payload	w9.gzdio/%%_binary_payload	w6.xzio/' > macros.rpmbuild
 rm -f macros.tmp macros.rpmbuild.tmp)

mkdir -p ${RPM_BUILD_ROOT}%{__usrlibrpm}/%{_arch}-solaris2.11/
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{__usrlibrpm}/%{_arch}-solaris2.11/macros
cp %{SOURCE4} ${RPM_BUILD_ROOT}%{__usrlibrpm}
cp %{SOURCE5} ${RPM_BUILD_ROOT}%{__usrlibrpm}
cp %{SOURCE6} ${RPM_BUILD_ROOT}%{__usrlibrpm}

chmod a+x ${RPM_BUILD_ROOT}%{__usrlibrpm}/find-info.sh \
	${RPM_BUILD_ROOT}%{__usrlibrpm}/install-info.sh \
	${RPM_BUILD_ROOT}%{__usrlibrpm}/drvtestadd

mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/rpm-%{version}
cp -rp CHANGES doc/manual/[a-z]* ${RPM_BUILD_ROOT}%{_docdir}/rpm-%{version}

mkdir ${RPM_BUILD_ROOT}%{_libdir32}/python%{with_python_version}/vendor-packages/rpm/%{_arch64}
mv ${RPM_BUILD_ROOT}%{_libdir32}/python%{with_python_version}/vendor-packages/rpm/*.so* \
	${RPM_BUILD_ROOT}%{_libdir32}/python%{with_python_version}/vendor-packages/rpm/%{_arch64}

%if %{build_64bit}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir32}
(cd ${RPM_BUILD_ROOT}%{_bindir}
 for f in *
 do
   (cd ..; ln -s %{_arch64}/${f})
 done)
%endif

%find_lang rpm

%if %{with_apidocs}
gzip -9n apidocs/man/man*/* || :
%endif

# Get rid of unpackaged files
{ cd $RPM_BUILD_ROOT

  rm -f .%{__rpmhome}/{Specfile.pm,cpanflute,cpanflute2,rpmdiff,rpmdiff.cgi,sql.prov,sql.req,tcl.req,trpm}

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
  rm -f .%{_libdir}/*.la

  rm -f .%{_libdir32}/python%{with_python_version}/vendor-packages/*.{a,la}
  rm -f .%{_libdir32}/python%{with_python_version}/vendor-packages/rpm/*.{a,la}
}

%clean
rm -rf $RPM_BUILD_ROOT

%define	rpmattr		%attr(0755, root, bin)
%define	rpmdbattr %attr(0644, root, bin) %verify(not md5 size mtime) %ghost %config(missingok,noreplace)

%files
%rpmattr	%{_bindir}/rpm
%rpmattr	%{_bindir}/rpmconstant

%if %{build_64bit}
%{_bindir32}/rpm
%{_bindir32}/rpmconstant
%endif

%rpmattr %dir	%{__rpmhome}
%rpmattr	%{__rpmhome}/rpm.*
%rpmattr	%{__rpmhome}/tgpg
%attr(0644, root, bin)	%{__rpmhome}/macros
%attr(0644, root, bin)	%{__rpmhome}/rpmpopt
%rpmattr %dir    %{__rpmhome}/%{_arch}-solaris2.11
%attr(0644, root, bin)  %{__rpmhome}/%{_arch}-solaris2.11/macros

%rpmattr	%{__rpmhome}/rpmdb_loadcvt
###%rpmattr	%{__rpmhome}/magic
###%rpmattr	%{__rpmhome}/magic.mgc
###%rpmattr	%{__rpmhome}/magic.mime
###%rpmattr	%{__rpmhome}/magic.mime.mgc
%rpmattr	%{__rpmhome}/rpm2cpio
%rpmattr	%{__rpmhome}/vcheck

%rpmattr	%{__rpmhome}/helpers

%rpmattr	%{__rpmhome}/qf

%rpmattr	%{__rpmhome}/cpuinfo.yaml

%rpmattr %dir	%{__rpmhome}/bin
###%rpmattr	%{__rpmhome}/bin/db_*
###%rpmattr	%{__rpmhome}/bin/grep
%rpmattr	%{__rpmhome}/bin/mtree
%rpmattr	%{__rpmhome}/bin/rpmrepo
%rpmattr	%{__rpmhome}/bin/rpmspecdump
%rpmattr	%{__rpmhome}/bin/wget
%rpmattr	%{__rpmhome}/drvtestadd
%rpmattr	%{__rpmhome}/find-info.sh
%rpmattr	%{__rpmhome}/install-info.sh
%rpmattr	%{__rpmhome}/dbconvert.sh

%rpmattr %dir	%{__rpmhome}/lib

%files common -f rpm-%{version}/rpm.lang
%dir %rpmattr	%{_docdir}/rpm-%{version}
%attr(0666, root, other) %{_docdir}/rpm-%{version}/*
%rpmattr	%{_bindir}/rpm2cpio
%rpmattr	%{_bindir}/gendiff

%if %{build_64bit}
%{_bindir32}/rpm2cpio
%{_bindir32}/gendiff
%endif

%dir			/etc/rpm
%attr(0755, root, bin)	%dir /var/lib/rpm
%rpmdbattr		/var/lib/rpm/*
%attr(0755, root, bin)	%dir /var/spool/repackage

%attr(0755, root, bin)	%dir %{__usrlibrpm}
#%attr(-, root, bin)		%{__usrlibrpm}/noarch*

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

###%{__rpmhome}/lib/libxar.so.*
###%{__rpmhome}/lib/libjs.so.*
###%{__rpmhome}/lib/librpmjsm.so.*
###%{__rpmhome}/lib/rpmjsm.so

%files build
%rpmattr	%{_bindir}/rpmbuild

%if %{build_64bit}
%{_bindir32}/rpmbuild
%endif

%rpmattr	%{__rpmhome}/brp-*
%rpmattr	%{__rpmhome}/check-files
%rpmattr	%{__rpmhome}/cross-build
%rpmattr	%{__rpmhome}/find-debuginfo.sh
%rpmattr	%{__rpmhome}/find-lang.sh
%rpmattr	%{__rpmhome}/find-prov.pl
%rpmattr	%{__rpmhome}/find-provides.perl
%rpmattr	%{__rpmhome}/find-req.pl
%rpmattr	%{__rpmhome}/find-requires.perl
%rpmattr	%{__rpmhome}/getpo.sh
%rpmattr	%{__rpmhome}/http.req
%rpmattr	%{__rpmhome}/javadeps.sh
%rpmattr	%{__rpmhome}/mono-find-provides
%rpmattr	%{__rpmhome}/mono-find-requires

%rpmattr	%{__rpmhome}/executabledeps.sh
%rpmattr	%{__rpmhome}/libtooldeps.sh
%rpmattr	%{__rpmhome}/osgideps.pl
%rpmattr	%{__rpmhome}/perldeps.pl
%rpmattr	%{__rpmhome}/perl.prov
%rpmattr	%{__rpmhome}/perl.req
%rpmattr	%{__rpmhome}/php.prov
%rpmattr	%{__rpmhome}/php.req
%rpmattr	%{__rpmhome}/pkgconfigdeps.sh
%rpmattr	%{__rpmhome}/pythondeps.sh

%rpmattr	%{__rpmhome}/gem_helper.rb

#%rpmattr	%{__rpmhome}/bin/debugedit
%rpmattr	%{__rpmhome}/bin/rpmcache
%rpmattr	%{__rpmhome}/bin/rpmcmp
%rpmattr	%{__rpmhome}/bin/rpmdeps
%rpmattr	%{__rpmhome}/bin/rpmdigest
%rpmattr	%{__rpmhome}/bin/abi-compliance-checker.pl
%rpmattr	%{__rpmhome}/bin/api-sanity-autotest.pl
%rpmattr	%{__rpmhome}/bin/chroot
%rpmattr	%{__rpmhome}/bin/cp
%rpmattr	%{__rpmhome}/bin/dbsql
%rpmattr	%{__rpmhome}/bin/find
%rpmattr	%{__rpmhome}/bin/install-sh
%rpmattr	%{__rpmhome}/bin/lua
%rpmattr	%{__rpmhome}/bin/luac
%rpmattr	%{__rpmhome}/bin/mkinstalldirs
%rpmattr	%{__rpmhome}/bin/rpmlua
%rpmattr	%{__rpmhome}/bin/rpmluac
%rpmattr	%{__rpmhome}/bin/sqlite3

%rpmattr	%{__rpmhome}/lib/liblua.a
%rpmattr	%{__rpmhome}/lib/liblua.la

%rpmattr %dir	%{__rpmhome}/macros.d
%rpmattr	%{__rpmhome}/macros.d/cmake
%rpmattr	%{__rpmhome}/macros.d/java
%rpmattr	%{__rpmhome}/macros.d/libtool
%rpmattr	%{__rpmhome}/macros.d/mandriva
%rpmattr	%{__rpmhome}/macros.d/mono
%rpmattr	%{__rpmhome}/macros.d/perl
%rpmattr	%{__rpmhome}/macros.d/php
%rpmattr	%{__rpmhome}/macros.d/pkgconfig
%rpmattr	%{__rpmhome}/macros.d/python
%rpmattr	%{__rpmhome}/macros.d/ruby
%rpmattr	%{__rpmhome}/macros.d/selinux
%rpmattr	%{__rpmhome}/macros.d/tcl
%rpmattr	%{__rpmhome}/macros.rpmbuild

#%rpmattr	%{__rpmhome}/symclash.*
%rpmattr	%{__rpmhome}/u_pkg.sh
%rpmattr	%{__rpmhome}/vpkg-provides.sh
%rpmattr	%{__rpmhome}/vpkg-provides2.sh

%files python
%defattr (-, root, bin)
%{_libdir32}/python%{with_python_version}/vendor-packages/rpm

%files devel
%defattr (-, root, bin)
%if %{with_apidocs}
%doc 
%endif
%{_includedir}/rpm
%{_libdir}/librpm.a
%{_libdir}/librpm.so
%{_libdir}/librpmconstant.a
%{_libdir}/librpmconstant.so
%{_libdir}/librpmdb.a
%{_libdir}/librpmdb.so
%{_libdir}/librpmio.a
%{_libdir}/librpmio.so
%{_libdir}/librpmmisc.a
%{_libdir}/librpmmisc.so
%{_libdir}/librpmbuild.a
%{_libdir}/librpmbuild.so
%{_libdir}/pkgconfig/rpm.pc

#%{_libdir}/librpm.la
#%{_libdir}/librpmconstant.la
#%{_libdir}/librpmdb.la
#%{_libdir}/librpmio.la
#%{_libdir}/librpmmisc.la
#%{_libdir}/librpmbuild.la
###%{__rpmhome}/lib/libjs.a
###%{__rpmhome}/lib/libjs.la
###%{__rpmhome}/lib/libjs.so
###%{__rpmhome}/lib/librpmjsm.a
###%{__rpmhome}/lib/librpmjsm.la
###%{__rpmhome}/lib/librpmjsm.so

%changelog
* Sat Oct 23 2010 Jeff Johnson <jbj@rpm5.org> - 5.3.5-0.1
- resurrect rpm.spec.

* Tue Jan 22 2008 Jeff Johnson <jbj@rpm5.org> - 5.1-0.1
- resurrect rpm.spec.
