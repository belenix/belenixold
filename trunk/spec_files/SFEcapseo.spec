#
# spec file for package SFEcapseo
#
# includes module(s): Capseo
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFEcapseo
Summary:                 Capseo - a realtime video encoder/decoder library
%define  tarball_dir capseo-0.3.0~svn158.orig
Version:                 0.3.0_svn158
URL:                     http://code.ninchens.net/projects/capseo
Source:                  http://www.belenix.org/binfiles/capseo_%{version}.tar.gz
Patch1:                  capseo.pc.in.17.diff
Patch2:                  capseo.encode-raw.cpp.13.diff
Patch3:                  capseo.encode-stream.cpp.14.diff
Patch4:                  capseo.cpsinfo.cpp.0.diff
Patch5:                  capseo.cpsplay.cpp.1.diff
Patch6:                  capseo.cpsrecode.cpp.2.diff
Patch7:                  capseo.cursor.cpp.9.diff
Patch8:                  capseo.encode.cpp.10.diff
Patch9:                  capseo.global.cpp.8.diff
Patch10:                 capseo.stream.cpp.11.diff


License:                 GPL2
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWlibtheora
Requires:                SUNWogg-vorbis
Requires:                SUNWspeex
BuildRequires:           SUNWlibtheora-devel
BuildRequires:           SUNWogg-vorbis-devel
BuildRequires:           SUNWspeex-devel
BuildRequires:           SFEyasm

%include default-depend.inc

%prep
%if %cc_is_gcc
%else
%error "This SPEC should be built with Gcc. Please set CC and CXX env variables"
%endif

%setup -q -c -n %name-%version
cd %{tarball_dir}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp %{tarball_dir} %{tarball_dir}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd %{tarball_dir}-64

%ifarch sparcv9
	accel=generic
%else
%ifarch amd64
        accel=amd64
%endif
%endif

export CFLAGS="%optflags64"
export CPPFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 -L/usr/lib/%{_arch64} -R/usr/lib/%{_arch64}"
X11_LIBS="-L/usr/X11/lib/%{_arch64} -R/usr/X11/lib/%{_arch64} -lX11"
export X11_LIBS


# smack the timestamps into line
touch -r configure *

chmod 0755 configure

./configure \
        --prefix=%{_prefix} \
        --bindir=%{_bindir}/%{_arch64} \
        --sbindir=%{_sbindir}/%{_arch64} \
        --libdir=%{_libdir}/%{_arch64} \
        --libexecdir=%{_libexecdir}/%{_arch64} \
        --localstatedir=%{_localstatedir} \
        --disable-warnings \
        --disable-debug \
        --disable-dependency-tracking \
        --enable-shared --disable-static \
        --disable-libtool-lock \
        --enable-examples --enable-theora --with-pic --with-accel=$accel

make -j $CPUS
cd ..
%endif

cd %{tarball_dir}
accel=x86
export CFLAGS="%optflags"
export CPPFLAGS="%optflags"
export LDFLAGS="%_ldflags"
X11_LIBS="-L/usr/X11/lib -R/usr/X11/lib -lX11"
export X11_LIBS

# smack the timestamps into line
touch -r configure *

chmod 0755 configure

./configure \
        --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --localstatedir=%{_localstatedir} \
        --disable-warnings \
        --disable-debug \
        --disable-dependency-tracking \
        --enable-shared --disable-static \
        --disable-libtool-lock \
        --enable-examples --enable-theora --with-pic --with-accel=$accel

make -j $CPUS
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd %{tarball_dir}-64
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/lib*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd %{tarball_dir}
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libcapseo.so.0.2.0
%{_libdir}/libcapseo.so.0
%{_libdir}/libcapseo.so
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/capseo.pc
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/cpsinfo
%{_bindir}/cpsplay
%{_bindir}/cpsrecode

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%_arch64
%{_libdir}/%_arch64/libcapseo.so.0.2.0
%{_libdir}/%_arch64/libcapseo.so.0
%{_libdir}/%_arch64/libcapseo.so
%dir %attr (0755, root, other) %{_libdir}/%_arch64/pkgconfig
%{_libdir}/%_arch64/pkgconfig/capseo.pc
%dir %attr (0755, root, bin) %{_bindir}/%_arch64
%{_bindir}/%_arch64/cpsinfo
%{_bindir}/%_arch64/cpsplay
%{_bindir}/%_arch64/cpsrecode
%endif

%changelog
* Sun May 03 2009 - moinakg@belenix.org
- Initial spec file
