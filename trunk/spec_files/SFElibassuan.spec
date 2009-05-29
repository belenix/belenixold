#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


%define src_name     libassuan
Name:                SFElibassuan
Summary:             An IPC libbray used by GnuPG 2, GPGME etc. 
Version:             1.0.5
License:             LGPL
Source:              ftp://ftp.gnupg.org/gcrypt/libassuan/libassuan-%{version}.tar.bz2
URL:                 http://www.gnupg.org/

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWlibgpg-error
BuildRequires: SFEpth-devel
Requires: SFEpth
Requires: SUNWlibgpg-error
Requires: SUNWtexi

%prep
%setup -q -c -n %name-%version

%ifarch amd64 sparcv9
cp -rp %{src_name}-%version %{src_name}-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi
OPATH="${PATH}"

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 -lsocket -lnsl"
export PATH="%{_prefix}/bin/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${PATH}"

./configure --prefix=%{_prefix}  \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --with-pth=yes    \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info

make -j$CPUS
cd ..
%endif

cd %{src_name}-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lsocket -lnsl"
export PATH="${OPATH}"

./configure --prefix=%{_prefix}  \
	    --with-pth=yes    \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/usr/share/info/dir

cp ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}/libassuan-config ./libassuan-config.orig 
cat ./libassuan-config.orig | sed '{
    s/all_thread_modules=""/all_thread_modules="pth"/
    s/extralibs=""/extralibs="-lsocket -lnsl"/
}' > ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}/libassuan-config

if [ -f ${RPM_BUILD_ROOT}%{_libdir}/libassuan-pth.a ]
then
	mv ${RPM_BUILD_ROOT}%{_libdir}/libassuan-pth.a \
	    ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/libassuan-pth.a
fi
cd ..
%endif

cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/usr/share/info/dir

cp ${RPM_BUILD_ROOT}%{_bindir}/libassuan-config ./libassuan-config.orig
cat ./libassuan-config.orig | sed '{
    s/all_thread_modules=""/all_thread_modules="pth"/
    s/extralibs=""/extralibs="-lsocket -lnsl"/
}' > ${RPM_BUILD_ROOT}%{_bindir}/libassuan-config
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'assuan' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'assuan' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/libassuan-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.a

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/libassuan-config
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.a
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*

%changelog
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Added 64Bit build.
- Fix libassuan-config.
- Bump version to 1.0.5.
* Sat Dec 29 2007 - jijun.yu@sun.com
- Initial spec
