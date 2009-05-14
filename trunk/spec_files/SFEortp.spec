#
# spec file for package SFEortp
#
# includes module(s): ortp
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFEortp
Summary:                 A Real-time Transport Protocol (RTP,RFC3550) library
Version:                 0.16.0
License:                 LGPL
Source:                  http://ftp.twaren.net/Unix/NonGNU/linphone/ortp/sources/ortp-%{version}.tar.gz
URL:                     http://www.linphone.org/index.php/eng/code_review/ortp
Patch1:                  ortp-1-str_utils.c.1.diff
Patch2:                  ortp-2-rtpparse.c.2.diff
Patch3:                  ortp-3-rtpsession_priv.h.3.diff
Patch4:                  ortp-4-rtpsession.c.4.diff
Patch5:                  ortp-5-rtpsession_inet.c.7.diff
Patch6:                  ortp-6-event.c.11.diff
Patch8:                  ortp-8-rtcpparse.c.16.diff
Patch9:                  ortp-9-rtcp.c.19.diff
Patch10:                 ortp-10-telephonyevents.c.20.diff
Patch12:                 ortp-12-stun.c.24.diff
Patch13:                 ortp-13-Makefile.in.25.diff
Patch14:                 ortp-14-str_utils.h.26.diff
Patch15:                 ortp-15-event.h.27.diff
Patch16:                 ortp-16-port.h.28.diff
Patch17:                 ortp-17-rtpsession.h.29.diff
Patch18:                 ortp-18-rtcp.h.30.diff
Patch19:                 ortp-19-rtp.h.31.diff
Patch20:                 ortp-20-telephonyevents.h.33.diff
Patch22:                 ortp-22-configure.35.diff
Patch23:                 ortp-23-rtpsend_stupid.c.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                SFElibosip2
BuildRequires:           SFElibosip2-devel
Requires:                SFElibexosip2
BuildRequires:           SFElibexosip2-devel
Requires:                SUNWopenssl-libraries
BuildRequires:           SUNWopenssl-include

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:                SFElibosip2-devel
Requires:                SFElibexosip2-devel
Requires:                SUNWopenssl-include

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -c -n %name-%version
cd ortp-%version
%patch1  -p1
%patch2  -p1
%patch3  -p1
%patch4  -p1
%patch5  -p1
%patch6  -p1
%patch8  -p1
%patch9  -p1
%patch10  -p1
%patch12  -p1
%patch13  -p1
%patch14  -p1
%patch15  -p1
%patch16  -p1
%patch17  -p1
%patch18  -p1
%patch19  -p1
%patch20  -p1
%patch22  -p1
%patch23  -p1
cd ..

%ifarch amd64 sparcv9
cp -rp ortp-%{version} ortp-%{version}-64
%endif

%build
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

%ifarch amd64 sparcv9
cd ortp-%{version}-64
export CFLAGS="%optflags64 -D__EXTENSIONS__ -D_XPG4_2"
export CXXFLAGS="%cxx_optflags64 -D__EXTENSIONS__ -D_XPG4_2"
export LDFLAGS="%_ldflags64 -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64} -L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64} -lcrypto -lssl"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}              \
            --libdir=%{_libdir}/%{_arch64}              \
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static                 \
            --disable-libtool-lock \
            --enable-ipv6 \
            --enable-debug=no \
            --enable-memcheck=no \
            --enable-mode64bit \
            --with-pic

make
cd ..
%endif

cd ortp-%{version}
export CFLAGS="%optflags -D__EXTENSIONS__ -D_XPG4_2"
export CXXFLAGS="%cxx_optflags -D__EXTENSIONS__ -D_XPG4_2"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -lcrypto -lssl"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared                  \
            --disable-static                 \
            --disable-libtool-lock \
            --enable-ipv6 \
            --enable-debug=no \
            --enable-memcheck=no \
            --with-pic

make
cd ..


%install
rm -rf $RPM_BUILD_ROOT

export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

%ifarch amd64 sparcv9
cd ortp-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
cd ..
%endif

cd ortp-%{version}
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

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Thu May 14 2009 - moinakg@belenix.org
- Initial version
