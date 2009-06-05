#
# spec file for package SFEmplayer
#
# includes module(s): mplayer
#
%include Solaris.inc

%define codecdir %{_libdir}/mplayer/codecs

Name:                    SFEmplayer
Summary:                 mplayer - The Movie Player
Version:                 1.5
Source:                  http://www.mplayerhq.hu/MPlayer/releases/mplayer-checkout-snapshot.tar.bz2
Patch1:                  mplayer-01-cddb.diff

# Workaround for possible Gas bug on Solaris.
Patch2:                  mplayer-02-mlp.h.diff
patch3:                  mplayer-03-mlpdsp.c.diff

Patch5:                  mplayer-05-configure.diff

Source3:                 http://www.mplayerhq.hu/MPlayer/skins/Blue-1.7.tar.bz2
Source4:                 http://www.mplayerhq.hu/MPlayer/skins/Abyss-1.7.tar.bz2
Source5:                 http://www.mplayerhq.hu/MPlayer/skins/neutron-1.5.tar.bz2
Source6:                 http://www.mplayerhq.hu/MPlayer/skins/proton-1.2.tar.bz2
#Source7:                 http://www.3gpp.org/ftp/Specs/latest/Rel-6/26_series/26104-610.zip
#Source8:                 http://www.3gpp.org/ftp/Specs/latest/Rel-6/26_series/26204-610.zip
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{tarball_version}-build
%include default-depend.inc
Requires: SFElibsndfile
Requires: SFElibdvdplay
Requires: SFElibmad
Requires: SFEliba52
Requires: SFEliveMedia
Requires: SFElame
Requires: SFEtwolame
Requires: SFEfaad2
Requires: SFElibmpcdec
Requires: SFEsdl
Requires: SUNWsmbau
Requires: SUNWgnome-audio
Requires: SUNWxorg-clientlibs
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWspeex
Requires: SUNWjpg
Requires: SUNWpng
Requires: SUNWogg-vorbis
Requires: SUNWlibtheora
Requires: SFEgccruntime
Requires: SFElibcdio
Requires: SUNWglib2
Requires: SUNWcairo
Requires: SUNWpango
Requires: SUNWlibatk
Requires: SUNWgtk2
Requires: SUNWsmbau
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
Requires: SUNWdbus-libs
Requires: SFElibx264
Requires: SFEgccruntime
Requires: SUNWfreetype2
Requires: SFEjack
Requires: SFEaalib
Requires: SFEnas
Requires: SUNWxwplt
Requires: SUNWzlib
Requires: SUNWbzip
Requires: SFElibmng
Requires: SFElibcdio
Requires: SFElibdts
Requires: SFElibdv
Requires: SFExvid
Requires: SFElibfribidi
BuildRequires: SFElibfribidi-devel
Requires: SFEladspa
BuildRequires: SFEladspa-devel
Requires: SFEopenal
BuildRequires: SFEopenal-devel
BuildRequires: SFElibsndfile-devel
BuildRequires: SFElibdvdplay-devel
BuildRequires: SFElibmad-devel
BuildRequires: SFEliba52-devel
BuildRequires: SFEliveMedia
BuildRequires: SFElame-devel
BuildRequires: SFEtwolame-devel
BuildRequires: SFEfaad2-devel
BuildRequires: SFElibmpcdec-devel
BuildRequires: SFEsdl-devel
BuildRequires: SFEgawk
BuildRequires: SUNWgnome-audio-devel
BuildRequires: SUNWgnu-libiconv-devel
BuildRequires: SFElibx264-devel
BuildRequires: SUNWgnu-gettext-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SFEjack-devel
BuildRequires: SFEaalib-devel
BuildRequires: SFEnas-devel
BuildRequires: SFElibmng-devel
BuildRequires: SFElibcdio-devel
BuildRequires: SFElibdts-devel
BuildRequires: SFElibdv-devel
BuildRequires: SFExvid-devel
BuildRequires: SUNWglib2-devel
BuildRequires: SUNWcairo-devel
BuildRequires: SUNWpango-devel
BuildRequires: SUNWlibatk-devel
BuildRequires: SUNWgtk2-devel

%define x11	/usr/openwin
%ifarch i386 amd64
%define x11	/usr/X11
%endif

%prep
%setup -q -c -n %name-%version
cd mplayer-checkout*
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1

#unzip %SOURCE7
#unzip 26104-610_ANSI_C_source_code.zip
#mv c-code libavcodec/amr_float
#unzip %SOURCE8
#unzip 26204-610_ANSI-C_source_code.zip
#mv c-code libavcodec/amrwb_float

perl -pi -e 's/-O2/-O1/' configure

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd mplayer-checkout*

%if %debug_build
dbgflag=--enable-debug
export CFLAGS="-g -D__hidden=\"\""
%else
dbgflag=--disable-debug
export CFLAGS="-O2 -D__hidden=\"\""
%endif

export LDFLAGS="-L%{x11}/lib -R%{x11}/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -L/usr/lib/live/liveMedia -R/usr/lib/live/liveMedia -L/usr/lib/live/groupsock -R/usr/lib/live/groupsock -L/usr/lib/live/UsageEnvironment -R/usr/lib/live/UsageEnvironment -L/usr/lib/live/BasicUsageEnvironment -R/usr/lib/live/BasicUsageEnvironment " 
export CC=gcc
rm -rf ./grep
ln -s /usr/sfw/bin/ggrep ./grep
PATH="`pwd`:$PATH"
echo "`type grep`"

