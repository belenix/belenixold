#
# spec file for package totem
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include l10n.inc
Name:         totem
License:      GPL v2, LGPL v2, BSD
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Totem Multimedia Player
Source:       http://ftp.gnome.org/pub/GNOME/sources/totem/2.26/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
#owner:jerrytan date:2006-01-08 type:branding
Patch1:       totem-01-remove-unsupported-format.diff
#owner:yippi date:2006-04-27 type:branding
Patch2:       totem-02-menu-entry.diff
#owner:jerrytan date:2007-06-20 type:branding
Patch3:	      totem-03-browserplugin.diff
#owner:yippi date:2008-04-25 type:branding
Patch4:	      totem-04-web-plugin.diff
#owner:davelam date:2008-12-25 type:bug bugzilla:N/A
Patch5:	      totem-05-libsocket.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%define	libgnomeui_version			2.6.0
%define	gstreamer_version               	0.8.1
%define gstreamer_plugins_version       	0.8.1
%define gnome_desktop_version                   2.6.1

Requires:       libgnomeui >= %{libgnomeui_version}
Requires:       gstreamer >= %{gstreamer_version}
Requires:       gstreamer-plugins >= %{gstreamer_plugins_version}
Requires:       gnome-desktop >= %{gnome_desktop_version}
Requires:       iso-codes
BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  gstreamer-devel >= %{gstreamer_version}
BuildRequires:  gstreamer-plugins-devel >= %{gstreamer_plugins_version}
BuildRequires:  gnome-desktop-devel >= %{gnome_desktop_version}

%description
Totem is multimeida player for the GNOME desktop, allowing you to play CDs, DVDS and a 
wide range of multimedia formats

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export PYTHON=/usr/bin/python%{pythonver}

if test "x$x_includes" = "x"; then
 x_includes="/usr/X11/include"
fi

if test "x$x_libraries" = "x"; then
 x_libraries="/usr/X11/lib"
fi

libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

export MOZILLA_PLUGINDIR="%{_libdir}/firefox/plugins"
CFLAGS="$RPM_OPT_FLAGS"	\

# We enable the above totem plugins including gmp, narrowspace,
# mully, cone since they are used for media types that are
# not supported on Solaris, but can get codecs through codeina
#
# - GMP         = Windows Media
# - narrowspace = QuickTime
# - MullY       = DivX
# - Cone        = VLC
#

