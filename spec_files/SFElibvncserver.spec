#
# spec file for package SFElibvncserver
#
# includes module(s): libvncserver
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFElibvncserver
Summary:                 Library to make writing a vnc server easy
Version:                 0.9.7
URL:                     http://libvncserver.sourceforge.net/
Source:                  %{sf_download}/libvncserver/LibVNCServer-%{version}.tar.gz
License:                 GPLv2+
Patch1:                  libvncserver-01-close_server_socket.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:               SUNWjpg
Requires:               SUNWzlib
BuildRequires:          SUNWjpg-devel

%description
LibVNCServer makes writing a VNC server (or more correctly, a program
exporting a framebuffer via the Remote Frame Buffer protocol) easy.

It hides the programmer from the tedious task of managing clients and
compression schemata.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:          SUNWzlib
Requires:          SUNWjpg-devel


%prep
%setup -q -c -n %name-%version
cd LibVNCServer-%{version}
%patch1 -p1
find . \( -name "*.c" -o -name "*.h" \) | xargs chmod 644
cd ..

%ifarch amd64 sparcv9
cp -rp LibVNCServer-%{version} LibVNCServer-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd LibVNCServer-%{version}-64
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}          \
            --libdir=%{_libdir}/%{_arch64}          \
            --enable-shared		            \
            --disable-static                        \
            --without-tightvnc-filetransfer

make -j$CPUS 
cd ..
%endif

cd LibVNCServer-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}                     \
            --libdir=%{_libdir}                     \
            --enable-shared		            \
            --disable-static                        \
            --without-tightvnc-filetransfer

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd LibVNCServer-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/lib*.a
cd ..
%endif

cd LibVNCServer-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib*.a
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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Jul 03 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version
