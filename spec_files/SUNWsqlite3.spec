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

%include base.inc

%define compat_link1     libsqlite3-3.5.4.so.0

Name:                    SUNWsqlite3
Summary:                 SQLite3, an embeddable, zero-conf, self-contained, serverless transactional SQL engine
Version:                 3.6.7
%define doc_version      3_6_7
URL:                     http://www.sqlite.org/
Source:                  http://www.sqlite.org/sqlite-%{version}.tar.gz
Source1:                 http://www.sqlite.org/sqlite_docs_%{doc_version}.zip
Source2:                 pkgIndex.tcl
Source3:                 mapfile-libsqlite3
Source4:                 mapfile_noexstk
Source5:                 sqlite3.1

Patch1:                  sqlite3-01.diff
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 SQLite3 development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name

%package tcl
Summary:                 SQLite3 Tcl bindings
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name

%package doc
Summary:                 SQLite3 documentation
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name

%prep
if [ "x`basename $CC`" = xgcc ]
then
	%error This spec file requires SUN Studio, set the CC and CXX env variables
fi
%setup -q -c -n %name-%version
unzip %{SOURCE1}
cd sqlite-%{version}
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -pr sqlite-%{version} sqlite-%{version}-64
%endif


%build

%ifarch amd64 sparcv9
cd sqlite-%{version}-64
export PATH=/usr/ccs/bin:/usr/bin:/usr/sbin:/bin:/usr/sfw/bin:/opt/SUNWspro/bin
export CFLAGS="%optflags64 -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -DUSE_PREAD -DHAVE_USLEEP -DHAVE_FDATASYNC -DHAVE_STATVFS"
export INSTALL=/usr/ucb/install
export MAKE=/usr/bin/gmake
export LDFLAGS="-L$RPM_BUILD_ROOT%{_libdir}/%{_arch64}"
export CMD_MAPFILE=%{SOURCE4}
export LIBSQLITE_MAPFILE=%{SOURCE3}

./configure --prefix=%{_basedir} --libdir=%{_libdir}/%{_arch64} \
            --enable-threadsafe --enable-cross-thread-connections \
            --enable-threads-override-locks --enable-shared \
            --disable-static --with-tcl="%{_libdir}"

/usr/bin/gmake solaris/libsqlite3.so solaris/libtclsqlite3.so solaris/sqlite3
cd ..
%endif

cd sqlite-%{version}
export PATH=/usr/ccs/bin:/usr/bin:/usr/sbin:/bin:/usr/sfw/bin:/opt/SUNWspro/bin
export CFLAGS="%optflags -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -DUSE_PREAD -DHAVE_USLEEP -DHAVE_FDATASYNC -DHAVE_STATVFS"
export INSTALL=/usr/ucb/install
export MAKE=/usr/bin/gmake
export LDFLAGS="-L$RPM_BUILD_ROOT%{_libdir}"
export CMD_MAPFILE=%{SOURCE4}
export LIBSQLITE_MAPFILE=%{SOURCE3}

./configure --prefix=%{_basedir} \
            --enable-threadsafe --enable-cross-thread-connections \
            --enable-threads-override-locks --enable-shared \
            --disable-static --with-tcl="%{_libdir}"

/usr/bin/gmake solaris/libsqlite3.so solaris/libtclsqlite3.so solaris/sqlite3
cd ..


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_docdir}
cp -pr sqlite-%{doc_version}-docs ${RPM_BUILD_ROOT}%{_docdir}/sqlite3

