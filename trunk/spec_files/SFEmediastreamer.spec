#
# spec file for package SFEmediastreamer
#
# includes module(s): mediastreamer
#
#
%include Solaris.inc

Name:                    SFEmediastreamer
Summary:                 A modular sound and video processing and streaming library
Version:                 2.2.4
License:                 GPL
Source:                  http://ftp.twaren.net/Unix/NonGNU/linphone/mediastreamer/mediastreamer-%{version}.tar.gz
URL:                     http://savannah.nongnu.org/projects/linphone
Patch1:                  mediastreamer-1-mscommon.c.0.diff
Patch2:                  mediastreamer-2-msqueue.c.1.diff
Patch3:                  mediastreamer-3-alaw.c.2.diff
Patch4:                  mediastreamer-4-arts.c.3.diff
Patch5:                  mediastreamer-5-dtmfgen.c.4.diff
Patch6:                  mediastreamer-6-gsm.c.5.diff
Patch7:                  mediastreamer-7-ice.c.6.diff
Patch8:                  mediastreamer-8-macsnd.c.7.diff
Patch9:                  mediastreamer-9-msconf.c.8.diff
Patch10:                 mediastreamer-10-msfileplayer.c.9.diff
Patch11:                 mediastreamer-11-msfilerec.c.10.diff
Patch12:                 mediastreamer-12-msjoin.c.11.diff
Patch14:                 mediastreamer-14-msrtp.c.13.diff
Patch15:                 mediastreamer-15-msspeex.c.14.diff
Patch16:                 mediastreamer-16-msv4l.c.15.diff
Patch17:                 mediastreamer-17-msv4m.c.16.diff
Patch18:                 mediastreamer-18-msvideo.c.17.diff
Patch19:                 mediastreamer-19-msvolume.c.18.diff
Patch20:                 mediastreamer-20-nowebcam.c.19.diff
Patch21:                 mediastreamer-21-oss.c.20.diff
Patch22:                 mediastreamer-22-pasnd.c.21.diff
Patch23:                 mediastreamer-23-pixconv.c.22.diff
Patch24:                 mediastreamer-24-rfc3984.c.23.diff
Patch26:                 mediastreamer-26-sizeconv.c.25.diff
Patch27:                 mediastreamer-27-speexec.c.26.diff
Patch28:                 mediastreamer-28-tee.c.27.diff
Patch29:                 mediastreamer-29-theora.c.28.diff
Patch30:                 mediastreamer-30-ulaw.c.29.diff
Patch31:                 mediastreamer-31-videodec.c.30.diff
Patch32:                 mediastreamer-32-videoenc.c.31.diff
Patch33:                 mediastreamer-33-nowebcam.h.32.diff
Patch34:                 mediastreamer-34-videoout.c.33.diff
Patch35:                 mediastreamer-35-Makefile.in.34.diff
Patch36:                 mediastreamer-36-msqueue.h.35.diff
Patch37:                 mediastreamer-37-ice.h.36.diff
Patch38:                 mediastreamer-38-mediastream.h.37.diff
Patch39:                 mediastreamer-39-msrtp.h.38.diff
Patch40:                 mediastreamer-40-msvideo.h.39.diff
Patch41:                 mediastreamer-41-rfc3984.h.40.diff
Patch42:                 mediastreamer-42-mediastream.c.41.diff
Patch43:                 mediastreamer-43-Makefile.in.42.diff
Patch44:                 mediastreamer-44-configure.43.diff
Patch45:                 mediastreamer-45-mediastreamer.pc.in.44.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                SFEortp
BuildRequires:           SFEortp-devel
Requires:                SFElibgsm
BuildRequires:           SFElibgsm-devel
Requires:                SFEsdl
BuildRequires:           SFEsdl-devel
Requires:                SFEjack
BuildRequires:           SFEjack-devel
Requires:                SFEportaudio
BuildRequires:           SFEportaudio-devel
Requires:                SFElibsamplerate
BuildRequires:           SFElibsamplerate-devel
Requires:                SUNWogg-vorbis
BuildRequires:           SUNWogg-vorbis-devel
Requires:                SUNWopenssl-libraries
BuildRequires:           SUNWopenssl-include

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:                SFEortp-devel
Requires:                SFElibgsm-devel
Requires:                SFEsdl-devel
Requires:                SFEjack-devel
Requires:                SFEportaudio-devel
Requires:                SFElibsamplerate-devel
Requires:                SUNWogg-vorbis-devel
Requires:                SUNWopenssl-include

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%description
Using mediastreamer2 will allow you to chain filters in a graph. Each
filter will be responsible for doing some kind of processing and will
deliver data to the next filter. As an example, you could get some
data from network and unpack it in an RTP filter. This RTP filter will
deliver the data to a decoder (speex, G711...) which will deliver it
to a filter that is able to play the PCM data or record it into a .wav
file.

There is a doxygen documentation for more information.


%prep
%setup -q -c -n %name-%version
cd mediastreamer-%version
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
%patch11 -p1
%patch12 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
cd ..

%build
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

cd mediastreamer-%{version}
export CFLAGS="%optflags -fno-schedule-insns -fschedule-insns2 -fstrict-aliasing"
export CXXFLAGS="%cxx_optflags -fno-schedule-insns -fschedule-insns2 -fstrict-aliasing"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared                  \
            --disable-static                 \
            --disable-libtool-lock \
            --enable-ipv6 \
            --enable-debug=no \
            --enable-alsa=no \
            --enable-artsc=no \
            --enable-portaudio=yes \
            --enable-macsnd=no \
            --enable-video=no \
            --enable-external-ortp \
            --with-pic \
            --with-gsm=%{_prefix}  \
            --with-sdl=%{_prefix} \
            --with-pic

make
cd ..


%install
rm -rf $RPM_BUILD_ROOT

export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

cd mediastreamer-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
cd ..



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/mediastream

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr (0755, root, bin) %{_datadir}/images
%{_datadir}/images/*

%changelog
* Fri Sep 18 2009 - moinakg(at)belenix<dot>org
- Remove commented patches.
* Thu May 14 2009 - moinakg@belenix.org
- Initial version
