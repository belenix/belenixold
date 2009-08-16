#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                SFEpth
Summary:             The GNU Portable Threads 
Version:             2.0.7
License:             LGPLv2.1
Source:              ftp://ftp.gnu.org/gnu/pth/pth-%{version}.tar.gz
URL:                 http://www.gnu.org/software/pth/
Patch1:              pth-01-pth.h.in.diff
Patch2:              pth-02-Makefile.in.0.diff

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
cd pth-%version
%patch1 -p1
%patch2 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp pth-%version pth-%{version}-64
%endif


%build
export OCC="${CC}"

%ifarch amd64 sparcv9
cd pth-%{version}-64

export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 -lsocket -lnsl"
export CC="${CC} -m64"

./configure --prefix=%{_prefix}  \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info \
            --enable-shared \
            --disable-static

make
cd ..
%endif

cd pth-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lsocket -lnsl"
export CC="${OCC}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info \
            --enable-shared \
            --disable-static

make 
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd pth-%{version}-64

make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/libpth.*a
cd ..
%endif

cd pth-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}/libpth.*a
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gawk gawkinet' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gawk gawkinet' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/pth-config
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/pth-config
%endif

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Sat Aug 15 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Fix permissions.
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Added 64Bit build.
* Sat Dec 29 2007 - jijun.yu@sun.com
- Initial spec
