#
# spec file for package SFEstrigi
#
# includes module(s): strigi
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_dir          strigi
Name:                    SFEstrigi
Summary:                 A fast and light desktop search engine
Version:                 0.6.4
License:                 GPLv2
URL:                     http://strigi.sourceforge.net/
Source:                  %{sf_download}/strigi/strigi-%{version}.tar.bz2
Source1:	         strigiclient.desktop
Source2:	         strigi-daemon.desktop
Patch1:		         strigi-01-0.6.2-multilib.patch
Patch2:		         strigi-02-gcc44.patch
Patch3:                  strigi-03-0.6.4-root-crash.patch


SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFEexiv2
Requires:      SFEclucene-core
Requires:      SFElog4cxx
Requires:      SFEcppunit
Requires:      SUNWbzip
Requires:      SUNWlxml
Requires:      SUNWdbus-libs
Requires:      SUNWgamin
BuildRequires: SFEexiv2-devel
BuildRequires: SFEclucene-core-devel
BuildRequires: SFEautomoc
BuildRequires: SFEqt4-devel
BuildRequires: SFEcmake
BuildRequires: SFEdoxygen
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SFElog4cxx-devel
BuildRequires: SFEcppunit-devel
BuildRequires: SUNWgamin-devel
BuildRequires: SUNWgnome-desktop-prefs


%description
Strigi is a fast and light desktop search engine. It can handle a large
range of file formats such as emails, office documents, media files, and
file archives. It can index files that are embedded in other files. This
means email attachments and files in zip files are searchable as if they
were normal files on your harddisk.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWlibexif-devel
Requires: SFEclucene-core-devel
Requires: SFEautomoc
Requires: SFEqt4-devel
Requires: SFEcmake
Requires: SFEdoxygen
Requires: SUNWlxml-devel
Requires: SUNWdbus-devel
Requires: SFElog4cxx-devel
Requires: SUNWgamin-devel


%prep
%setup -q -c -n %name-%version
cd %{src_dir}-%{version}
%patch1 -p1
%patch2 -p0
%patch3 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp %{src_dir}-%{version} %{src_dir}-%{version}-64
%endif

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
export CMAKE_INCLUDE_PATH="%{gnu_inc}:%{xorg_inc}"
OPATH=${PATH}

%ifarch amd64 sparcv9
cd %{src_dir}-%{version}-64
export CFLAGS="%optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -lstdc++ %{xorg_lib_path64}"
export PATH="%{qt4_bin_path64}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/%{_arch64}/pkgconfig:%{_prefix}/gnu/lib/%{_arch64}/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib64}:%{gnu_lib64}:%{_prefix}/lib/%{_arch64}:/lib/%{_arch64}"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_DESTINATION=%{_libdir}/%{_arch64}                         \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBUILD_SHARED_LIBS=On                                          \
        -DPKGCONFIG_INSTALL_PREFIX=%{_libdir}/%{_arch64}/pkgconfig      \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..
%endif

cd %{src_dir}-%{version}
export CFLAGS="%optflags -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++ %{xorg_lib_path} -L/lib -R/lib"
export PATH="%{qt4_bin_path}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DCMAKE_INCLUDE_PATH="%{gnu_inc}"				\
        -DLIB_DESTINATION=%{_libdir}                                    \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT

OPATH=${PATH}

%ifarch amd64 sparcv9
cd %{src_dir}-%{version}-64
export PATH="%{qt4_bin_path64}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
for prg in luceneindexer strigidaemon deepfind deepgrep xmlindexer strigiclient strigicmd
do
	mv ${RPM_BUILD_ROOT}%{_bindir}/${prg} ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
done
cd ..
%endif

cd %{src_dir}-%{version}
export PATH="%{qt4_bin_path}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
cd ..
export PATH="${OPATH}"

desktop-file-install --vendor="belenix" \
                     --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
                     %{SOURCE1}

# Add an autostart desktop file for the strigi daemon
install -p -m644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/xdg/autostart/strigi-daemon.desktop


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/luceneindexer
%{_bindir}/strigidaemon
%{_bindir}/deepfind
%{_bindir}/deepgrep
%{_bindir}/xmlindexer
%{_bindir}/strigiclient
%{_bindir}/strigicmd

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/strigi
%{_libdir}/strigi/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/strigi
%{_datadir}/strigi/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/luceneindexer
%{_bindir}/%{_arch64}/strigidaemon
%{_bindir}/%{_arch64}/deepfind
%{_bindir}/%{_arch64}/deepgrep
%{_bindir}/%{_arch64}/xmlindexer
%{_bindir}/%{_arch64}/strigiclient
%{_bindir}/%{_arch64}/strigicmd

%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/strigi
%{_libdir}/%{_arch64}/strigi/*
%endif

%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg/autostart
%{_sysconfdir}/xdg/autostart/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif

%changelog
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
