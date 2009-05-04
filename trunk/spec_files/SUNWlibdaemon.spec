
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Note: This spec file will only work if CC is gcc. Do it at the command line
# before invoking this spec file (as opposed to putting it in %build below).
# That way the macros in Solaris.inc will know you've set it.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SUNWlibdaemon
Summary:             Lightweight C library for UNIX daemons
Version:             0.13
Source:              http://0pointer.de/lennart/projects/libdaemon/libdaemon-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version

%ifarch amd64 sparcv9
cp -rp libdaemon-%{version} libdaemon-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export BASE_CFLAGS="-I/usr/gnu/include -D_NSIG=NSIG"
export BASE_CFLAGS="$BASE_CFLAGS -D__EXTENSIONS__"

export BASE_LDFLAGS="%{_ldflags} -lsocket -lnsl -L/usr/gnu/lib -R/usr/gnu/lib"

%ifarch amd64 sparcv9
cd libdaemon-%{version}-64

export CFLAGS="${BASE_CFLAGS} -m64"
export LDFLAGS="${BASE_LDFLAGS} -m64"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --libdir=%{_libdir}/%{_arch64} \
            --localstatedir=%{_localstatedir} \
            --sysconfdir=%{_sysconfdir} \
            --disable-warnings \
            --disable-debug \
            --disable-dependency-tracking \
            --enable-shared \
            --disable-static \
            --disable-libtool-lock \
            --disable-lynx --with-pic

make -j$CPUS
cd ..
%endif

cd libdaemon-%{version}
export CFLAGS="${BASE_CFLAGS}"
export LDFLAGS="${BASE_LDFLAGS}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
	    --localstatedir=%{_localstatedir} \
	    --sysconfdir=%{_sysconfdir} \
            --disable-warnings \
            --disable-debug \
            --disable-dependency-tracking \
            --enable-shared \
            --disable-static \
            --disable-libtool-lock \
            --disable-lynx --with-pic

make -j$CPUS 
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd libdaemon-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
cd ..
%endif

cd libdaemon-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
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

%changelog
* Mon May 04 2009 - moinakg@belenix.org
- Initial version imported from JDS repo and version bumped.
