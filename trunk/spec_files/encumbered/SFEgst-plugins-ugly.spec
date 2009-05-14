#
# spec file for package SFEgst-plugins-ugly
#
# includes module(s): gst-plugins-ugly
#
#
%include Solaris.inc

Name:                    SFEgst-plugins-ugly
Summary:                 Well supported encumbered GStreamer plug-ins
Version:                 0.10.11
Source:                  http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-%{version}.tar.bz2
URL:                     http://www.gstreamer.net/
Patch1:                  gst-plugins-ugly-02-gstmad.c.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
License:                 LGPL
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibcdio
BuildRequires: SFElibcdio-devel
Requires: SUNWgnu-gettext
BuildRequires: SUNWgnu-gettext-devel
Requires: SFElibmpeg2
BuildRequires: SFElibmpeg2-devel
Requires: SFEliba52
BuildRequires: SFEliba52-devel
Requires: SFElibmad
BuildRequires: SFElibmad-devel
Requires: SFElibiec61883
BuildRequires: SFElibiec61883-devel
Requires: SFElibraw1394
BuildRequires: SFElibraw1394-devel
Requires: SFElibid3tag
BuildRequires: SFElibid3tag-devel
Requires: SFElibdvdread
BuildRequires: SFElibdvdread-devel
Requires: SFElibdvdnav
BuildRequires: SFElibdvdnav-devel
Requires: SFElame
BuildRequires: SFElame-devel
Requires: SFEtwolame
BuildRequires: SFEtwolame-devel
Requires: SUNWgnome-media
BuildRequires: SUNWgnome-media-devel

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains well-written plug-ins that can't be shipped in
gstreamer-plugins-good because:
- the license is not LGPL
- the license of the library is not LGPL
- there are possible licensing issues with the code.

%prep
%setup -q -c -n %name-%version
cd gst-plugins-ugly-%version
%patch1 -p1
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd gst-plugins-ugly-%{version}
export CFLAGS="%optflags -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/us/gnu/lib"
export PYTHON=/usr/bin/python2.5

bash ./configure \
        --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --localstatedir=%{_localstatedir} \
        --disable-debug \
        --disable-dependency-tracking \
        --enable-shared --disable-static \
        --disable-libtool-lock \
        --enable-nls \
        --disable-experimental \
        --enable-a52dec \
        --enable-amrnb \
        --enable-dvdread \
        --enable-dvdnav \
        --enable-lame \
        --enable-id3tag \
        --enable-mad \
        --enable-mpeg2dec \
        --with-libiconv-prefix=%{_prefix}/gnu \
        --with-libintl-prefix=%{_prefix}/gnu \
        --with-a52dec-prefix=%{_prefix} --with-pic

make -j $CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

cd gst-plugins-ugly-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..
find ${RPM_BUILD_ROOT} -name "*.la" | xargs rm -f

rm -f ${RPM_BUILD_ROOT}%{_libdir}/gstreamer-0.10/libgstoss4audio.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/gstreamer-0.10/libgstselector.so


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/gstreamer-0.10
%{_libdir}/gstreamer-0.10/libgstasf.so
%{_libdir}/gstreamer-0.10/libgstdvdlpcmdec.so
%{_libdir}/gstreamer-0.10/libgstdvdsub.so
%{_libdir}/gstreamer-0.10/libgstiec958.so
%{_libdir}/gstreamer-0.10/libgstmpegaudioparse.so
%{_libdir}/gstreamer-0.10/libgstmpegstream.so
%{_libdir}/gstreamer-0.10/libgstrmdemux.so
%{_libdir}/gstreamer-0.10/libgsta52dec.so
%{_libdir}/gstreamer-0.10/libgstdvdread.so
%{_libdir}/gstreamer-0.10/libgstlame.so
%{_libdir}/gstreamer-0.10/libgstmad.so
%{_libdir}/gstreamer-0.10/libgstmpeg2dec.so
%{_libdir}/gstreamer-0.10/libgstcdio.so
%{_libdir}/gstreamer-0.10/libgsttwolame.so


%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale/*/LC_MESSAGES/gst-plugins-ugly-0.10.mo

%changelog
* Tue May 12 2009 - moinakg@belenix.org
- Initial version
