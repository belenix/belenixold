#
# spec file for package SFEpython26-sip
#
# includes module(s): sip
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define python_version 2.6

Name:			SFEpython26-sip
Summary:		Python binding creator for C++ libraries (For Python 2.6)
License:		Pythonish
Version:		4.8
Source:			http://www.riverbankcomputing.com/static/Downloads/sip4/sip-%{version}.tar.gz
URL:			http://www.riverbankcomputing.co.uk/sip
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
SUNW_Copyright:         %{name}.copyright
%include default-depend.inc
Requires: SUNWPython26
BuildRequires: SUNWPython26-devel
Conflicts:     SFEsip

%description
SIP is a tool for generating bindings for C++ classes so that they can be
accessed as normal Python classes. SIP takes many of its ideas from SWIG but,
because it is specifically designed for C++ and Python, is able to generate
tighter bindings. SIP is so called because it is a small SWIG.

SIP was originally designed to generate Python bindings for KDE and so has
explicit support for the signal slot mechanism used by the Qt/KDE class
libraries. However, SIP can be used to generate Python bindings for any C++
class library.

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp sip-%{version} sip-%{version}-64
%endif

%build
%ifarch amd64 sparcv9
cd sip-%{version}-64

export PYTHON="/usr/bin/%{_arch64}/python%{python_version}"
export CFLAGS="%optflags64"
export LFLAGS="%_ldflags64 %{gnu_lib_path64}"
${PYTHON} configure.py --platform=solaris-g++-64 \
    --bindir=%{_bindir}/%{_arch64} \
    --destdir=%{_libdir}/python%{python_version}/vendor-packages \
    LFLAGS="${LFLAGS}"

make
cd ..
%endif

cd sip-%{version}
export PYTHON="/usr/bin/python%{python_version}"
export CFLAGS="%optflags"
export LFLAGS="%_ldflags %{gnu_lib_path}"
${PYTHON} configure.py --platform=solaris-g++ \
    --bindir=%{_bindir} \
    --destdir=%{_libdir}/python%{python_version}/vendor-packages \
    LFLAGS="${LFLAGS}"
make
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd sip-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
mkdir ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/64
mv ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/sip.so \
   ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/64
cd ..
%endif

cd sip-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sip
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/python%{python_version}/sip.h
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/sip
%endif


%changelog
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Initial version.

