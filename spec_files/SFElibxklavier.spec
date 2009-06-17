#
# spec file for package SFElibxklavier
#
# includes module(s): libxklavier
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define _python_ver      2.5
%define _orig_ver        3.9
Name:                    SFElibxklavier
Summary:                 A library providing high-level API for the X Keyboard Extension.
Version:                 %{_orig_ver}
URL:                     http://freedesktop.org/wiki/Software/LibXklavier
Source:                  %{sf_download}/gswitchit/libxklavier-%{version}.tar.bz2
Patch1:                  libxklavier-01-test_config.c.diff
License:                 LGPLv2

SUNW_BaseDir:            %{_basedir}
#SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:               SUNWlxml
Requires:               SUNWglib2
Requires:               SUNWiso-codes
Requires:               SUNWxorg-clientlibs
Requires:               SUNWxwplt
BuildRequires:          SUNWxorg-headers
BuildRequires:          FSWxorg-headers
BuildRequires:          SUNWlxml-devel
BuildRequires:          SUNWglib2-devel
BuildRequires:          SUNWiso-codes-devel
BuildRequires:          SUNWgnome-common-devel

%description
libxklavier is a library providing a high-level API for the X Keyboard
Extension (XKB). This library is intended to support XFree86 and other
commercial X servers. It is useful for creating XKB-related software
(layout indicators etc).

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:          SUNWxorg-headers
Requires:          FSWxorg-headers
Requires:          SUNWlxml-devel
Requires:          SUNWglib2-devel
Requires:          SUNWiso-codes-devel
Requires:          SUNWgnome-common-devel

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -c -n %name-%version
cd libxklavier-%{_orig_ver}
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp libxklavier-%{_orig_ver} libxklavier-%{_orig_ver}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export PYTHON=%{_bindir}/python%{_python_ver}

%ifarch amd64 sparcv9
cd libxklavier-%{_orig_ver}-64
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 %{xorg_lib_path64}"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}              \
            --libdir=%{_libdir}/%{_arch64}              \
            --with-xkb-base=%{_prefix}/X11/share/X11/xkb        \
            --with-xkb-bin-base=%{_prefix}/X11/bin/%{_arch64}   \
            --enable-shared		                        \
            --disable-static

make -j$CPUS 
cd ..
%endif

cd libxklavier-%{_orig_ver}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags %{xorg_lib_path}"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}                  \
            --libdir=%{_libdir}                  \
            --with-xkb-base=%{_prefix}/X11/share/X11/xkb \
            --with-xkb-bin-base=%{_prefix}/X11/bin       \
            --enable-shared		                 \
            --disable-static

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd libxklavier-%{_orig_ver}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd libxklavier-%{_orig_ver}
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
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/*


%changelog
* Wed Jun 17 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version
