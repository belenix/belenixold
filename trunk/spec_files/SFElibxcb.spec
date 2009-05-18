#
# spec file for package SFElibxcb
#
# includes module(s): libxcb
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define _python_ver      2.5
Name:                    SFElibxcb
Summary:                 An interface to the X Window System protocol, which replaces the current Xlib interface.
Version:                 1.2
Source:                  http://xcb.freedesktop.org/dist/libxcb-%{version}.tar.gz
URL:                     http://xcb.freedesktop.org/
License:                 MIT_X11

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:               SUNWxorg-clientlibs
Requires:               SUNWxwplt
Requires:               SFExcb-proto
BuildRequires:          SFExcb-proto
BuildRequires:          SUNWxorg-headers
BuildRequires:          FSWxorg-headers
BuildRequires:          SFEdoxygen

%description
The X protocol C-language Binding (XCB) is a replacement for Xlib featuring
a small footprint, latency hiding, direct access to the protocol, improved
threading support, and extensibility.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:              SFExcb-proto
Requires:              SUNWxorg-headers
Requires:              FSWxorg-headers
Requires:              SFEdoxygen

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp libxcb-%{version} libxcb-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export PYTHON=%{_bindir}/python%{_python_ver}

%ifarch amd64 sparcv9
cd libxcb-%{version}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}              \
            --libdir=%{_libdir}/%{_arch64}              \
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 
cd ..
%endif

cd libxcb-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared                  \
            --disable-static

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd libxcb-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd libxcb-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/libxcb
%{_docdir}/libxcb/*


%changelog
* Sun Apr 17 2009 - moinakg@belenix.org
- Initial version
