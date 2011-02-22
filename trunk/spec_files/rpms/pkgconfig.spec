Name:           pkgconfig
Summary:        A tool for determining compilation options
Version:        0.25
URL:            http://pkgconfig.freedesktop.org
Source:         http://www.freedesktop.org/software/pkgconfig/releases/pkg-config-%{version}.tar.gz
Patch1:         pkg-config-0.21-compat-loop.patch
Patch2:         pkg-config-lib64-excludes.patch
Patch3:         pkg-config-dnl.patch
License:        GPLv2+
Release:        1%{?dist}
Group:          Development/Tool
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#Requires: SUNWlibm

%description
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.
 
%prep
%bsetup

%build
cd pkg-config-%{version}
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export SHELL="/usr/bin/bash"

bash ./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --mandir=%{_mandir}         \
            --datadir=%{_datadir}       \
            --sysconfdir=%{_sysconfdir} \
            --with-pc-path=%{_libdir}/pkgconfig:%{_datadir}/pkgconfig
gmake
cd ..

%install
rm -rf $RPM_BUILD_ROOT

cd pkg-config-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%{_mandir}/man1/*
%{_docdir}/*

%defattr (-, root, other)
%{_aclocaldir}/*

%changelog
