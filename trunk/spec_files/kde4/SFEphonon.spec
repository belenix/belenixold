#
# spec file for package SFEphonon
#
# includes module(s): phonon
#
# 64Bit build commented for now since GStreamer is still 32Bit only.
#
%include Solaris.inc

#%ifarch amd64 sparcv9
#%include arch64.inc
#%endif

#%include base.inc

%define src_dir          phonon
Name:                    SFEphonon
Summary:                 KDE4 Pluggable Multimedia framework api
Version:                 4.3.1
License:                 LGPLv2+
Source:                  %{kde_mirror}/4.2.1/src/phonon-%{version}.tar.bz2
Source1:                 http://gstreamer.freedesktop.org/data/images/artwork/gstreamer-logo.svg
URL:                     http://phonon.kde.org/

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFElibxcb
Requires:      SUNWgnome-media
BuildREquires: SUNWgnome-media-devel
BuildRequires: SFEautomoc
BuildRequires: SFElibxcb-devel
BuildRequires: SFEqt4-devel
BuildRequires: SFEcmake
BuildRequires: SFEdoxygen

%description
Phonon is a Multimedia Framework for KDE4 and Applications. It is pluggable and
supports multiple backends.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version

#%ifarch amd64 sparcv9
#cp -rp %{src_dir}-%{version} %{src_dir}-%{version}-64
#%endif

%build
#
# Need to force some shell info to point to bash because the scripts
# are for bash.
#
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
export GCC="yes"
export CC=%{_prefix}/gnu/bin/gcc
export CXX=%{_prefix}/gnu/bin/g++
export QTDIR=%{_prefix}
export QT_INCLUDES=%{_includedir}/qt4

#%ifarch amd64 sparcv9
#cd %{src_dir}-%{version}-64
#export CFLAGS="%optflags64 -I${QT_INCLUDES}"
#export CXXFLAGS="%cxx_optflags64 -I${QT_INCLUDES}"
#export LDFLAGS="%_ldflags64 -L%{_prefix}/lib/%{_arch64} -R%{_prefix}/lib/%{_arch64} %{gnu_lib_path64} -lstdc++"
#
#cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
#        -DCMAKE_BUILD_TYPE=Release                                      \
#        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
#        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
#        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
#        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
#        -DLIB_INSTALL_DIR=%{_libdir}/%{_arch64}                         \
#        -DBIN_INSTALL_DIR=%{_bindir}/%{_arch64}                         \
#        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
#        -DBUILD_SHARED_LIBS=On                                          \
#        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1
#
#make VERBOSE=1
#cd ..
#%endif

cd %{src_dir}-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -L%{_prefix}/lib -R%{_prefix}/lib %{gnu_lib_path} -lstdc++"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_INSTALL_DIR=%{_libdir}                                    \
        -DBIN_INSTALL_DIR=%{_bindir}                                    \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..


%install
rm -rf $RPM_BUILD_ROOT

#%ifarch amd64 sparcv9
#cd %{src_dir}-%{version}-64
#make install DESTDIR=$RPM_BUILD_ROOT
#rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
#cd ..
#%endif

cd %{src_dir}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/kde4
%dir %attr (0755, root, bin) %{_datadir}/kde4/services
%dir %attr (0755, root, bin) %{_datadir}/kde4/services/phononbackends
%{_datadir}/kde4/services/phononbackends/*

%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/interfaces
%{_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, other) %{_libdir}/kde4
%{_libdir}/kde4/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*

#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%{_libdir}/%{_arch64}/*.so*
#%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/phonon.pc

%changelog
* Sun Apr 17 2009 - moinakg@belenix.org
- Initial version.
