#
# spec file for package SFElibosip2
#
# includes module(s): libosip2
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFElibosip2
Summary:                 oSIP is a GNU implementation of SIP
Version:                 3.3.0
License:                 LGPL
Source:                  http://ftp.gnu.org/gnu/osip/libosip2-%{version}.tar.gz
URL:                     http://www.gnu.org/software/osip/
Patch1:                  libosip2-01-configure.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                SFEgperf

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
cd libosip2-%version
%patch1  -p1
cd ..

%ifarch amd64 sparcv9
cp -rp libosip2-%{version} libosip2-%{version}-64
%endif

%build
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

%ifarch amd64 sparcv9
cd libosip2-%{version}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}              \
            --libdir=%{_libdir}/%{_arch64}              \
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static                 \
            --disable-libtool-lock \
            --disable-gprof \
            --enable-mt \
            --enable-pthread \
            --enable-semaphore \
            --enable-sysv \
            --enable-gperf \
            --enable-test \
            --with-pic

make
cd ..
%endif

cd libosip2-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared                  \
            --disable-static                 \
            --disable-libtool-lock \
            --disable-gprof \
            --enable-mt \
            --enable-pthread \
            --enable-semaphore \
            --enable-sysv \
            --enable-gperf \
            --enable-test \
            --with-pic

make
cd ..


%install
rm -rf $RPM_BUILD_ROOT

export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

%ifarch amd64 sparcv9
cd libosip2-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
cd ..
%endif

cd libosip2-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
cd ..



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*


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
* Thu May 14 2009 - moinakg@belenix.org
- Initial version
