#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define cc_is_gcc 1

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFESilly
Summary:             Simple and easy to use library for image loading
Version:             0.1.0
Group:               System Environment/Libraries
License:             MIT
URL:                 http://www.cegui.org.uk
Source:              %{sf_download}/crayzedsgui/SILLY-%{version}.tar.gz
Source1:             %{sf_download}/crayzedsgui/SILLY-DOCS-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
#SUNW_Copyright:      %{name}.copyright
Group:               Games
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWpng
BuildRequires: SUNWpng-devel
BuildRequires: SFEdoxygen
Requires: SUNWjpg
BuildRequires: SUNWjpg-devel
Requires: SUNWzlib

%description
The Simple Image Loading LibrarY is a companion library of the CEGUI project.
It provides a simple and easy to use library for image loading.

It currently supports the following formats:
TGA (Targa)
JPEG (Joint Photographic Experts Group)
PNG (Portable Network Graphics)

%package devel
Summary:                 Development files for SILLY
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWpng-devel
Requires: SFEdoxygen
Requires: SUNWjpg-devel

%description devel
Development files for SILLY.

%prep
%setup -q -c -n %name-%version
cd SILLY-%{version}
# Don't use full path, otherwise it shows buildroot as part of the path
%{gnu_bin}/sed -i 's|\(FULL_PATH_NAMES[ \t][ \t]*= \)YES|\1NO|' Doxyfile

# Get rid of some useless noise
%{gnu_bin}/sed -i 's|\(WARNINGS[ \t][ \t]*= \)YES|\1NO|' Doxyfile
%{gnu_bin}/sed -i 's|\(WARN_IF_UNDOCUMENTED[ \t][ \t]*= \)YES|\1NO|' Doxyfile
%{gnu_bin}/sed -i 's|\(WARN_IF_DOC_ERROR[ \t][ \t]*= \)YES|\1NO|' Doxyfile

# Generate developer man pages
%{gnu_bin}/sed -i 's|\(GENERATE_MAN[ \t][ \t]*= \)NO|\1YES|' Doxyfile

# Multiarch hack, we are now using prebuilt HTML
%{gnu_bin}/sed -i 's|\(GENERATE_HTML[ \t][ \t]*= \)YES|\1NO|' Doxyfile 
cd ..

%ifarch amd64 sparcv9
cp -pr SILLY-%{version} SILLY-%{version}-64
%endif

%build
%ifarch amd64 sparcv9
cd SILLY-%{version}-64
export CFLAGS="%{optflags64}"
export CXXFLAGS="%{cxx_optflags64}"
export LDFLAGS="%{_ldflags64} %{gnu_lib_path64}"

./configure --prefix=%{_prefix}  \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --mandir=%{_mandir} \
            --disable-static \
            --with-pic
gmake
cd ..
%endif

cd SILLY-%{version}
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags} %{gnu_lib_path}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --disable-static \
            --with-pic
gmake

#Build developer documentation
doxygen
cd ..

%install
rm -rf $RPM_BUILD_ROOT
PDIR=`pwd`
%ifarch amd64 sparcv9
cd SILLY-%{version}-64
make install     DESTDIR=$RPM_BUILD_ROOT INSTALL="ginstall -p"
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd ${PDIR}/SILLY-%{version}
make install     DESTDIR=$RPM_BUILD_ROOT INSTALL="ginstall -p"
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

#Install man pages
mkdir -p %{buildroot}%{_mandir}/man3
cp -r doc/man/man3/* %{buildroot}%{_mandir}/man3 
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
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Sat Nov 21 2009 - Moinak Ghosh
- Initial version.
