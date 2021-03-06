#
# spec file for package SFEffmpeg
#
# includes module(s): FFmpeg
#

%include Solaris.inc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:                    SFEffmpeg
Summary:                 FFmpeg - a very fast video and audio converter

%define year 2009
%define month  04
%define day    26

Version:                 %{year}.%{month}.%{day}
Source:                  http://pkg.belenix.org/tarballs/ffmpeg-export-%{year}-%{month}-%{day}.tar.bz2
Patch4:                  ffmpeg-04-options.diff
SUNW_BaseDir:            %{_basedir}
URL:                     http://ffmpeg.mplayerhq.hu/index.html
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%ifarch sparc
%define mlib_opt --enable-mlib
BuildRequires: SUNWmlib
Requires: SUNWmlib
%else
%define mlib_opt
%endif
Requires: FSWxwrtl
Requires: FSWxorg-clientlibs
BuildRequires: FSWxorg-headers
Requires: SUNWzlib
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
BuildRequires: SFElibdts-devel
Requires: SFElibdts
BuildRequires: SFElibgsm-devel
Requires: SFElibgsm
BuildRequires: SFEliba52-devel
Requires: SFEliba52
BuildRequires: SFEliba52-devel
Requires: SFEliba52
BuildRequires: SFExvid-devel
Requires: SFExvid
BuildRequires: SFElibx264-devel
Requires: SFElibx264
BuildRequires: SFEfaad2-devel
Requires: SFEfaad2
#BuildRequires: SFEamrnb-devel
#Requires: SFEamrnb
#BuildRequires: SFEamrwb-devel
#Requires: SFEamrwb
BuildRequires: SFElame-devel
Requires: SFElame
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
BuildRequires: SUNWlibtheora-devel
Requires: SUNWlibtheora

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n ffmpeg-export-%{year}-%{month}-%{day}
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="-O4"
export LDFLAGS="%_ldflags -lm"
export PATH=/usr/gnu/bin:$PATH

cat configure | sed "s#SHFLAGS='-shared#SHFLAGS='-Wl,-G#" > configure.new
chmod +w configure
cp configure.new configure

bash ./configure	\
    --prefix=%{_prefix} \
    --cc=gcc		\
    %{mlib_opt}		\
    --enable-libgsm	\
    --enable-libxvid	\
    --enable-libx264	\
    --enable-gpl	\
    --enable-postproc	\
    --enable-libfaad	\
    --enable-libfaadbin	\
    --enable-libtheora	\
    --enable-libmp3lame	\
    --enable-libspeex	\
    --enable-pthreads	\
    --enable-libvorbis	\
    --enable-x11grab	\
    --enable-static	\
    --enable-shared

make -j $CPUS
cd libpostproc
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir $RPM_BUILD_ROOT%{_libdir}/ffmpeg
cp config.mak $RPM_BUILD_ROOT%{_libdir}/ffmpeg

cd libpostproc
make install DESTDIR=$RPM_BUILD_ROOT

# Create a ffmpeg.pc - Some apps need it
cat > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/ffmpeg.pc << EOM
Name: ffmpeg
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include
Description: FFmpeg codec library
Version: 51.40.4
Requires:  libavcodec libpostproc libavutil libavformat libswscale x264 ogg theora vorbisenc vorbis dts
Conflicts:
EOM

mv $RPM_BUILD_ROOT%{_libdir}/lib*.*a $RPM_BUILD_ROOT%{_libdir}/ffmpeg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/ffmpeg
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Apr 28 2009 - moinakg@belenix.org
- Bump version to 2009-04-26.
- Remove support for 3GPP AMR codecs as they are non-redistributable.
* Thu Feb 21 2008 - moinak.ghosh@sun.com
- Fix dependencies to build with FOX.
* Sat Aug 11 2007 - trisk@acm.jhu.edu
- Disable mediaLib support on non-sparc (conflicts with MMX)
- Enable x11grab for X11 recording
- Enable v4l2 demuxer for video capture
- Add workaround for options crash
* Wed Aug  3 2007 - dougs@truemail.co.th
- Bumped export version
- Added codecs
- Created ffmpeg.pc
* Tue Jul 31 2007 - dougs@truemail.co.th
- Added SUNWlibsdl test. Otherwise require SFEsdl
* Sat Jul 14 2007 - dougs@truemail.co.th
- Build shared library
* Sun Jan 21 2007 - laca@sun.com
- fix devel pkg default attributes
* Wed Jan 10 2007 - laca@sun.com
- create