ROOT=${RPM_BUILD_ROOT}
TCLDIR=%{_libdir}/tcl8.4/sqlite3
ROOTSQLITE3TCLDIR=${ROOT}${TCLDIR}
ROOTSQLITE3TCLDIR64=${ROOTSQLITE3TCLDIR}/%{_arch64}
ROOTINCLUDEDIR=${ROOT}%{_includedir}
ROOTLIB=${RPM_BUILD_ROOT}%{_libdir}
ROOTLIB64=${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}
ROOTPKGCONFIGDIR=${ROOTLIB}/pkgconfig
ROOTPKGCONFIGDIR64=${ROOTLIB64}/pkgconfig
ROOTBIN=${RPM_BUILD_ROOT}%{_bindir}
ROOTBIN64=${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
ROOTMANDIR=${RPM_BUILD_ROOT}%{_mandir}/man1

%ifarch amd64 sparcv9
cd sqlite-%{version}-64
mkdir -p ${ROOTSQLITE3TCLDIR64}
mkdir -p ${ROOTLIB64}
mkdir -p ${ROOTPKGCONFIGDIR64}
mkdir -p ${ROOTBIN64}

/usr/ucb/install -m 0755 solaris/libsqlite3.so.0 ${ROOTLIB64}/libsqlite3.so.0
(cd ${ROOTLIB64}
  ln -s libsqlite3.so.0 libsqlite3.so
  ln -s libsqlite3.so.0 libsqlite3-%{version}.so.0
  ln -s %{compat_link1} libsqlite3-%{version}.so.0
)
(cd ${ROOTSQLITE3TCLDIR}
  ln -s %{_arch64} 64)
/usr/ucb/install -m 0755 solaris/libtclsqlite3.so ${ROOTSQLITE3TCLDIR64}/libtclsqlite3.so
/usr/ucb/install -m 0755 solaris/sqlite3 ${ROOTBIN64}/sqlite3
/usr/ucb/install -m 0644 sqlite3.pc ${ROOTPKGCONFIGDIR64}/sqlite3.pc
cd ..
%endif

cd sqlite-%{version}
mkdir -p ${ROOTINCLUDEDIR}
mkdir -p ${ROOTPKGCONFIGDIR}
mkdir -p ${ROOTMANDIR}
/usr/ucb/install -m 0755 solaris/libsqlite3.so.0 ${ROOTLIB}/libsqlite3.so.0
(cd ${ROOTLIB}
  ln -s libsqlite3.so.0 libsqlite3.so
  ln -s libsqlite3.so.0 libsqlite3-%{version}.so.0
  ln -s %{compat_link1} libsqlite3-%{version}.so.0
)
/usr/ucb/install -m 0755 solaris/libtclsqlite3.so ${ROOTSQLITE3TCLDIR}/libtclsqlite3.so
/usr/ucb/install -m 0755 solaris/sqlite3 ${ROOTBIN}/sqlite3
/usr/ucb/install -m 0644 sqlite3.pc ${ROOTPKGCONFIGDIR}/sqlite3.pc
/usr/ucb/install -m 0644 %{SOURCE2} ${ROOTSQLITE3TCLDIR}
/usr/ucb/install -m 0644 sqlite3.h ${ROOTINCLUDEDIR}/sqlite3.h
/usr/ucb/install -m 0644 src/sqlite3ext.h ${ROOTINCLUDEDIR}/sqlite3ext.h
/usr/ucb/install -m 0644 %{SOURCE5} ${ROOTMANDIR}/`basename %{SOURCE5}`
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sqlite3
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/sqlite3
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%files tcl
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/tcl8.4
%dir %attr (0755, root, bin) %{_libdir}/tcl8.4/sqlite3
%{_libdir}/tcl8.4/sqlite3/lib*.so*
%{_libdir}/tcl8.4/sqlite3/*.tcl

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/tcl8.4/sqlite3/%{_arch64}
%{_libdir}/tcl8.4/sqlite3/%{_arch64}/lib*.so*
%{_libdir}/tcl8.4/sqlite3/64
%endif

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Tue Jun 30 2009 - moinakg@gmail.com
- Bump version and add compat links.
* Tue Feb 10 2009 - moinakg@gmail.com
- Initial spec (migrated and modified from SFW gate).

