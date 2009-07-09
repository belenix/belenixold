#
# spec file for package gst-plugins-good
#
# Copyright (c) 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
Name:           gst-plugins-good
License:        LGPL v2, BSD
Version:        0.10.14
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
Group:          Libraries/Multimedia
Summary:        GStreamer Streaming-media framework plug-ins.
URL:            http://gstreamer.freedesktop.org/
Source:         http://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
#owner:laca date:2006-01-19 type:bug bugster:6570425
Patch1:         gst-plugins-good-01-gettext.diff
#owner:yippi date:2007-03-16 type:feature bugzilla:529741
Patch2:         gst-plugins-good-02-cdda.diff
#owner:yippi date:2008-11-26 type:feature bugster:6825148
# Note this is a bug in the Sun Studio comnpiler, so no bug has been filed
# upstream for this issue.  Marking it as a feature so it does not show up
# as yellow in the patch report.
Patch3:         gst-plugins-good-03-compiler.diff
#owner:alfred date:2008-12-16 type:bug bugster:6787829
Patch4:         gst-plugins-good-04-selector.diff
#owner:yippi date:2009-03-06 type:feature
# This SunAudio patch will go upstream, but a bug has not been filed because
# the gst-plugins-base-03-flags.diff patch needs to be released by the
# community before this patch can go upstream.  The gst-plugins-base
# patch has gone upstream, but hasn't yet been released in a tarball.
Patch5:         gst-plugins-good-05-sunaudio.diff
#owner:yippi date:2009-03-06 type:feature
# This OSSv4 patch will go upstream, but a bug has not been filed because the
# gst-plugins-base-03-flags.diff patch needs to be released by the
# community before this patch can go upstream.  The gst-plugins-base
# patch has gone upstream, but hasn't yet been released in a tarball.
Patch6:         gst-plugins-good-06-ossv4.diff
#owner:yippi date:2009-03-12 type:branding
# Note that this patch is needed to disable MMX support in GOOM due to 
# Sun Studio compiler bugster bug #6825148.
Patch7:         gst-plugins-good-07-goom.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Docdir:         %{_defaultdocdir}/doc
Autoreqprov:    on
Prereq:         /sbin/ldconfig

%define 	majorminor	0.10

%define         _glib2          1.3.12

Requires:       glib2 >= %_glib2
Requires: 	gstreamer >= 0.10.0
Requires:       gst-plugins-base >= 0.10.0
Requires:       flac
Requires:       speex
Requires:       audiofile >= 0.2.1
Requires:       esound >= 0.2.8
Requires:       libjpeg
Requires:       libpng >= 1.2.0
Requires: 	XFree86-libs
Requires: 	GConf
BuildRequires:  glib2-devel >= %_glib2
BuildRequires: 	gstreamer-devel >= 0.10.0
BuildRequires:	gstreamer-tools >= 0.10.0
BuildRequires:  gstreamer-plugins-devel >= 0.10.0
BuildRequires:  flac-devel
BuildRequires:  speex-devel
BuildRequires:  pyxml
BuildRequires:  audiofile-devel >= 0.2.1
BuildRequires:  esound-devel >= 0.2.8
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel >= 1.2.0
BuildRequires:  glibc-devel
BuildRequires: 	GConf-devel

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

%prep
%setup -n gst-plugins-good-%{version} -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
# Turn off optimization as ss12 cores. Bugster: 6706089
#CFLAGS=$(echo $CFLAGS | sed -e 's/-xO4//'); \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ; \
glib-gettextize -f
libtoolize --copy --force
intltoolize --copy --force --automake
aclocal -I ./m4 -I ./common/m4 $ACLOCAL_FLAGS

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

# If building Indiana, then always use xvimagesink since Xorg
# will always be used in this situation.  Otherwise, use
# ximagsink on Sparc since Xsun does not support Xvideo.
#
%ifarch sparc
VIDEOSINK_CONFIG="--with-default-videosink=ximagesink"
%else
VIDEOSINK_CONFIG="--with-default-videosink=xvimagesink"
%endif

