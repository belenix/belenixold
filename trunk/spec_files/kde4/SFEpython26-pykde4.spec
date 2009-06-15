#
# spec file for package SFEpython26-pykde4
#
# includes module(s): pykde4
#
%include Solaris.inc

%define python_version 2.6

Name:			SFEpython26-pykde4
Summary:		Python bindings for KDE4
License:		GPLv3 or GPLv2 with exceptions
Version:		4.2.4
Source:			http://gd.tuwien.ac.at/pub/kde/stable/%{version}/src/kdebindings-%{version}.tar.bz2
URL:			http://www.riverbankcomputing.co.uk/software/pykde/
Patch1:                 python26-pykde4-01-disable-features.diff
Patch2:                 python26-pykde4-02-typedefs.sip.diff
Patch3:                 python26-pykde4-03-kptydevice.sip.diff
Patch4:                 python26-pykde4-04-kstartupinfo.sip.diff
Patch5:                 python26-pykde4-05-kacl.sip.diff
Patch6:                 python26-pykde4-06-global.sip.diff
Patch7:                 python26-pykde4-07-factory.sip.diff

BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
SUNW_Copyright:         %{name}.copyright
%include default-depend.inc
Requires: SFEkdelibs4
Requires: SUNWPython26
Requires: SUNWdbus-python26
BuildRequires: SFEkdelibs4-devel
BuildRequires: SUNWPython26-devel
BuildRequires: SUNWdbus-python26-devel
BuildRequires: SFEpython26-sip

%description
Python bindings for KDE4.

%package devel
Summary:                %{summary} - Development files.
SUNW_BaseDir:           %{_prefix}
%include default-depend.inc
Requires: %{name}
Requires: SFEkdelibs4-devel
Requires: SUNWPython26-devel
Requires: SUNWdbus-python26-devel
Requires: SFEpython26-sip
Conflicts: SFEpyqt-devel

%prep
%setup -q -c -n %name-%version
cd kdebindings-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
cd ..
mkdir kdebld

%build
export QTDIR=%{_prefix}
export QT_INCLUDES=%{_includedir}/qt4
OPATH=${PATH}

cd kdebld
export PYTHON="/usr/bin/python%{python_version}"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
export QMAKESPEC=%{_datadir}/qt4/mkspecs/solaris-g++
export PATH="%{qt4_bin_path}:${OPATH}"

cmake   ../kdebindings-%{version} -DCMAKE_INSTALL_PREFIX=%{_prefix}      \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DCMAKE_INCLUDE_PATH="%{gnu_inc}"                               \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DSYSCONF_INSTALL_DIR=%{_sysconfdir}                            \
        -DBUILD_SHARED_LIBS=On                                          \
        -DKDE4_ENABLE_HTMLHANDBOOK=Off                                  \
        -DENABLE_KORUNDUM=off -DENABLE_SMOKE=off                        \
        -DENABLE_RUBY=off -DENABLE_PYKDE4=on                            \
        -DENABLE_KROSSPYTHON=off                                        \
        -DENABLE_KROSSRUBY=off                                          \
        -DENABLE_KROSSJAVA=off                                          \
        -DENABLE_KROSSFALCON=off                                        \
        -DENABLE_PHP=off                                                \
        -DENABLE_FALCON=off                                             \
        -DENABLE_CSHARP=off                                             \
        -DENABLE_JAVA=off                                               \
        -DCMAKE_VERBOSE_MAKEFILE=1 > config.log 2>&1

make
cd ..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT

OPATH=${PATH}

cd kdebld
export PATH="%{qt4_bin_path}:${OPATH}"
make install DESTDIR=$RPM_BUILD_ROOT

mv ${RPM_BUILD_ROOT}/%{_libdir}/python%{python_version}/site-packages \
   ${RPM_BUILD_ROOT}/%{_libdir}/python%{python_version}/vendor-packages
cd ..
export PATH="${OPATH}"


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/*

%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*

%defattr(-,root,other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/apps
%dir %attr (0755, root, other) %{_datadir}/apps/pykde4
%{_datadir}/apps/pykde4/kde4.py*

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/sip
%dir %attr (0755, root, bin) %{_datadir}/sip/PyKDE4
%{_datadir}/sip/PyKDE4/*

%defattr(-,root,other)
%dir %attr (0755, root, other) %{_datadir}/apps
%dir %attr (0755, root, other) %{_datadir}/apps/pykde4
%{_datadir}/apps/pykde4/pykdeuic4.py*
%dir %attr (0755, root, other) %{_datadir}/apps/pykde4/examples
%{_datadir}/apps/pykde4/examples/*

%changelog
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Initial version.
