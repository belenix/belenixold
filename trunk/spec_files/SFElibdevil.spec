#
# spec file for package SFElibdevil.spec
#
# includes module(s): libdevil
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_name	DevIL
Name:                   SFElibdevil
Summary:                Cross-platform image library
Version:                1.7.8
Group:                  System Environment/Libraries
License:                LGPLv2
URL:                    http://openil.sourceforge.net/
Source:                 %{sf_download}/openil/%{src_name}-%{version}.tar.gz
Patch1:			libdevil-01-allegropicfix.diff

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibmng-devel
Requires: SFElibmng
BuildRequires: SFElcms-devel
Requires: SFElcms
BuildRequires: SFEjasper-devel
Requires: SFEjasper
BuildRequires: SUNWTiff-devel
Requires: SUNWTiff
BuildRequires: SUNWpng-devel
Requires: SUNWpng
BuildRequires: SUNWjpg-devel
Requires: SUNWjpg
BuildRequires: SFEallegro-devel
Requires: SFEallegro
BuildRequires: SFEsdl-devel
Requires: SFEsdl
BuildRequires: SUNWxorg-headers
Requires: SUNWxorg-mesa

%description
Developer's Image Library (DevIL) is a programmer's library to develop
applications with very powerful image loading capabilities, yet is easy for a
developer to learn and use. Ultimate control of images is left to the
developer, so unnecessary conversions, etc. are not performed. DevIL utilizes
a simple, yet powerful, syntax. DevIL can load, save, convert, manipulate,
filter and display a wide variety of image formats.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SFElibmng-devel
Requires: SFElcms-devel
Requires: SFEjasper-devel
Requires: SUNWTiff-devel
Requires: SUNWpng-devel
Requires: SUNWjpg-devel
Requires: SFEallegro-devel
Requires: SFEsdl-devel
Requires: SUNWxorg-headers

%description devel
Development files for DevIL 

%package ILUT
Summary:                 The libILUT component of DevIL
Group:                   System Environment/Libraries
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%description ILUT
The libILUT component of DevIL

%package ILUT-devel
Summary:                 Development files for the libILUT component of DevIL
Group:                   Development/Libraries
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %{name}-ILUT
Requires: %{name}-devel
Requires: SUNWgnome-common-devel

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -pr devil-%{version} devil-%{version}-64
cd devil-%{version}
%patch1 -p1
cd ..
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd devil-%{version}-64

export CFLAGS="-O2 -m64 -Dlinux=1"
export CXXFLAGS="-O2 -m64 -Dlinux=1"
export LDFLAGS="%_ldflags64"
export LD_OPTIONS="-z muldefs"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}/%{_arch64}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}/%{_arch64}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --enable-ILU                \
            --enable-ILUT               \
            --enable-x86_64=yes         \
            --enable-shared		\
	    --disable-static
gmake -j$CPUS 
cd ..
%endif

cd devil-%{version}
export CFLAGS="-O2 -Dlinux=1"
export CXXFLAGS="-O2 -Dlinux=1"
export LDFLAGS="%_ldflags"
export LD_OPTIONS="-z muldefs"
./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-ILU                \
            --enable-ILUT               \
            --enable-shared             \
            --disable-static
gmake -j$CPUS
cd ..

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd devil-%{version}-64
export LD_OPTIONS="-z muldefs"
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.*a
cd ..
%endif

cd devil-%{version}
export LD_OPTIONS="-z muldefs"
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/ilur 
%{_libdir}/libIL.so*
%{_libdir}/libILU.so*

%ifarch amd64 sparcv9
%dir %attr(0755, root, bin) %{_bindir}/%{_arch64}
%dir %attr(0755, root, bin) %{_libdir}/%{_arch64}
%{_bindir}/%{_arch64}/ilur 
%{_libdir}/%{_arch64}/libIL.so*
%{_libdir}/%{_arch64}/libILU.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_libdir}
%dir %attr(0755, root, bin) %{_includedir}/IL
%{_includedir}/IL/devil_cpp_wrapper.hpp
%{_includedir}/IL/il.h
%{_includedir}/IL/ilu.h
%{_includedir}/IL/ilu_region.h
%dir %attr(0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/IL.pc
%{_libdir}/pkgconfig/ILU.pc
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/*

%ifarch amd64 sparcv9
%dir %attr(0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr(0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/IL.pc
%{_libdir}/%{_arch64}/pkgconfig/ILU.pc
%endif

%files ILUT
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_libdir}
%{_libdir}/libILUT.so*

%ifarch amd64 sparcv9
%dir %attr(0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libILUT.so*
%endif

%files ILUT-devel
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_libdir}
%dir %attr(0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/ILUT.pc
%{_includedir}/IL/ilut.h

%ifarch amd64 sparcv9
%dir %attr(0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/ILUT.pc
%endif

%changelog
* Sat Fri Nov 21 2009 - Moinak Ghosh
- Initial version
