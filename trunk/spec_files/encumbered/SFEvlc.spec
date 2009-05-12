#
# spec file for package SFEvlc
#
# includes module(s): vlc
#
%include Solaris.inc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

%define	src_name	vlc
%define	src_url		http://download.videolan.org/pub/videolan/vlc

Name:                   SFEvlc
Summary:                vlc - the cross-platform media player and streaming server
Version:                0.9.9a
Source:                 %{src_url}/%{version}/%{src_name}-%{version}.tar.bz2
Patch1:                 vlc-01-alloca.diff
Patch2:                 vlc-02-solaris_specific.diff
Patch3:                 vlc-03-oss.diff
Patch4:                 vlc-04-segv.diff
Patch5:                 vlc-05-dirent.diff
Patch6:                 vlc-06-file.c.diff
Patch8:			vlc-08-osdmenu_path.diff
Patch9:			vlc-09-pic-mmx.diff

SUNW_BaseDir:           %{_basedir}
SUNW_Copyright:         %{src_name}.copyright
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %SUNWlibsdl
BuildRequires:  SUNWlibsdl-devel
Requires:       SUNWlibsdl
%else
BuildRequires:  SFEsdl-devel
Requires:       SFEsdl
%endif
BuildRequires:  SFEsdl-image-devel
Requires:       SFEsdl-image
Requires:       SUNWhal
BuildRequires:  SUNWdbus-devel
Requires:       SUNWdbus
Requires:       SUNWxorg-clientlibs
BuildRequires:  SUNWsmbau
BuildRequires:  SFElibfribidi-devel
Requires:       SFElibfribidi
BuildRequires:  SUNWfreetype2
Requires:       SUNWfreetype2
BuildRequires:  SFEliba52-devel
Requires:       SFEliba52
BuildRequires:  SFEffmpeg-devel
Requires:       SFEffmpeg
BuildRequires:  SFElibmad-devel
Requires:       SFElibmad
BuildRequires:  SFElibmpcdec-devel
Requires:       SFElibmpcdec
BuildRequires:  SFElibmatroska-devel
Requires:       SFElibmatroska
BuildRequires:  SUNWogg-vorbis-devel
Requires:       SUNWogg-vorbis
BuildRequires:  SFElibdvbpsi-devel
Requires:       SFElibdvbpsi
BuildRequires:  SFElibdvdread-devel
Requires:       SFElibdvdread
BuildRequires:  SFElibdvdread-devel
Requires:       SFElibdvdread
BuildRequires:  SFElibdts-devel
BuildRequires:  SFElibcddb-devel
Requires:       SFElibcddb
BuildRequires:  SFElibmpeg2-devel
Requires:       SFElibmpeg2
BuildRequires:  SFElibupnp-devel
Requires:       SFElibupnp
BuildRequires:  SFEvcdimager-devel
Requires:       SFEvcdimager
BuildRequires:  SFElibx264-devel
Requires:       SFElibx264
BuildRequires:  SFElibtar-devel
Requires:       SFElibtar
BuildRequires:  SFEqt4-devel
Requires:       SFEqt4

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n vlc-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch8 -p1
%patch9 -p1

%if %cc_is_gcc
%else
%error "This spec file requires Gcc4 to build. Please set the CC and CXX environment variables"
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
# ffmpeg is build with g++, therefore we need to build with g++

%if %build_l10n
nlsopt=-enable-nls
%else
nlsopt=-disable-nls
%endif

X11LIB="-L/usr/X11/lib -R/usr/X11/lib"
GNULIB="-L/usr/gnu/lib -R/usr/gnu/lib"

export PATH=/usr/gnu/bin:$PATH
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CC=gcc
export CXX=g++
export SHELL="/usr/bin/bash"
#
# -D_XPG4_2 is to get CMSG_* declarations and expected struct msghdr in <sys/socket.h>.
# -D-D__C99FEATURES__ to get fpclassify
#
export CPPFLAGS="-D__EXTENSIONS__ -D_XPG4_2 -D__C99FEATURES__ -I/usr/X11/include -I/usr/gnu/include -I/usr/lib/live/liveMedia/include -I/usr/lib/live/groupsock/include -I/usr/lib/live/BasicUsageEnvironment/include -I/usr/lib/live/UsageEnvironment/include"
%if %debug_build
export CFLAGS="-g"
%else
export CFLAGS="-O3"
%endif

