#
# spec file for package SFElibcaptury
#
# includes module(s): Libcaptury
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFElibcaptury
Summary:                 libcaptury is a realtime multimedia capturing framework
Version:                 0.3.0
URL:                     http://www.ohloh.net/p/captury
Source:                  http://www.belenix.org/binfiles/libcaptury-%{version}.tar.bz2
Patch1:                  libcaptury-01.capture-region.cpp.diff
Patch2:                  libcaptury-02.capture-screen.cpp.diff
%define tarball_dir libcaptury-%{version}

License:                 GPLv2+
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                SFEcapseo
Requires:                SUNWogg-vorbis
Requires:                SUNWxwplt
BuildRequires:           SFEcapseo
BuildRequires:           SUNWogg-vorbis-devel
BuildRequires:           SUNWxwplt

%description
libcaptury is a realtime multimedia capturing framework for currently
OpenGL video (to be extended to XShm and audio/alsa soon). Its uses
are e.g. for capturing video from external OpenGL applications (via
captury itself) and is currently also used by KDE?s kwin to record
your desktop efficiently (VideoRecord plugin).

libcaptury supports full encoding as well as incremential(!) encoding
by only regions from the screen that have actually changed. Window
managers (like kwin) do know of such areas and can make use of it.

%prep
%if %cc_is_gcc
%else
%error "This SPEC should be built with Gcc. Please set CC and CXX env variables"
%endif

%setup -q -c -n %name-%version
cd %{tarball_dir}
%patch1 -p1
%patch2 -p1
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
export LDFLAGS="%_ldflags64 -L/usr/lib/%{_arch64} -R/usr/lib/%{_arch64} %{gnu_lib_path64}"
X11_LIBS="-L/usr/X11/lib/%{_arch64} -R/usr/X11/lib/%{_arch64} -lX11"
export X11_LIBS

find . -type f | xargs touch
bash ./autogen.sh
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
        --enable-examples

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

find . -type f | xargs touch
bash ./autogen.sh
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
        --enable-examples

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
%{_libdir}/libcaptury.so.0.3.0
%{_libdir}/libcaptury.so.0
%{_libdir}/libcaptury.so
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/libcaptury.pc

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%_arch64
%{_libdir}/%_arch64/libcaptury.so.0.3.0
%{_libdir}/%_arch64/libcaptury.so.0
%{_libdir}/%_arch64/libcaptury.so
%dir %attr (0755, root, other) %{_libdir}/%_arch64/pkgconfig
%{_libdir}/%_arch64/pkgconfig/libcaptury.pc
%endif

%changelog
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Initial version.
