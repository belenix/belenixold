#
# spec file for package SFEstellarium.spec
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define SFEfreetype %(/usr/bin/pkginfo -q SFEfreetype && echo 1 || echo 0)
%define guidever 0.10.2-1
%define perl_bin %{_prefix}/perl5/5.8.4/bin

Name:                    SFEstellarium
Summary:                 A Photo-realistic nightsky renderer
Version:                 0.10.2
Group:                   Education/Astronomy
License:                 GPLv2+
URL:                     http://stellarium.free.fr/
Source:                  %{sf_download}/stellarium/stellarium-%{version}.tar.gz
Source1:                 stellarium.png
Source2:                 stellarium.desktop
Source3:                 %{sf_download}/stellarium/stellarium_user_guide-%{guidever}.pdf
Patch1:                  stellarium-01-solaris.diff
Patch2:                  stellarium-02-cmake.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEsdl-devel
Requires: SFEsdl
BuildRequires:	SFEsdl-mixer-devel
Requires:	SFEsdl-mixer
Requires: SUNWxorg-mesa
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWperl584usr
%if %SFEfreetype
BuildRequires: SFEfreetype-devel
Requires: SFEfreetype
%else
BuildRequires: SUNWfreetype2
Requires: SUNWfreetype2
%endif
Requires: FSWxorg-fonts-core
BuildRequires: SFEcmake
Requires: SFEqt4
BuildRequires: SFEqt4-devel
Requires: SUNWgnu-gettext
BuildRequires: SUNWgnu-gettext-devel
Requires: SFEboost-gpp
BuildRequires: SFEboost-gpp-devel
Requires: SUNWglib2
BuildRequires: SUNWglib2-devel

%description
Stellarium is a real-time 3D photo-realistic nightsky renderer. It can
generate images of the sky as seen through the Earth's atmosphere with
more than one hundred thousand stars from the Hipparcos Catalogue,
constellations, planets, major satellites and nebulas.

%package doc
Summary:   	         The user guide about Stellarium
Group:		         Documentation
License:	         GFDL
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %{name}

%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -c -n %name-%version
cd stellarium-%{version}
%patch1 -p1
%patch2 -p1
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd stellarium-%{version}
export CXXFLAGS="%cxx_optflags"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path} -L%{_libdir}/boost/gcc4 -R%{_libdir}/boost/gcc4"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export PATH="%{perl_bin}:${PATH}"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_INSTALL_DIR=%{_libdir}/%{_arch64}                         \
        -DBIN_INSTALL_DIR=%{_bindir}/%{_arch64}                         \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBOOST_INCLUDEDIR=%{_includedir}/boost/gcc4                    \
        -DBOOST_LIBRARYDIR=%{_libdir}/boost/gcc4                        \
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

gmake -j$CPUS 

%install
cd stellarium-%{version}
export PATH="%{perl_bin}:${PATH}"
gmake install DESTDIR=$RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/applications

cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_datadir}/applications

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/doc/stellarium
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_datadir}/doc/stellarium

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%defattr (-, root, other)
%{_datadir}/applications
%{_datadir}/pixmaps
%{_datadir}/stellarium

%files doc
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/doc

%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%changelog
* Mon Nov 02 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial spec.