%if %option_with_indiana_branding
VIDEOSINK_CONFIG="--with-default-videosink=xvimagesink"
%endif

autoheader
autoconf
automake -a -c -f

# Disable the cdio plugin.  We do not want to link GPL libraries into
# GStreamer.
# Disable the oss plugin.  We use the ossv4 plugin if OSS is enabled.
./configure \
  --prefix=%{_prefix}	\
  --sysconfdir=%{_sysconfdir} \
  --mandir=%{_mandir}   \
  --disable-cdio	\
  --disable-oss		\
  %{gtk_doc_option}	\
  $VIDEOSINK_CONFIG	\
  --enable-external --with-check=no

# FIXME: hack: stop the build from looping
touch po/stamp-it

if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make 
else
  make
fi

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ]
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

# Clean out files that should not be part of the rpm.
# This is the recommended way of dealing with it for RH8
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm $RPM_BUILD_ROOT%{_bindir}/gst-visualise-0.10

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS COPYING README REQUIREMENTS
%{_libdir}/gstreamer-*/*.so
%{_sysconfdir}/gconf/schemas/gstreamer-*.schemas
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%post 
%{_bindir}/gst-register > /dev/null 2> /dev/null
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gstreamer-0.10.schemas"
for S in $SCHEMAS; do
 gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%package devel
Summary: 	GStreamer Plugin Library Headers.
Group: 		Development/Libraries
Requires: 	gstreamer-plugins-devel >= 0.10.0
Requires:       %{name} = %{version}
Provides:	gstreamer-play-devel = %{version}

%description devel
GStreamer support libraries header files.

%files devel
%defattr(-, root, root)
%{_datadir}/gtk-doc

%changelog
* Wed Mar 11 2009 - brian.cameron@sun.com
- Add patch gst-plugins-good-07-goom.diff to disable MMX support in the GOOM
  plugin.  It crashes on the amd64 platform.
* Fri Mar 06 2009 - brian.cameron@sun.com
- Add patches gst-plugins-good-05-sunaudio.diff and
  gst-plugins-good-06-ossv4.diff to support the new OSSv4 interfaces and so
  the SunAudio plugin makes use of the new gst-plugins-base flags.
* Fri Feb 20 2009 - brian.cameron@sun.com
- Bump to 0.10.14.
* Thu Jan 22 2009 - brian.cameron@sun.com
- Bump to 0.10.13.  Add patch gst-plugins-good-07-makefile.diff
* Wed Jan 07 2009 - alfred.peng@sun.com
- Add gst-06-selector.diff to include selector element.
* Thu Oct 30 2008 - brian.cameron@sun.com
- Add gst-04-fixmixer.diff so that the AUDIO_MIXER_MULTIPLE_OPEN ioctl is
  called after we set the mixer file descriptor.  Otherwise the ioctl is
  ignored.
* Mon Oct 27 2008 - brian.cameron@sun.com
- Bump to 0.10.11.
* Wed Aug 27 2008 - brian.cameron@sun.com
- Bump to 0.10.10.
* Thu Jul 31 2008 - brian.cameron@sun.com
- Bump to 0.10.9.
* Fri Jun 06 2008 - brian.cameron@sun.com
- Add patch gst-plugins-good-05-fixmixer.diff so that gnome-volume-control
  works properly with the SunAudio mixer applet.  Fixes bugzilla bug 
  #537031.
* Fri May 23 2008 - damien.carbery@sun.com
- Modify CFLAGS to turn off optimization as ss12 cores, bugster: 6706089.
  Add patch 04-disable-gcc-asm to workaround bugster 6706715. ss12 claims to
  support inline asm but fails when it encounters some.
  Disable both of these changes until we switch to building with ss12.
* Fri May 09 2008 - brian.cameron@sun.com
- Fix default audiosource so it is sunaudiosink rather than goom.
  Fixes P2 bug #6698690
* Wed Apr 23 2008 - brian.cameron@sun.com
- Bump to 0.10.8.  Remove upstream patch gst-plugins-good-03-fixmixer.diff.
* Wed Feb 20 2008 - brian.cameron@sun.com
- Bump to 0.10.7.  Remove upstream patch
  gst-plugins-good-03-fix-gconf-func.diff.
* Thu Jun 21 2007 - damien.carbery@sun.com
- Add patch 03-fix-gconf-func to fix 449747, a mismatch in func param types.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 0.10.6. Remove upstream patch, 02-opendeviceonce. Rename rest.
* Tue Jun 14 2007 - irene.huang@sun.com
- remove -03-endianess.diff since this patch is for
  libcdio which we no longer use. And -02-fixgoom.diff
  which is no longer useful. Renumbering opendeviceonce.diff 
  and cdda.diff.
* Wed Mar 21 2007 - damien.carbery@sun.com
- Add --with-check=no to configure so as not to pick up SFEcheck package. Build
  breaks when it finds the package.
* Fri Mar 16 2007 - brian.cameron@sun.com
- Add patch gst-plugins-good-05-cdda.diff to provide an ioctl based
  CDDA plugin, and disable the cdio plugin since it is GPL.
* Sat Mar 04 2007 - damien.carbery@sun.com
- Add intltoolize call to expand MSGFMT_OPTS.
* Thu Jan 25 2007 - chris.wang@sun.com
- Added patch, 03-endianess, to fix bug that sound-juicer cannot play audio CD
  properly on Sparc box. Bugzilla 377280.
* Thu Dec 21 2006 - brian.cameron@sun.com
- Bump to 0.10.5 and remove patch that updated sunaudiosink to CVS
  head.
* Mon Dec 11 2006 - brian.cameron@sun.com
- Remove patches 4, 5, 6 and replace with a patch that updates to 
  CVS head.  This fixes all these issues and the performance issues
  we have been seeing with GStreamer on Solaris.
* Mon Nov 27 2006 - brian.cameron@sun.com
- Patch to rest function so that on close we flush the input/output
  buffer.  This makes pause/stopping a file much more responsive.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Tue Oct 17 2006 - damien.carbery@sun.com
- Remove code that deletes *.a and *.la from %{_libdir} as none are installed 
  there.
* Mon Oct 16 2006 - damien.carbery@sun.com
- Remove the '-f' from the 'rm *.la *.a' lines so that any changes to the
  module source will be seen as a build error and action can be taken.
* Mon Sep 11 2006 - brian.cameron@sun.com
- Bump to 0.10.4.
* Thu Jul 27 2006 - brian.cameron@sun.com
- Fix src plugin so it opens nonblocking with the
  gst-plugins-good-09-srcopen.diff patch.
* Fri Jul 21 2006 - brian.cameron@sun.com
- Fix CDDA plugin so it doesn't assert & core dump if the CD device
  is not found.
* Thu Jun 29 2006 - brian.cameron@sun.com
- Move monitor to "source" tab, so it is more like sdtaudiocontrol.
  done via patch gst-plugins-good-07-monitorinput.diff.
* Tue Jun 27 2006 - brian.cameron@sun.com
- Fix sink plugin so it does not always reset port in prepare.  If the
  user has turned off the built-in speaker port in sdtaudiocontrol
  (or otherwise), then turning it back on causes the speakers to
  turn back on each time the user changes a track in rhythmbox, totem,
  etc.
* Thu Jun 15 2006 - brian.cameron@sun.com
- Now mute works with input tracks, and setting mute in the panel
  applet and gnome-volume-control doesn't get out-of-sync.
* Wed Jun 14 2006 - brian.cameron@sun.com
- Add patches to fix mixer and add source plugin.
* Tue Jun 13 2006 - brian.cameron@sun.com
- Bump to 0.10.3.
* Tue Jun 06 2006 - brian.cameron@sun.com
- Add patch gst-plugins-good-03-fixmixer.diff so that the mixer no
  longer core dumps if you check/uncheck the choices in 
  gnome-volume-control preferences.  Fix so mute works in
  gnome-volume-control, and fix so that setting the volume isn't
  hardcoded to only work with the audio output track.
* Wed May 10 2006 - brian.cameron@sun.com
- Remove gst-visualize again, this got lost when we migrated from
  gst-plugins to gst-plugins-base.
* Wed Apr 05 2006 - brian.cameron@sun.com
- Add patch 2 to fix the sunaudiosink so it allocates the ringbuffer 
  properly instead of using buffer-time property.  This fix should be
  in the next release of gst-plugins-good and can be removed at that
  time.
* Wed Feb 15 2006 - damien.carbery@sun.com
- Bump to 0.10.2.
- Remove upstream patches, 02-fixconfig, 03-fixsunaudio.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Add hack to fix infinite loop problem in po/Makefile.
* Mon Jan 9 2006 - brian.cameron@sun.com
- Update to 0.10.0.  This file was copied from the old gst-plugins.spec file
  and modified to work with gst-plugins-good.  The Obsoletes, Provides and
  packaging sections will need work if someone wants to build this
  on Linux.
* Mon Sep 26 2005 - brian.cameron@sun.com
- Add patch 2 which defines "inline" functions as either
  "static inline" or "extern inline".  Just defining
  functions as "inline" breaks Forte.
* Tue Sep 20 2005 - brian.cameron@sun.com
- Bump to 0.8.11.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 0.8.10.
* Tue Aug 02 2005 - balamurali.viswanathan@wipro.com
- Enable building of flac
* Tue Jul 26 2005 - balamurali.viswanathan@wipro.com
- Enable building of speex and theora plugins
* Mon Jul 25 2005 - balamurali.viswanathan@wipro.com
- Enable building of musicbrainz plugin
* Fri Jul 01 2005 - matt.keenan@sun.com
- Added patch 02-pkgconfig.diff, for Solairs build with new pkg-config
* Mon Jun 06 2005 - brian.cameron@sun.com
- Removed patch for modifying uninstalled-pc file since it is no longer
  needed.
* Fri Jun 03 2005 - brian.cameron@sun.com
- Add autodetect, equalizer, games, librfb, subparse, tta plugins which
  are new to 2.8.8.
* Fri May 13 2005 - brian.cameron@sun.com
- For the previous version of GStreamer, we were copying in a few files
  to fix GPL headers.  Took out this since it isn't needed and was 
  breaking the build.
* Tue Mar 15 2005 - balamurali.viswanathan@wipro.com
- Add patch gst-plugins-13-query-position-osssrc.diff to fix bug #6238742
  Patch taken from HEAD.
* Fri Feb 25 2005 - balamurali.viswanathan@wipro.com
- Add patch gst-plugins-12-query-length-wavparse.diff to fix bug #6226597
  Patch taken from HEAD.
* Fri Jan 28 2005 - ghee.teo@sun.com
- Cleaned up some obsoletion and provides conditions for gst-plugins
  To fix update bug 6222864.
* Fri Oct 29 2004 - laca@sun.com
- Add gst-launch-ext.1.gz to %files
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add gst-launch-ext*, libogg.3, libvorbis.3 man pages
* Tue Oct 05 2004 - takao.fujiwara@sun.com
- Added patch gst-plugins-11-g11n-i18n-ui.diff to localize gnome-volume-control
- Fixed 5108713
- updated gst-plugins-02-g11n-potfiles.diff
* Thu Sep 16 2004 - balamurali.viswanathan@wipro.com
- Add patch 09 and 10 for bugs #5102383 and #5102465
* Wed Sep 01 2004 - balamurali.viswanathan@wipro.com
- Add patch 07 to add an source element to sunaudio plugin
* Mon Aug 30 2004 - takao.fujiwara@sun.com
- Update gst-plugins-02-g11n-potfiles.diff
* Thu Aug 26 2004 - brian.cameron@sun.com
- No longer delete gstffmpegcolorspace since totem will not work without it.
  It does not use any MPEG licensed logic (ffmpeg refers to the ffmpeg
  module not MPEG).  Also don't delete libgstaasink.so since we never
  install it anyway with --disable-aalib.
* Thu Aug 26 2004 - ghee.teo@sun.com
- Obsoleted external plugin module, colorspace, asf and avi.
  These are now bundled into gstreamer-plugins.
* Tue Aug 24 2004 - niall.power@sun.com
- Build breakage fixed. Files removed in %install have to
  be removed from %files too. gst-visualize-0.8
* Fri Aug 20 2004 - brian.cameron@sun.com
- Removed dirac plugin.  The dirac website says they don't know if
  if has IP issues and that made SunLegal nervous. 
* Tue Aug 17 2004 - balamurali.viswanathan@wipro.com
- Add patch 06 to add an mixer element to sunaudio plugin
* Wed Aug 11 2004 - brian.cameron@sun.com
- Add patch 05 to correct GPL licensing problem in gstvideo
  plugin.  Remove gst-visualise from install since it is a
  test program that we do not want to create a man page for.
* Mon Aug 09 2004 - brian.cameron@sun.com
- corrected Linux packaging.
* Mon Aug 09 2004 - niall.power@sun.com
- reset release when the version is bumped
* Fri Aug 06 2004 - brian.cameron@sun.com
- Fixed --disable arguments so that the appropriate plugins get
  disabled, added --with-plugins to disable the proper gst
  plugins.
* Thu Aug 05 2004 - brian.cameron@sun.com
- Updated to 0.8.3
* Thu Jul 29 2004 - brian.cameron@sun.com
- Updated to gst-plugins 0.8.2, making patches 1, 4, 5, and 8 go
  away since they were integrated into CVS head.  Fixed libtoolize
  call so it works for Solaris.  Added patch 6 to make wavparse work,
  and this patch will go away when we upgrade to gst-plugins 0.8.3
* Fri Jul 16 2004 - brian.cameron@sun.com
- Added patch to change default video sink to ximagesink when
  building on Solaris, since xvimagesink requires Xvideo which
  does not exist on Solaris. 
* Mon Jul 12 2004 - niall.power@sun.com
- ported to rpm4
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gst-plugins-l10n-po-1.2.tar.bz2
* Tue May 25 2004 - yuriy.kuznetsov@sun.com
- Added gst-plugins-09-g11n-potfiles.diff
* Fri May 14 2004 - brian.cameron@sun.com
- added patch 08 from CVS head to support aligned memory access,
  needed for Solaris.
* Wed May 12 2004 - brian.cameron@sun.com
- Added changes to patch05 so that it contains more Solaris
  needed build patches.  Renamed patch to a more generic name.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gst-plugins-l10n-po-1.1.tar.bz2
* Wed May 12 2004 - ghee.teo@sun.com
- Updated tarball to 0.8.1 as per Laca and Brian's request.
* Wed May 12 2004 - laca@sun.com
- jds-autotoolize
- change order of directories in the aclocal call so that the correct vorbis
  macro is picked up. The one that comes with SuSE appears to be broken.
* Mon May 10 2004 - laca@sun.com
- require gstreamer >= 0.8.0
* Fri Apr 16 2004 - brian.cameron@sun.com
- Removed rm -rf $RPM_BUILD_ROOT from top of %install section since this
  was breaking Solaris build.
* Fri Apr 2 2004 - ghee.teo@sun.com
- Updated to 0.8.0 release tarball from 2.6
  Also removed gst-plugins-04-remove-xopen-source.diff 
  because gstxwindow.c no longer exists in 0.8.0
  Also changed majorminor to 0.8, updated a number of entries
  in %files sections.
* Fri Apr 2 2004 - brian.cameron@sun.com
- Added patch 2 to fix Solaris Makefile issue, and replace tar jxf
  with the more solaris friendly bzcat piped through tar
* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding gst-plugins-l10n-po-1.0.tar.bz2 l10n content
* Sun Mar 28 2004 Brian Cameron <brian.cameron@sun.com>
- Remove _XOPEN_SOURCE #define since it causes the Forte 
  compiler to be unable to compile this file.
* Mon Mar 22 2004 Niall Power <niall.power@sun.com>
- revert back to previous libtoolize invocation style
  until I figure out why .so files aren't being built.
* Tue Mar 16 2004 takao.fujiwara@sun.com
- Added gst-plugins-03-g11n-potfiles.diff
* Mon Mar 08 2004 Niall Power <niall.power@sun.com>
- add two patches to fix -uninstalled.pc files and
  to fix a gcc'ism in xwindowlistener.
* Wed Mar 03 2004 Ghee Teo <ghee.teo@sun.com>
- Corrected the Obsolete modules and sorted them correctly.
* Fri Feb 13 2004 Matt Keenan <matt.keenan@sun.com>
- Bump to 0.7.4
* Mon Jan 05 2004 Ghee Teo <ghee.teo@sun.com>
- Removed -%{majorminor} from gst-register because as a distro we do not
  need a parallel installed version of the program. That is, we should only
  have one version of the program only.
* Sun Nov 23 2003 Christian Schaller <Uraeus@gnome.org>
- Update spec file for latest changes
- add faad plugin
* Thu Oct 16 2003 Christian Schaller <Uraeus@gnome.org>
- Add new colorbalance and tuner and xoverlay stuff
- Change name of kde-audio-devel to arts-devel
* Sat Sep 27 2003 Christian Schaller <Uraeus@gnome.org>
- Add majorminor to man page names
- add navigation lib to package
* Tue Sep 11 2003 Christian Schaller <Uraeus@gnome.org>
- Add -%{majorminor} to each instance of gst-register
* Tue Aug 19 2003 Christian Schaller <Uraeus@Gnome.org>
- Add new plugins
* Sat Jul 12 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- move gst/ mpeg plugins to base package
- remove hermes conditional from snapshot
- remove one instance of resample plugin
- fix up silly versioned plugins efence and rmdemux
* Sat Jul 05 2003 Christian Schaller <Uraeus@gnome.org>
- Major overhaul of SPEC file to make it compatible with what Red Hat ships
  as default
- Probably a little less sexy, but cross-distro SPEC files are a myth anyway
  so making it convenient for RH users wins out
- Keeping conditionals even with new re-org so that developers building the
  RPMS don't need everything installed
- Add bunch of obsoletes to ease migration from earlier official GStreamer RPMS
- Remove plugins that doesn't exist anymore
* Sun Mar 02 2003 Christian Schaller <Uraeus@gnome.org>
- Remove USE_RTP statement from RTP plugin
- Move RTP plugin to no-deps section
* Sat Mar 01 2003 Christian Schaller <Uraeus@gnome.org>
- Remove videosink from SPEC
* Thu Jan 23 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- various fixes
- make video output packages provide gstreamer-videosink
* Thu Jan 23 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- split out ffmpeg stuff to separate plugin
* Fri Dec 27 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- add virtual provides for audio sources and sinks
* Sun Dec 15 2002 Christian Schaller <Uraeus@linuxrising.org>
- Update mpeg2dec REQ to be 0.3.1
* Tue Dec 10 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- only install schema once
- move out devel lib stuff to -devel package
* Sun Dec 08 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- fix location of libgstpng
- changes for parallel installability
* Thu Nov 28 2002 Christian Schaller <Uraeus@linuxrising.org>
- Put in libgstpng plugin
- rm the libgstmedia-info stuff until thomas think they are ready
* Fri Nov 01 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- don't use compprep until ABI issues can be fixed
* Wed Oct 30 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- added smpte plugin
- split out dvdnavread package
- fixed snapshot deps and added hermes conditionals
* Tue Oct 29 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- added -play package, libs, and .pc files
* Thu Oct 24 2002 Christian Schaller <Uraeus@linuxrising.org>
- Added wavenc to audio formats package
* Sat Oct 20 2002 Christian Scchaller <Uraeus@linuxrising.org>
- Removed all .la files
- added separate non-openquicktime demuxer plugin
- added snapshot plugin
- added videotest plugin
- Split avi plugin out to avi and windec plugins since aviplugin do not depend on avifile
- Added cdplayer plugin
* Fri Sep 20 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added gst-compprep calls
* Wed Sep 18 2002 Thomas Vander Stichele <thomas@apestaart.org>
- add gst-register-%{majorminor} calls everywhere again since auto-reregister doesn't work
- added gstreamer-audio-formats to mad's requires since it needs the typefind
  to work properly
* Mon Sep 9 2002 Christian Schaller <Uraeus@linuxrising.org>
- Added v4l2 plugin
* Thu Aug 27 2002 Christian Schaller <Uraeus@linuxrising.org>
- Fixed USE_DV_TRUE to USE_LIBDV_TRUE
- Added Gconf and floatcast headers to gstreamer-plugins-devel package
- Added mixmatrix plugin to audio-effects package
* Thu Jul 11 2002 Thomas Vander Stichele <thomas@apestaart.org>
- fixed oss package to buildrequire instead of require glibc headers
* Mon Jul 08 2002 Thomas Vander Stichele <thomas@apestaart.org>
- fixed -devel package group
* Fri Jul 05 2002 Thomas Vander Stichele <thomas@apestaart.org>
- release 0.4.0 !
- added gstreamer-libs.pc
- removed all gst-register-%{majorminor} calls since this should be done
  automatically now
* Thu Jul 04 2002 Thomas Vander Stichele <thomas@apestaart.org>
- fix issue with SDL package
- make all packages STRICTLY require the right version to avoid
  ABI issues
- make gst-plugins obsolete gst-plugin-libs
- also send output of gst-register-%{majorminor} to /dev/null to lower the
  noise
* Wed Jul 03 2002 Thomas Vander Stichele <thomas@apestaart.org>
- require glibc-devel instead of glibc-kernheaders since the latter is only
  since 7.3 and glibc-devel pulls in the right package anyway
* Sun Jun 23 2002 Thomas Vander Stichele <thomas@apestaart.org>
- changed header location of plug-in libs
* Mon Jun 17 2002 Thomas Vander Stichele <thomas@apestaart.org>
- major cleanups
- adding gst-register-%{majorminor} on postun everywhere
- remove ldconfig since we don't actually install libs in system dirs
- removed misc package
- added video-effects
- dot every Summary
- uniformify all descriptions a little
* Thu Jun 06 2002 Thomas Vander Stichele <thomas@apestaart.org>
- various BuildRequires: additions
* Tue Jun 04 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added USE_LIBADSPA_TRUE bits to ladspa package
* Mon Jun 03 2002 Thomas Vander Stichele <thomas@apestaart.org>
- Added libfame package
* Mon May 12 2002 Christian Fredrik Kalager Schaller <Uraeus@linuxrising.org>
- Added jack, dxr3, http packages
- Added visualisation plug-ins, effecttv and synaesthesia
- Created devel package
- Removed gstreamer-plugins-libs package (moved it into gstreamer-plugins)
- Replaced prefix/dirname with _macros
* Mon May 06 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added gstreamer-GConf package
* Wed Mar 13 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added more BuildRequires and Requires
- rearranged some plug-ins
- added changelog ;)
