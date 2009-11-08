#
# spec file for package SFErdesktop
#
# includes module(s): rdesktop
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFErdesktop
Summary:                 An open source client for Windows Terminal Services
Version:                 1.6.0
URL:                     http://www.rdesktop.org/
Source:                  %{sf_download}/rdesktop/rdesktop-%{version}.tar.gz
License:                 GPLv2

SUNW_BaseDir:            %{_basedir}
#SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibsamplerate
BuildRequires: SFElibsamplerate-devel
Requires: SUNWopenssl-libraries
BuildRequires: SUNWopenssl-include

%description
Rdesktop is an open source client for Windows Terminal Services,
capable of natively speaking Remote Desktop Protocol (RDP) in
order to present the user's Windows desktop. Supported servers
include Windows 2000 Server, Windows Server 2003, Windows Server
2008, Windows XP, Windows Vista and Windows NT Server 4.0.

Rdesktop currently runs on most UNIX based platforms with the X
Window System, and other ports should be fairly straightforward.

%prep
%if %cc_is_gcc
%else
error "This spec file requires /usr/gnu/bin/g++. Please set your environment variables."
%endif

%setup -q -c -n %name-%version
cd rdesktop-%{version}
cd ..

%build
#
# Need to force some shell info to point to bash because the scripts
# are for bash.
#
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
export GCC="yes"

cd rdesktop-%{version}
export LDFLAGS="%_ldflags -L/lib -R/lib"
export CFLAGS="%optflags -fno-strict-aliasing"
export CXXFLAGS="%cxx_optflags -fno-strict-aliasing"

./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --datadir=%{_datadir}       \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes         \
            --disable-static

gmake
cd ..

%install
rm -rf $RPM_BUILD_ROOT

export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

cd rdesktop-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/rdesktop
%{_datadir}/rdesktop/*

%changelog
* Sun Nov 08 2009 - Moinak Ghosh
- Initial version
