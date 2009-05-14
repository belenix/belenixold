#
# spec file for package SFEgst-plugins-bad
#
# includes module(s): gst-plugins-bad
#
#
%include Solaris.inc

Name:                    SFEgst-plugins-bad
Summary:                 Less supported GStreamer plug-ins that have not been rigorously tested
Version:                 0.10.11
Source:                  http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.bz2
URL:                     http://www.gstreamer.net/
Patch1:                  gst-plugins-bad-1-gstmpeg2encoder.cc.0.diff
Patch2:                  gst-plugins-bad-2-gstmpeg2encpicturereader.hh.1.diff
Patch3:                  gst-plugins-bad-3-gstmpeg2encpicturereader.cc.2.diff
Patch4:                  gst-plugins-bad-4-gstdc1394.c.3.diff
Patch5:                  gst-plugins-bad-5-gstdc1394.h.4.diff
Patch6:                  gst-plugins-bad-6-Makefile.in.5.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
License:                 LGPL
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibavc1394
BuildRequires: SFElibavc1394-devel
Requires: SUNWgnu-gettext
BuildRequires: SUNWgnu-gettext-devel
Requires: SFElibmpeg2
BuildRequires: SFElibmpeg2-devel
Requires: SFEfaad2
BuildRequires: SFEfaad2-devel
Requires: SFElibraw1394
BuildRequires: SFElibraw1394-devel
Requires: SFElibiec61883
BuildRequires: SFElibiec61883-devel
Requires: SFElibmusicbrainz3
BuildRequires: SFElibmusicbrainz3-devel
Requires: SFEnas
BuildRequires: SFEnas-devel
Requires: SFEsdl
BuildRequires: SFEsdl-devel
Requires: SFElibx264
BuildRequires: SFElibx264-devel
Requires: SFExvid
BuildRequires: SFExvid-devel
Requires: SFElibquicktime
BuildRequires: SFElibquicktime-devel
Requires: SFElibgsm
BuildRequires: SFElibgsm-devel
Requires: SFEjasper
BuildRequires: SFEjasper-devel
Requires: SFElibdvdnav
BuildRequires: SFElibdvdnav-devel
Requires: SFElibdts
BuildRequires: SFElibdts-devel
Requires: SFElibsndfile
BuildRequires: SFElibsndfile-devel
Requires: SFEjack
BuildRequires: SFEjack-devel
Requires: SFElibofa
Requires: SUNWbzip
Requires: SUNWogg-vorbis
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWlibexif
BuildRequires: SUNWlibexif-devel
Requires: SUNWliboil
BuildRequires: SUNWliboil-devel
Requires: SUNWgnome-media
BuildRequires: SUNWgnome-media-devel

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

This package contains GStreamer Plugins that are considered to be of bad
quality, even though they might work.

%prep
%setup -q -c -n %name-%version
cd gst-plugins-bad-%version
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd gst-plugins-bad-%{version}
export CFLAGS="%optflags -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/us/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib"
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
        --disable-profiling \
        --enable-vcd \
        --disable-alsa \
        --disable-amrwb \
        --enable-bz2 \
        --enable-cdaudio \
        --enable-dc1394 \
        --enable-divx \
        --enable-metadata \
        --enable-faac \
        --enable-faad \
        --enable-gsm \
        --enable-ivorbis \
        --enable-jack \
        --disable-ladspa \
        --enable-mpeg2enc \
        --disable-musepack \
        --enable-musicbrainz \
        --enable-nas \
        --disable-neon \
        --enable-sdl \
        --enable-sdltest \
        --enable-sndfile \
        --enable-spc \
        --disable-swfdec \
        --disable-theoradec \
        --enable-x264 \
        --enable-xvid \
        --disable-dvb \
        --with-libiconv-prefix=%{_prefix}/gnu \
        --with-libintl-prefix=%{_prefix}/gnu \
        --with-sdl-prefix=%{_prefix} \
        --with-pic

make -j $CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