export CFLAGS="$CFLAGS -fno-strict-aliasing -ftree-loop-distribution -ftree-loop-linear -floop-interchange -floop-strip-mine"
export CXXFLAGS="-fno-strict-aliasing -ftree-loop-distribution -ftree-loop-linear -floop-interchange -floop-strip-mine"
LIVE_LFLAGS="-L/usr/lib/live/liveMedia -R/usr/lib/live/liveMedia -L/usr/lib/live/groupsock -R/usr/lib/live/groupsock -L/usr/lib/live/BasicUsageEnvironment -R/usr/lib/live/BasicUsageEnvironment"
export LDFLAGS="-lsocket -lnsl -lgnuintl -lgnuiconv $X11LIB $GNULIB $LIVE_LFLAGS"

rm ./configure
bash ./bootstrap

bash ./configure --prefix=%{_prefix}            \
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
	    --enable-shared			\
	    --enable-mkv			\
	    --enable-live555			\
	    --enable-ffmpeg			\
	    --enable-xvid			\
	    --enable-real			\
	    --enable-realrtsp			\
%if %debug_build
	    --enable-debug=yes			\
%endif
	    --disable-static			\
	    $nlsopt

#
# FIX '$echo' in libtool
#
cp libtool libtool.orig
cat libtool.orig | sed '{
    s#\$echo#echo#g
    s#/bin/sh#/usr/bin/bash#
}' > libtool

cp ./modules/misc/freetype.c ./modules/misc/freetype.c.orig
cat ./modules/misc/freetype.c.orig | sed '{
    s#/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf#/usr/openwin/lib/X11/fonts/TrueType/FreeSerifBold.ttf#
}' > ./modules/misc/freetype.c

export RM="/usr/bin/rm -f"
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
export RM="/usr/bin/rm -f"
export SHELL="/usr/bin/bash"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
cp $RPM_BUILD_ROOT%{_datadir}/vlc/vlc48x48.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/vlc.png
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
cp $RPM_BUILD_ROOT%{_datadir}/vlc/vlc32x32.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/vlc.png
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
cp $RPM_BUILD_ROOT%{_datadir}/vlc/vlc16x16.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/vlc.png

find ${RPM_BUILD_ROOT} -name "*.la" | xargs rm -f 

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then 
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS
( touch %{_datadir}/icons/hicolor  || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/vlc
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/vlc
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/16x16/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/*.png
%{_datadir}/icons/hicolor/48x48/apps/*.png

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Tue May 12 2009 - moinakg@belenix.org
- Bump version to 0.9.9a.
- Rework patches.
* Sat Jun 21 2008 - moinakg@gmail.com
- Remove dependency from SFEfreetype. It is no longer needed since
- SUNWfreetype is updated to new version.
* Fri Aug  3 2007 - dougs@truemail.co.th
- Added devel and l10n
- Added options to better find codecs
- Added icons for app
* Tue Jul 31 2007 - dougs@truemail.co.th
- added --disable-rpath option
- added SFElibx264 to the requirements
* Sun Jul 15 2007 - dougs@truemail.co.th
- --with-debug enables --enable-debug, added some dependencies
* Sat Jul 14 2007 - dougs@truemail.co.th
- Build with gcc
* Fri Mar 23 2007 - daymobrew@users.sourceforge.net
- Add two patches, 01-configure-no-pipe and 02-solaris. Add multiple
  dependencies. Getting closer but not quite building yet.
  Patch 01-configure-no-pipe removes the '-pipe' test. It causes problems later
  with -DSYS_SOLARIS being added after -pipe and being rejected by the linker.
  Patch 02-solaris.diff fixes two compiler issues. First involves expansion of
  ?: code; second changes AF_LOCAL to AF_UNIX as the former is not defined in
  <sys/socket.h>.

* Thu Mar 22 2007 - daymobrew@users.sourceforge.net
- Initial version
