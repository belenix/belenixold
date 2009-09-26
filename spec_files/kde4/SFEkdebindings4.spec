#
# spec file for package SFEkdebindings4
#
# includes module(s): kdebindings4
#
%include Solaris.inc

%define php_version 5.2.4
%define ruby_version 1.8

Name:			SFEkdebindings4
Summary:		Various language bindings for KDE4 (except Python)
License:		GPLv2
Version:		4.3.1
URL:                    http://developer.kde.org/language-bindings/
Source:			http://gd.tuwien.ac.at/pub/kde/stable/%{version}/src/kdebindings-%{version}.tar.bz2
Patch2:                 kdebindings4-02-qyoto-examples.diff

# Disable building PyKDE as it is packaged separately in SFEpython26-pykde4
Patch3:                 kdebindings4-03-disable-python.diff

# Uncomment some includes as otherwise krossjava does not build.
# Dunno why they are commented.
Patch4:                 kdebindings4-04-jvmvariant.h.diff

BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
SUNW_Copyright:         %{name}.copyright
%include default-depend.inc
Requires: SFEkdelibs4
Requires: SFEkdepimlibs4
Requires: SFEakonadi
Requires: SFEkdegraphics4
Requires: SFEsoprano
BuildRequires: SFEkdelibs4-devel
BuildRequires: SFEkdepimlibs4-devel
BuildRequires: SFEakonadi-devel
BuildRequires: SFEkdegraphics4-devel
BuildRequires: SFEsoprano-devel
BuildRequires: SFEdoxygen
BuildRequires: SFEgraphviz
BuildRequires: SUNWruby18u
BuildRequires: SUNWphp524usr
BuildRequires: SUNWj6dev

%description
Various non C++ language bindings for KDE4. For bindings to Python 2.6 install
the SFEpython26-pykde4 package.

%package devel
Summary:                %{summary} - Development files.
SUNW_BaseDir:           %{_prefix}
%include default-depend.inc
Requires: %{name}
Requires: SFEkdelibs4-devel
Requires: SFEkdepimlibs4-devel
Requires: SFEakonadi-devel
Requires: SFEkdegraphics4-devel
Requires: SFEsoprano-devel
Requires: SFEdoxygen
Requires: SFEgraphviz

%package ruby
Summary:                Ruby bindings for Qt4 and KDE4
SUNW_BaseDir:           %{_prefix}
%include default-depend.inc
Requires: %{name}
Requires: SUNWruby18u

%package ruby-devel
Summary:                Ruby bindings for Qt4 and KDE4 - Development files
SUNW_BaseDir:           %{_prefix}
%include default-depend.inc
Requires: %{name}-devel
Requires: %{name}-ruby

%package php
Summary:                PHP bindings for Qt4 and KDE4
SUNW_BaseDir:           %{_prefix}
%include default-depend.inc
Requires: %{name}
Requires: SUNWphp524usr

%package java
Summary:                Java bindings for the Kross scripting framework in KDE4
SUNW_BaseDir:           %{_prefix}
%include default-depend.inc
Requires: %{name}
Requires: SUNWj6rt
BuildRequires: SUNWj6dev

%prep
%setup -q -c -n %name-%version
cd kdebindings-%{version}
%patch2 -p0
%patch3 -p1
%patch4 -p1

#
# Disable Soprano bindings for now, it does not build
#
cp CMakeLists.txt CMakeLists.txt.orig
cat CMakeLists.txt.orig | sed '{
    s/macro_optional_find_package(Soprano)/#macro_optional_find_package(Soprano)/
'} > CMakeLists.txt

cd ..
mkdir kdebld

%build
export QTDIR=%{_prefix}
export QT_INCLUDES=%{_includedir}/qt4
OPATH=${PATH}
PHP5_DIR=%{_prefix}/php5/%{php_version}
rm -rf $RPM_BUILD_ROOT

cd kdebld
export CFLAGS="%optflags -I%{_includedir}/boost/gcc4"
export CXXFLAGS="%cxx_optflags -I${PHP5_DIR}/include -I%{_includedir}/boost/gcc4"
export LDFLAGS="%_ldflags %{gnu_lib_path} -L%{_libdir}/boost/gcc4 -R%{_libdir}/boost/gcc4"
export QMAKESPEC=%{_datadir}/qt4/mkspecs/solaris-g++
export PATH="%{qt4_bin_path}:${PHP5_DIR}/bin:${OPATH}"
export JAVA_HOME=%{_prefix}/java

cmake   ../kdebindings-%{version} -DCMAKE_INSTALL_PREFIX=%{_prefix}     \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DCMAKE_INCLUDE_PATH="%{gnu_inc}"                               \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DSYSCONF_INSTALL_DIR=%{_sysconfdir}                            \
        -DJAVA_INCLUDE_PATH2=${JAVA_HOME}/include/solaris               \
        -DPHP5_CONFIG_EXECUTABLE=${PHP5_DIR}/bin/php-config             \
        -DPHP5_EXECUTABLE=${PHP5_DIR}/bin/php                           \
        -DBOOST_INCLUDEDIR=%{_includedir}/boost/gcc4                    \
        -DBOOST_LIBRARYDIR=%{_libdir}/boost/gcc4                        \
        -DBUILD_SHARED_LIBS=On                                          \
        -DKDE4_ENABLE_HTMLHANDBOOK=Off                                  \
        -DENABLE_KORUNDUM=on -DENABLE_SMOKE=on                          \
        -DENABLE_RUBY=on -DENABLE_PYKDE4=off                            \
        -DENABLE_KROSSPYTHON=on                                         \
        -DENABLE_KROSSRUBY=on                                           \
        -DENABLE_KROSSJAVA=on                                           \
        -DENABLE_PHP=on                                                 \
        -DENABLE_PHP-QT=on                                              \
        -DENABLE_JAVA=on                                                \
        -DWITH_Soprano:BOOL=OFF                                         \
        -DCMAKE_VERBOSE_MAKEFILE=1 > config.log 2>&1

make install DESTDIR=$RPM_BUILD_ROOT
cd ..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT

OPATH=${PATH}

cd kdebld
export PATH="%{qt4_bin_path}:${OPATH}"
make install DESTDIR=$RPM_BUILD_ROOT
cd ..
export PATH="${OPATH}"


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libsmoke*

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/smoke.h
%dir %attr (0755, root, bin) %{_includedir}/smoke
%{_includedir}/smoke/*

%files ruby
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libqtruby*
%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/krubypluginfactory.so
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/rbkconfig_compiler4
%{_bindir}/rbqtapi
%{_bindir}/krubyapplication
%{_bindir}/rbrcc
%dir %attr (0755, root, bin) %{_prefix}/ruby
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_version}
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_version}/lib
%{_prefix}/ruby/%{ruby_version}/lib/*

%defattr(-,root,other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%files ruby-devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/qtruby
%{_includedir}/qtruby/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/rbuic4

%files php
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_prefix}/php5
%dir %attr (0755, root, bin) %{_prefix}/php5/%{php_version}
%dir %attr (0755, root, bin) %{_prefix}/php5/%{php_version}/modules
%{_prefix}/php5/%{php_version}/modules/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/phpuic

%files java
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/libkrossjava.so
%dir %attr (0755, root, bin) %{_libdir}/kde4/kross
%{_libdir}/kde4/kross/kross.jar

%changelog
* Sat Sep 26 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Changes to uprev to KDE4.3.1.
* Tue Jun 23 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
