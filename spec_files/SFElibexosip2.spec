#
# spec file for package SFElibexosip2
#
# includes module(s): libexosip2
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFElibexosip2
Summary:                 The eXtended OSIP library
Version:                 3.3.0
License:                 GPL
Source:                  http://ftp.twaren.net/Unix/NonGNU/exosip/libeXosip2-%{version}.tar.gz
URL:                     http://savannah.nongnu.org/projects/exosip
Patch1:                  libexosip2-01-configure.diff
Patch2:                  libexosip2-02-sip_reg.c.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                SFEgperf
Requires:                SFElibosip2
BuildRequires:           SFElibosip2-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:                SFElibosip2-devel

%prep
%setup -q -c -n %name-%version
cd libeXosip2-%version
%patch1  -p1
%patch2  -p1
cd ..

%ifarch amd64 sparcv9
cp -rp libeXosip2-%{version} libeXosip2-%{version}-64
%endif

%build
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

%ifarch amd64 sparcv9
cd libeXosip2-%{version}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64 -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64} -L/lib/64 -R/lib/64"

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
            --disable-minisize \
            --with-pic

make
cd ..
%endif

cd libeXosip2-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib -L/lib -R/lib -lssl -lcrypto"

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
            --disable-minisize \
            --with-pic

make
cd ..


%install
rm -rf $RPM_BUILD_ROOT

export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

%ifarch amd64 sparcv9
cd libeXosip2-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
cd ..
%endif

cd libeXosip2-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
cd ..



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sip_reg
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/sip_reg
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Thu May 14 2009 - moinakg@belenix.org
- Initial version