cd gst-plugins-bad-%{version}
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
%{_libdir}/*.so*
#%{_libdir}/gstreamer-0.10/libgstapp.so
%{_libdir}/gstreamer-0.10/libgstbayer.so
%{_libdir}/gstreamer-0.10/libgstcdxaparse.so
%{_libdir}/gstreamer-0.10/libgstdeinterlace.so
%{_libdir}/gstreamer-0.10/libgstdvdspu.so
%{_libdir}/gstreamer-0.10/libgstfestival.so
#%{_libdir}/gstreamer-0.10/libgstfilter.so
#%{_libdir}/gstreamer-0.10/libgstflvdemux.so
%{_libdir}/gstreamer-0.10/libgstfreeze.so
%{_libdir}/gstreamer-0.10/libgsth264parse.so
#%{_libdir}/gstreamer-0.10/libgstinterleave.so
%{_libdir}/gstreamer-0.10/libgstrfbsrc.so
#%{_libdir}/gstreamer-0.10/libgstmpegtsparse.so
%{_libdir}/gstreamer-0.10/libgstmpeg4videoparse.so
%{_libdir}/gstreamer-0.10/libgstmpegvideoparse.so
%{_libdir}/gstreamer-0.10/libgstmve.so
%{_libdir}/gstreamer-0.10/libgstnsf.so
%{_libdir}/gstreamer-0.10/libgstnuvdemux.so
%{_libdir}/gstreamer-0.10/libgstrawparse.so
%{_libdir}/gstreamer-0.10/libgstreal.so
#%{_libdir}/gstreamer-0.10/libgstreplaygain.so
%{_libdir}/gstreamer-0.10/libgstrtpmanager.so
%{_libdir}/gstreamer-0.10/libgstsdpelem.so
%{_libdir}/gstreamer-0.10/libgstspeed.so
%{_libdir}/gstreamer-0.10/libgststereo.so
%{_libdir}/gstreamer-0.10/libgsttta.so
%{_libdir}/gstreamer-0.10/libgstvideosignal.so
%{_libdir}/gstreamer-0.10/libgstvmnc.so
%{_libdir}/gstreamer-0.10/libgsty4menc.so
%{_libdir}/gstreamer-0.10/libgstbz2.so
#%{_libdir}/gstreamer-0.10/libgstfaac.so
%{_libdir}/gstreamer-0.10/libgstfaad.so
%{_libdir}/gstreamer-0.10/libgstgsm.so
%{_libdir}/gstreamer-0.10/libgstmetadata.so
%{_libdir}/gstreamer-0.10/libgsttrm.so
%{_libdir}/gstreamer-0.10/libgstsdl.so
%{_libdir}/gstreamer-0.10/libgstsndfile.so
%{_libdir}/gstreamer-0.10/libgstx264.so
%{_libdir}/gstreamer-0.10/libgstxvid.so
%{_libdir}/gstreamer-0.10/libgstxdgmime.so
%{_libdir}/gstreamer-0.10/libgstjp2k.so
%{_libdir}/gstreamer-0.10/libgstaiffparse.so
%{_libdir}/gstreamer-0.10/libgstscaletempoplugin.so
%{_libdir}/gstreamer-0.10/libresindvd.so
%{_libdir}/gstreamer-0.10/libgstaacparse.so
%{_libdir}/gstreamer-0.10/libgstdtmf.so
%{_libdir}/gstreamer-0.10/libgstnassink.so
%{_libdir}/gstreamer-0.10/libgstqtmux.so
%{_libdir}/gstreamer-0.10/libgstautoconvert.so
%{_libdir}/gstreamer-0.10/libgstmpegdemux.so
%{_libdir}/gstreamer-0.10/libgstdeinterlace2.so
%{_libdir}/gstreamer-0.10/libgstmxf.so
%{_libdir}/gstreamer-0.10/libgstlegacyresample.so
%{_libdir}/gstreamer-0.10/libgstrtpmux.so
%{_libdir}/gstreamer-0.10/libgstofa.so
%{_libdir}/gstreamer-0.10/libgstamrparse.so
%{_libdir}/gstreamer-0.10/libgstliveadder.so
%{_libdir}/gstreamer-0.10/libgstcamerabin.so
%{_libdir}/gstreamer-0.10/libgstpcapparse.so
%{_libdir}/gstreamer-0.10/libgstdtsdec.so
%{_libdir}/gstreamer-0.10/libgstapexsink.so
%{_libdir}/gstreamer-0.10/libgstmpegtsmux.so
%{_libdir}/gstreamer-0.10/libgstsubenc.so
%{_libdir}/gstreamer-0.10/libgstdccp.so
%{_libdir}/gstreamer-0.10/libgstjack.so
%{_libdir}/gstreamer-0.10/libgstsiren.so
%{_libdir}/gstreamer-0.10/libgstflv.so
%{_libdir}/gstreamer-0.10/libgstvalve.so
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale/*/LC_MESSAGES/gst-plugins-bad-0.10.mo

%changelog
* Tue May 12 2009 - moinakg@belenix.org
- Initial version
