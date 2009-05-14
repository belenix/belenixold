#
# spec file for package SFEgst-ffmpeg
#
# includes module(s): gst-ffmpeg
#
#
%include Solaris.inc

Name:                    SFEgst-ffmpeg
Summary:                 GStreamer Streaming-media framework plug-in using FFmpeg.
Version:                 0.10.7
Source:                  http://gstreamer.freedesktop.org/src/gst-ffmpeg/gst-ffmpeg-%{version}.tar.bz2
Patch1:                  gst-ffmpeg-01-gstffmpegdemux.c.diff
Patch2:                  gst-ffmpeg-02-gstffmpeg.h.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
License:                 GPLv2
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEffmpeg
BuildRequires: SFEffmpeg-devel
Requires: SUNWgnome-media
BuildRequires: SUNWgnome-media-devel

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related. Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

This plugin contains the FFmpeg codecs, containing codecs for most popular
multimedia formats.

%prep
%setup -q -c -n %name-%version
cd gst-ffmpeg-%version
%patch1 -p1
%patch2 -p1
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

cd gst-ffmpeg-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared                  \
            --disable-static                 \
            --disable-valgrind               \
            --disable-debug                  \
            --with-pic                       \
            --with-system-ffmpeg

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

cd gst-ffmpeg-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..
find ${RPM_BUILD_ROOT} -name "*.la" | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Tue May 12 2009 - moinakg@belenix.org
- Initial version