./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
        --libdir=%{_libdir}         \
        --bindir=%{_bindir}         \
	--libexecdir=%{_libexecdir} \
	--mandir=%{_mandir}         \
	--localstatedir=/var/lib    \
	--enable-gstreamer	    \
	--disable-lirc              \
        --x-includes="$x_includes"  \
        --x-libraries="$x_libraries" 

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="totem.schemas totem-video-thumbnail.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%defattr (-, root, root)
%{_bindir}/*
%{_sysconfdir}/gconf/schemas
%{_libdir}/*
%{_libexecdir}/*
%{_datadir}/applications
%{_datadir}/gnome/help/totem/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/omf/totem/*
%{_datadir}/pixmaps/*
%{_datadir}/totem/*
%{_mandir}/man1/totem*
%{_includedir}/totem/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Thu Mar 12 2009 - brian.cameron@sun.com
- Bump to 2.25.92.  Add PYTHON environment variable to %build section.
* Tue Feb 17 2009 - brian.cameron@sun.com
- Bump to 2.25.91.
* Thu Feb 05 2009 - christian.kelly@sun.com
- Bump to 2.25.90.
- Remove patches/totem-06-function.diff.
- Rework patches/totem-01-remove-unsupported-format.diff.
* Tue Jan 20 2009 - brian.cameron@sun.com
- Bump to 2.25.3.  Remove upstream patch totem-05-avoid-plugin-coredump.diff.
  Add patch totem-06-function.diff.
* Tue Nov 04 2008 - brian.cameron@sun.com
- Backout fix for bug #6227253.  This changed totem's help file to point to
  sample_apps_info.xml since totem previously did not have its own docs. 
  Now that totem has docs, this hack needs to be removed or users can't see
  the actual totem help when selecting help from totem's menus.  Fixes bug
  #6756164.
* Wed Sep 24 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
* Mon Sep 01 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
- patches/totem-01-remove-unsupported-format.diff: rework.
- patches/totem-03-browserplugin.diff: rework.
- patches/totem-04-web-plugin.diff: rework.
* Fri Jun 20 2008 - jerry.tan@sun.com
- Bump to 2.23.4
* Wed Jun 04 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Tue May 27 2008 - jijun.yu@sun.com
- Remove --with-ff3 option since it also works agaist ff 2.
* Tue May 27 2008 - jijun.yu@sun.com
- Add a firfox 3 specific patch.
* Thu May 08 2008 - jijun.yu@sun.com
- Remove patch 5.
* Wed May 07 2008 - jijun.yu@sun.com
- Add a patch to fix bugster bug #6695629.
* Mon Apr 28 2008 - jijun.yu@sun.com
- Disable 4 plugins:libtotem-gmp, libtotem-narrowspace, libtotem-mully,
  libtotem-cone.
* Fri Apr 25 2008 - jijun.yu@sun.com
- Add a patch to remove some MIME types unsupported including flv, mp3.
* Thu Apr 24 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Thu Apr 10 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Tue Mar  4 2008 - damien.carbery@sun.com
- Bump to 2.21.96.
* Wed Feb 27 2008 - damien.carbery@sun.com
- Bump to 2.21.95.
* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 2.21.94.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.93.
* Tue Feb 05 2007 - brian.cameron@sun.com
- Bump to 2.21.92.
* Mon Jan 07 2007 - brian.cameron@sun.com
- Bump to 2.21.90.
* Mon Dec 03 2007 - brian.cameron@sun.com
- Bump to 2.21.4.
* Mon Nov 12 2007 - damien.carbery@sun.com
- Bump to 2.21.2. Remove upstream patches, 04-shell-change, 05-asprintf and
  06-tick.
* Tue Nov 06 2007 - brian.cameron@sun.com
- Remove totem-03-novisual.diff patch.  This patch was added because using
  the GStreamer GOOM plugin with totem caused severe flashing and audio 
  stuttering performance issues.  These issues have gone away with the
  latest GStreamer releases.
* Wed Oct 31 2007 - damien.carbery@sun.com
- Bump to 2.21.1.
* Wed Oct 31 2007 - damien.carbery@sun.com
- Add patch 07-tick to change TICK to TTICK to fix bugzilla 492087.
* Wed Oct 31 2007 - damien.carbery@sun.com
- Add patches 05-shell-change and 06-asprintf.
* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 2.21.0.
* Mon Oct 22 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Thu Aug 30 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.
* Wed Aug 22 2007 - damien.carbery@sun.com
- Set MOZILLA_PLUGINDIR before configure call as configure.in has been changed
  to fix #414457.
* Mon Aug 20 2007 - damien.carbery@sun.com
- Bump to 2.19.90.
* Fri Jun 22 2007 - jerry.tan@sun.com
- put totem plugins into /usr/lib/firefox/plugins
* Wed Jun 21 2007 - irene.huang@sun.com
- Removing patch 05-xthreadinit.diff, since it is the root cause
  of the bug is exists in libXi.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 2.19.4.
* Wed May 23 2007 - damien.carbery@sun.com
- Remove dos2unix call because the be.po file is correct (closes bugzilla
  #398052). Set PKG_CONFIG_PATH so that gnome-icon-theme.pc in
  %{_datadir}/pkgconfig can be found.
* Mon May 21 2007 - damien.carbery@sun.com
- Bump to 2.19.3.
* Wed May 16 2007 - damien.carbery@sun.com
- Change patch -05-xthreadinit.diff to be branding
* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 2.19.2. Remove code that deletes 'vanity' files and the pixmaps dir
  because they are not installed.
* Thu Apr 19 2007 - laca@sun.com
- add -ascii option to dos2unix so that utf8 strings are not messed up
* Wed Apr 04 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Wed Mar 22 2007 - irene.huang@sun.com
- add patch 05-xthreadinit.diff
* Wed Mar 21 2007 - irene.huang@sun.com
- add patch -04-cdmenuitem.diff.
* Sun Mar 11 2007 - damien.carbery@sun.com
- Bump to 2.18.0. Remove upstream patches, 04-grep-no-q and
  05-gst-0.10.12-support.
* Fri Mar 09 2007 - damien.carbery@sun.com
- Add patch, 05-gst-0.10.12-support, to build against new gst tarballs. These
  changes are from totem CVS.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Add patch, 04-grep-no-q, to remove -q from grep call. Fixes 414961.
* Thu Feb 22 2007 - damien.carbery@sun.com
- Bump to 2.17.92. Remove upstream patches, 04-shell-func, 05-func-macro and
  06-debug-macros.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Thu Feb 08 2007 - damien.carbery@sun.com
- Add patch, 04-shell-func, to make shell script work. Fixes 405758.
- Add patch 05-func-macro to use G_GNUC_FUNCTION (bugzilla 405850) and
  06-debug-macros to use G_GNUC_PRETTY_FUNCTION and proper va_args (#405880).
* Thu Feb 08 2007 - damien.carbery@sun.com
- Bump to 2.17.91. Remove upstream patches, 03-function-macro and
  04-moz-plugin. Renumber rest.
* Mon Jan 29 2007 - damien.carbery@sun.com
- Bump to 2.17.90. Remove upstream patches, 07-va_args, 06-2175-fix and
  03-uninstalled-pc. Add 03-function-macro to fix #402163.
* Thu Jan 18 2007 - damien.carbery@sun.com
- Add patch, 06-2175-fix, to include a missing file. Fixes 398071. Add patch,
  07-va_args, to make variable args macro work with forte. Fixes 398090.
* Wed Jan 17 2007 - damien.carbery@sun.com
- Bump to 2.17.5. Remove upstream patch, 04-fixcd. Renumber remainder.
* Wed Dec 06 2006 - brian.cameron@sun.com
- Add totem-06-novisual.diff so that the visualizer is turned off
  by default since goom has basd performance issues on Solaris
  that often cause audio stuttering.  Better to leave it off until
  the visualizer performance improves.
* Thu Nov 23 2006 - damien.carbery@sun.com
- Bump to 2.17.3.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Remove 'rm' lines from %install as the files listed are not installed.
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 2.16.2.
- Remove '-f' from 'rm' calls to force failure when source changes need
  attention.
* Fri Sep 08 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 1.5.92.
- Remove upstream patch, 05-automake-conditional, renumber rest.
* Thu Aug 17 2006 - damien.carbery@sun.com
- Add patch, 06-moz-plugin, to get mozilla plugin to build.
* Wed Aug 16 2006 - damien.carbery@sun.com
- Add patch, 05-automake-conditional, to fix an automake issue. #351617.
* Mon Aug 14 2006 - damien.carbery@sun.com
- Bump to 1.5.91.
* Fri Jul 28 2006 - damien.carbery@sun.com
- Bump to 1.5.90.
* Thu Jul 13 2006 - brian.cameron@sun.com
- Patch to fix totem so it passes the CD device name to GStreamer on Solaris.
* Wed Jun 21 2006 - brian.cameron@sun.com
- Bump to 1.5.2.
* Mon May 01 2006 - brian.cameron@sun.com
- Added uninstalled.pc file to totem so that rhythmbox can be built in same
  package, since rhythmbox depends on totem.
* Fri Apr 28 2006 - glynn.foster@sun.com
- Add patch to call it 'Totem Movie Player' from
  now on.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 1.4.0.
* Wed Mar  1 2006 - damien.carbery@sun.com
- Bump to 1.3.92.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 1.3.91.
* Sun Jan 29 2006 - damien.carbery@sun.com
- Bump to 1.3.90
* Mon Jan 23 2006 - damien.carbery@sun.com
- Remove obsolete patch, 03-fixfunc.
* Fri Jan 20 2006 - damien.carbery@sun.com
- Bump to 1.3.1.
* Tue Jan 03 2006 - damien.carbery@sun.com
- Remove obsolete patch, 01-desktop.sh; renumber remainder.
- Remove obsolete patch, 02-menu-entry.
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 1.3.0
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Tue Sep 27 2005 - brian.cameron@sun.com
- Bump to 1.2.0.
- Fix patch4 so it compiles against latest code.
* Tue Sep 27 2005 - damien.carbery@sun.com
- Bump to 1.1.5.
* Mon Sep 12 2005 - laca@sun.com
- add patch desktop.sh.diff: changes echo -n to printf as echo -n doesn't
  work on Solaris
* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 1.1.4.
* Tue Jul 12 2005 - damien.carbery@sun.com
- Add patch 5 to build CD-ROM code (src/totem-disc.c) on Solaris.
  http://bugzilla.gnome.org/show_bug.cgi?id=310149
* Thu Jun 16 2005 - matt.keenan@sun.com
- Bump to 1.0.3
* Thu Jun 09 2005 - matt.keenan@sun.com
- Bump to 1.0.1
- Remove patchs 02, 03, 04
- Rename patch 05 to 03
* Thu May 05 2005 - damien.carbery@sun.com
- 6227253: Change xml file in totem-C.omf from totem.xml to
  sample_apps_info.xml (part of gnome-user-docs). Bit of a hack but a very easy
  one to maintain.
* Fri Feb 25 2005 - kazuhiko.maekawa@sun.com
- Added dummy l10n help files to follow base update
* Mon Feb 14 2005 - damien.carbery@sun.com
- Integrate docs tarball (totem-docs-0.1) from irene.ryan@sun.com.
* Thu Feb 10 2005 - matt.keenan@sun.com
- 6227304 : install german help correctly
* Wed Jan 19 2005 - matt.keenan@sun.com
- Add Javahelp convert #6197736
* Sun Nov 14 2004 - laca@sun.com
- add --bindir=%{_bindir} and --libdir=%{_libdir} to configure opts
* Fri Oct 29 2004 - laca@sun.com
- Add missing deps
* Fri Oct 01 2004 - takao.fujiwara@sun.com
- Added '--x-libraries' option in configure to fix bug 5081938
* Sat Sep 11 2004 - laca@sun.com
- Move Solaris specific LDFLAGS to the Solaris spec file
* Fri Sep 10 2004 - damien.carbery@sun.com
- Set LDFLAGS so Xrandr and Xrender can be found.
* Fri Sep 03 2004 - kaushal.kumar@wipro.com
- Added patch 05 to let jmplay handle wav and mp3 files.
  Fixes bugtraq #5093284.
* Mon Jul 19 2004 - brian.cameron@sun.com
- Added patch 04 so that icons get displayed on Solaris.
  Patch approved by totem maintainer.
* Fri Jul 16 2004 - brian.cameron@sun.com
- Added patch 03 to support building on Solaris.
* Wed Jul 14 2004 - niall.power@sun.com
- packaging fixes for rpm4
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to totem-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to totem-l10n-po-1.1.tar.bz2
* Mon Apr 26 2004 - glynn.foster@sun.com
- Bump to 0.99.11
* Thu Apr 15 2004 - glynn.foster@sun.com
- Bump to 0.99.10, and remove Ghee's temporary workaround 
  patch.
* Tue Apr 06 2004 - ghee.teo@sun.com
- Created a totem-03-temporary-workaround-build.diff to resolve the
  hardcoded  GST_MAJORMINOR=0.7 problem. This patch should be removed
  once a new release totem is available.
* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar
* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding totem-l10n-po-1.0.tar.bz2 l10n content
* Fri Feb 13 2004 - matt.keenan@sun.com
- Bump tarball to 0.99.9, redo patch 01
* Mon Jan 12 2004 - matt.keenan@sun.com
- Bump tarball to 0.99.8, patch for compile errors
* Fri Nov 14 2003 - glynn.foster@sun.com
- Re add the desktop patch to change the menu entry.
* Fri Oct 31 2003 - glynn.foster@sun.com
- Remove the Sun Supported keyword from the 
  desktop file, since we're no longer going with the Extras
  menu.
* Wed Oct 22 2003 - glynn.foster@sun.com
- Update to 0.99.7
* Fri Oct 13 2003 - laca@sun.com
- Update to 0.99.6
* Thu Aug 14 2003 - ghee.teo@sun.com
- Removed totem totem.applications and totem.keys so that jmplay can 
  become the default media player.
* Sat Aug 02 2003 - glynn.foster@sun.com
- Update menu entry.
* Fri Jul 25 2003 - glynn.foster@sun.com
- Initial Sun release