export CFLAGS="$CFLAGS -fomit-frame-pointer -I/usr/lib/live/liveMedia/include -I/usr/lib/live/groupsock/include -I/usr/lib/live/UsageEnvironment/include -I/usr/lib/live/BasicUsageEnvironment/include -I%{x11}/include -I/usr/sfw/include -I/usr/gnu/include"

bash ./configure				\
	    --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --confdir=%{_sysconfdir}		\
            --enable-gui			\
            --enable-menu			\
	    --extra-cflags="${CFLAGS}"		\
	    --extra-ldflags="${LDFLAGS}"	\
%if %option_with_gnu_iconv
            --extra-libs='-lBasicUsageEnvironment -lUsageEnvironment -lgroupsock -lliveMedia -lsocket -lnsl -lstdc++ -lgnuintl -lgnuiconv' \
%else
            --extra-libs='-lBasicUsageEnvironment -lUsageEnvironment -lgroupsock -lliveMedia -lsocket -lnsl -lstdc++' \
%endif
            --codecsdir=%{codecdir}		\
            --enable-faad			\
            --enable-live			\
	    --enable-mp3lame			\
            --enable-network			\
	    --enable-rpath			\
            --enable-largefiles			\
	    --enable-crash-debug		\
            --disable-directfb			\
	    --disable-xvr100			\
	    --disable-liba52-internal		\
            --with-freetype-config=/usr/bin/freetype-config \
	    $dbgflag

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd mplayer-checkout*

gmake install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mplayer/codecs
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mplayer/skins
(
	cd $RPM_BUILD_ROOT%{_datadir}/mplayer/skins
	gtar fxj %SOURCE3
	gtar fxj %SOURCE4
	gtar fxj %SOURCE5
	gtar fxj %SOURCE6
	ln -s Blue default
)
ln -s /usr/openwin/lib/X11/fonts/TrueType/FreeSerif.ttf $RPM_BUILD_ROOT%{_datadir}/mplayer/subfont.ttf
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%{_datadir}/mplayer
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%changelog
* Fri Jun 05 2009 - moinakg@belenix(dot)org
- Updated to latest SVN snapshot.
- Remove disabling of x86 optimizations in cabac
- Add patch to work around possible Gas bug on Solaris.
* Sun Apr 17 2009 - moinakg@belenix.org
- Fix dependencies.
* Sun May 03 2009 - moinakg@belenix.org
- Update dependency to point to SFEgccruntime for Gcc4.
* Tue Apr 28 2009 - moinakg@belenix.org
- Update to latest SVN checkout snapshot.
- Add back SFEsdl dep.
* Fri Apr 10 2009 - moinakg@gmail.com
- Disable 3GPP AMR codecs as they are non-redistributable.
* Sat Jun 21 2008 - moinakg@gmail.com
- Remove dependency from SFEfreetype. It is no longer needed since
- SUNWfreetype is updated to new version.
* Sun Feb 24 2008 - moinakg@gmail.com
- Link with GNU gettext.
* Tue Jan 08 2008 - moinakg@gmail.com
- Link with SFEfreetype to fix missing symbol problem.
* Tue Jan 08 2008 - moinakg@gmail.com
- Updated LDFLAGS to add extra libs to fix link failure
- Chenged to dependency to SFEfreetype to get newer version of freetype2
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Remove SUNWlibiconv dependency to try to get the module to build.
* Mon Nov 5 2007 - markwright@internode.on.net
- Bump to 1.0rc2.  Change SUNWlibcdio to SFElibcdio.  Remove SFElibfame.
- Comment mplayer-02-makefile-libfame-dep.diff (libfame removed).  Bump patch1.
- Comment patch3 (already applied). Add BuildRequires: SFEgawk.  Add patch5
- as SFEgcc 4.2.2 does not understand -rdynamic.
* Fri Oct 19 2007 - dougs@truemail.co.th
- Fixed 3gpp urls
* Tue Aug 28 2007 - dougs@truemail.co.th
- Added debug option
* Tue Jul 31 2007 - dougs@truemail.co.th
- Removed dirac codec from Requirement
* Sun Jul 15 2007 - dougs@truemail.co.th
- Removed dirac codec patch - causes crashes
* Sat Jul 14 2007 - dougs@truemail.co.th
- Added dirac codec patch
- Added SFEladspa,SFElibfribidi requirement
* Tue May  1 2007 - dougs@truemail.co.th
- Removed SFEsdl from the Required. Conflicts with SUNWlibsdl
* Sun Apr 22 2007 - dougs@truemail.co.th
- Added /usr/gnu/libs to LDFLAGS
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add Requires SUNWsmbau after check-deps.pl run.
* Sun Jan  7 2007 - laca@sun.com
- split the codecs out into SFEmplayer-codecs
* Wed Jan  3 2007 - laca@sun.com
- re-add patches cddb and makefile-libfame-dep after merging with 1.0rc1
- add patches asmrules_20061231 (fixes a buffer overflow) and
  cabac-asm (disables some asm stuff that doesn't seem to compile on Solaris.
* Wed Nov 29 2006 - laca@sun.com
- bump to 1.0rc1
* Tue Sep 26 2006 - halton.huo@sun.com
- Add Requires after check-deps.pl run
* Tue Sep 26 2006 - halton.huo@sun.com
- Bump Source4 to version 1.6
* Thu Jul 27 2006 - halton.huo@sun.com
- Bump Source3 to version 1.6
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEmplayer
- delete -share subpkg
- update file attributes
* Mon Jun 13 2006 - dougs@truemail.co.th
- Bumped version to 1.0pre8
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
