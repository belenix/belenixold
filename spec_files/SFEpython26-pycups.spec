#
# spec file for package SFEpython26-pycups
#
# includes module(s): pycups
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define python_version 2.6

Name:			SFEpython26-pycups
Summary:		Python bindings for CUPS
License:		GPLv2
Version:		1.9.46
Source:			http://cyberelk.net/tim/data/pycups/pycups-%{version}.tar.bz2
URL:			http://cyberelk.net/tim/software/pycups/
Patch1:                 pycups-01-Makefile.diff

BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
#SUNW_Copyright:         %{name}.copyright
%include default-depend.inc
Requires: SFEcups
Requires: SUNWPython26
Requires: SUNWcups-manager
BuildRequires: SFEcups-devel
BuildRequires: SUNWPython26-devel

%description
Python bindings for CUPS.

%prep
%setup -q -c -n %name-%version
cd pycups-%{version}
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp pycups-%{version} pycups-%{version}-64
%endif

%build
export QTDIR=%{_prefix}
export QT_INCLUDES=%{_includedir}/qt4
export PYTHON="/usr/bin/python%{python_version}"
ln -s ${PYTHON} python
export PATH=`pwd`:${PATH}

%ifarch amd64 sparcv9
cd pycups-%{version}-64

export PYTHON="/usr/bin/%{_arch64}/python%{python_version}"
export CFLAGS="%optflags64 -DVERSION=\\\"%{version}\\\""
export LDFLAGS="%_ldflags64 %{gnu_lib_path64}"

make
cd ..
%endif

cd pycups-%{version}
export PYTHON="/usr/bin/python%{python_version}"
export CFLAGS="%optflags -DVERSION=\\\"%{version}\\\""
export LDFLAGS="%_ldflags %{gnu_lib_path}"

make
cd ..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT
export PATH=`pwd`:${PATH}

%ifarch amd64 sparcv9
cd pycups-%{version}-64
export PYTHON="/usr/bin/%{_arch64}/python%{python_version}"
export CFLAGS="%optflags64 -DVERSION=\\\"%{version}\\\""
export LDFLAGS="%_ldflags64 %{gnu_lib_path64}"

make install DESTDIR=${RPM_BUILD_ROOT}
mv ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/site-packages \
   ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages
mkdir ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/64
mv ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/*.so \
   ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/64
cd ..
%endif

cd pycups-%{version}
export PYTHON="/usr/bin/python%{python_version}"
export CFLAGS="%optflags -DVERSION=\\\"%{version}\\\""
export LDFLAGS="%_ldflags %{gnu_lib_path}"

make install DESTDIR=${RPM_BUILD_ROOT}
mv ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/site-packages/* \
   ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages
rmdir ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/site-packages
mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/%{name}
cp COPYING* ${RPM_BUILD_ROOT}%{_docdir}/%{name}
cp NEWS* ${RPM_BUILD_ROOT}%{_docdir}/%{name}
cp README* ${RPM_BUILD_ROOT}%{_docdir}/%{name}

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

%changelog
* Fri Jul 03 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
