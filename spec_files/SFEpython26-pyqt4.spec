#
# spec file for package SFEpython26-pyqt4
#
# includes module(s): pyqt4
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define python_version 2.6

Name:			SFEpython26-pyqt4
Summary:		Python bindings for Qt4
License:		GPLv3 or GPLv2 with exceptions
Version:		4.5
Source:			http://www.riverbankcomputing.com/static/Downloads/PyQt4/PyQt-x11-gpl-%{version}.tar.gz
URL:			http://www.riverbankcomputing.co.uk/software/pyqt/
Patch1:                 PyQt-x11-gpl-4.4.4-64bit.diff
Patch2:                 PyQt-x11-gpl-4.4.4-QT_SHARED.diff

BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
SUNW_Copyright:         %{name}.copyright
%include default-depend.inc
Requires: SFEqt4
Requires: SUNWPython26
Requires: SUNWdbus-python26
BuildRequires: SFEqt4-devel
BuildRequires: SUNWPython26-devel
BuildRequires: SUNWdbus-python26-devel
BuildRequires: SFEpython26-sip

%description
Python bindings for Qt4.

%package devel
Summary:                %{summary} - Development files.
SUNW_BaseDir:           %{_prefix}
%include default-depend.inc
Requires: %{name}
Requires: SFEqt4-devel
Requires: SUNWPython26-devel
Requires: SUNWdbus-python26-devel
Requires: SFEpython26-sip
Conflicts: SFEpyqt-devel

%prep
%setup -q -c -n %name-%version
cd PyQt-x11-gpl-%{version}
%patch1 -p1
%patch2 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp PyQt-x11-gpl-%{version} PyQt-x11-gpl-%{version}-64
%endif

%build
export QTDIR=%{_prefix}
export QT_INCLUDES=%{_includedir}/qt4
OPATH=${PATH}

%ifarch amd64 sparcv9
cd PyQt-x11-gpl-%{version}-64

export PYTHON="/usr/bin/%{_arch64}/python%{python_version}"
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64}"
export PATH="%{qt4_bin_path64}:%{_bindir}/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${OPATH}"
export QMAKESPEC=%{_datadir}/qt4/mkspecs/solaris-g++-64

${PYTHON} configure.py --confirm-license \
    --destdir=%{_libdir}/python%{python_version}/vendor-packages \
    --bindir=%{_bindir}/%{_arch64} \
    --verbose --qmake=%{qt4_bin_path64}/qmake

make
cd ..
%endif

cd PyQt-x11-gpl-%{version}
export PYTHON="/usr/bin/python%{python_version}"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
export QMAKESPEC=%{_datadir}/qt4/mkspecs/solaris-g++
export PATH="%{qt4_bin_path}:${OPATH}"

${PYTHON} configure.py --confirm-license \
    --destdir=%{_libdir}/python%{python_version}/vendor-packages \
    --bindir=%{_bindir} \
    --verbose --qmake=%{qt4_bin_path}/qmake

make
cd ..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT

OPATH=${PATH}

%ifarch amd64 sparcv9
cd PyQt-x11-gpl-%{version}-64
export PATH="%{qt4_bin_path64}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
mkdir ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/PyQt4/64
mv ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/PyQt4/*.so \
   ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/PyQt4/64
cd ..
%endif

cd PyQt-x11-gpl-%{version}
export PATH="%{qt4_bin_path}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/%{name}
cp GPL* ${RPM_BUILD_ROOT}%{_docdir}/%{name}
cp LICENSE* ${RPM_BUILD_ROOT}%{_docdir}/%{name}
cp OPENSOURCE* ${RPM_BUILD_ROOT}%{_docdir}/%{name}

cd ..
export PATH="${OPATH}"


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/%{name}
%doc %{_docdir}/%{name}/*

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/py*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/py*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/sip
%dir %attr (0755, root, bin) %{_datadir}/sip/PyQt4
%{_datadir}/sip/PyQt4/*

%changelog
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Initial version.
