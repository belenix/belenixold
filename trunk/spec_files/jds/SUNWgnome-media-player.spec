#
# spec file for package SUNWgnome-media-player
#
# includes module(s): totem
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include Solaris.inc

# Build plugins with Python 2.6.
#
%define pythonver 2.6

%define makeinstall make install DESTDIR=$RPM_BUILD_ROOT
%use totem = totem.spec
%use rhythmbox = rhythmbox.spec

Name:                    SUNWgnome-media-player
Summary:                 GNOME media player 
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_prefix}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWiso-codes-devel
BuildRequires: SUNWtotem-pl-parser-devel
BuildRequires: SUNWgnome-file-mgr
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWPython26-devel
BuildRequires: SUNWgnome-python26-libs-devel
BuildRequires: SUNWevolution-libs-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWmusicbrainz-devel
BuildRequires: SUNWgnome-media-apps-devel
BuildRequires: SUNWfirefox-devel
BuildRequires: SUNWgnome-themes-devel
BuildRequires: SUNWlibsoup-devel
BuildRequires: SUNWgst-python26
BuildRequires: SFElibsexy-devel
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-file-mgr
Requires: SUNWxorg-clientlibs
Requires: SUNWgnome-panel
Requires: SUNWtotem-pl-parser
Requires: SUNWiso-codes
Requires: SUNWdbus
Requires: SUNWgnome-config
Requires: SUNWgnome-media
Requires: SUNWgnome-vfs
Requires: SUNWlibms
Requires: SUNWlxml
Requires: SUNWgnome-component
Requires: SUNWdesktop-cache
Requires: SUNWPython26
Requires: SUNWgnome-python26-libs
Requires: SUNWevolution-libs
Requires: SUNWlibpopt
Requires: SUNWmusicbrainz
Requires: SUNWgnome-media-apps
Requires: SUNWfirefox
Requires: SUNWgnome-themes
Requires: SUNWhal
Requires: SUNWlibsoup
Requires: SUNWgst-python26
Requires: SFElibsexy
Requires: %{name}-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc


%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%totem.prep -d %name-%version
%rhythmbox.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export CFLAGS="%optflags -D__EXTENSIONS__ -I%{_includedir} -I/usr/X11/include"
export CXXFLAGS="%cxx_optflags -features=extensions -I/usr/X11/include"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%{?arch_ldadd} -z ignore -Bdirect -z combreloc -L/usr/X11/lib -R/usr/X11/lib -L/usr/sfw/lib -R/usr/sfw/lib -lX11"

%ifarch sparc
export x_includes="/usr/openwin/include"
export x_libraries="/usr/openwin/lib"
%endif

%totem.build -d %name-%version
%rhythmbox.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%totem.install -d %name-%version
%rhythmbox.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

#rhythbmox use librasero-media library, add RBAC permission for it
# RBAC related
mkdir $RPM_BUILD_ROOT/etc/security
# exec_attr(4)
cat >> $RPM_BUILD_ROOT/etc/security/exec_attr <<EOF
Desktop CD User:solaris:cmd:::/usr/bin/rhythmbox.bin:privs=sys_devices
EOF
#
mv $RPM_BUILD_ROOT/usr/bin/rhythmbox $RPM_BUILD_ROOT/usr/bin/rhythmbox.bin
cat >> $RPM_BUILD_ROOT/usr/bin/rhythmbox<< EOF
#!/bin/sh
#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#
# Copyright 2006 Sun Microsystems, Inc.	 All rights reserved.
# Use is subject to license terms.
#
pfexec "\`dirname \$0\`/\`basename \$0\`.bin" "\$@"
EOF


# We remove the below totem plugins including YouTube and Gromit
# since their respective dependecies gdata and gromit are missing
# on Solaris:
#
# - YouTube: a plugin to let you browse YouTube videos
# - Gromit: presentation helper to make annotations on screen
#
rm -r $RPM_BUILD_ROOT%{_libdir}/totem/plugins/gromit
rm -r $RPM_BUILD_ROOT%{_libdir}/totem/plugins/youtube

# We remove the below rhythmbox upnp_coherence plugin since its
# dependecy Coherence is missing on Solaris:
#
# - upnp_coherence: adds support for playing media from and sending media
# to DLNA/UPnP network devices, and enables Rhythmbox to be controlled
# by a DLNA/UPnP ControlPoint
#
#rm -r $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins/upnp_coherence

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/*/*-??_??.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%attr (0755, root, bin)%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/nautilus/extensions-2.0/lib*.so*
%{_libdir}/firefox/plugins
%{_libdir}/rhythmbox
%{_libdir}/rhythmbox-metadata
%{_libdir}/totem-plugin-viewer
%{_libdir}/totem
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%doc rhythmbox-%{rhythmbox.version}/AUTHORS
%doc rhythmbox-%{rhythmbox.version}/README
%doc(bzip2) rhythmbox-%{rhythmbox.version}/COPYING
%doc(bzip2) rhythmbox-%{rhythmbox.version}/NEWS
%doc(bzip2) rhythmbox-%{rhythmbox.version}/ChangeLog
%doc(bzip2) rhythmbox-%{rhythmbox.version}/po/ChangeLog
%doc(bzip2) rhythmbox-%{rhythmbox.version}/help/ChangeLog
%doc totem-%{totem.version}/AUTHORS
%doc totem-%{totem.version}/README
%doc(bzip2) totem-%{totem.version}/COPYING
%doc(bzip2) totem-%{totem.version}/NEWS
%doc(bzip2) totem-%{totem.version}/license_change
%doc(bzip2) totem-%{totem.version}/ChangeLog
%doc(bzip2) totem-%{totem.version}/po/ChangeLog
%doc(bzip2) totem-%{totem.version}/help/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/dbus-1/services/org.gnome.Rhythmbox.service
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/rhythmbox/C
%{_datadir}/gnome/help/totem/C
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/devices
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/devices
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/devices
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/devices
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/devices
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/devices
%attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps/*
%attr (-, root, other) %{_datadir}/icons/hicolor/16x16/devices/*
%attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps/*
%attr (-, root, other) %{_datadir}/icons/hicolor/22x22/devices/*
%attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps/*
%attr (-, root, other) %{_datadir}/icons/hicolor/24x24/devices/*
%attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps/*
%attr (-, root, other) %{_datadir}/icons/hicolor/32x32/devices/*
%attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps/*
%attr (-, root, other) %{_datadir}/icons/hicolor/48x48/devices/*
%attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps/*
%attr (-, root, other) %{_datadir}/icons/hicolor/scalable/devices/*
%{_datadir}/omf/rhythmbox/*-C.omf
%{_datadir}/omf/totem/*-C.omf
%{_datadir}/rhythmbox
%{_datadir}/totem
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%{_datadir}/gtk-doc


%files root
%defattr(-, root, sys)
%attr(0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/rhythmbox.schemas
%{_sysconfdir}/gconf/schemas/totem-handlers.schemas
%{_sysconfdir}/gconf/schemas/totem-video-thumbnail.schemas
%{_sysconfdir}/gconf/schemas/totem.schemas
%config %class (rbac) %attr (0644, root, sys) /etc/security/exec_attr


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Thu Mar 26 2009 - jerry.tan@sun.com
- move totem-pl-parser out to SUNWtotem-pl-parser 
* Fri Feb 27 2009 - jedy.wang@sun.com
- Use find command to remove static libraries.
* Tue Jan 20 2009 - brian.cameron@sun.com
- Fix packaging after bumping totem-pl-parser to 2.25.1 and totem to 2.25.3.
* Fri Dec 05 2008 - brian.cameron@sun.com
- Add attributes for icons in packaging.
* Thu Sep 18 2008 - brian.cameron@sun.com
- Fix packaging.
* Fri Sep 12 2008 - brian.cameron@sun.com
- Add new copyright files.
* Mon Jul 21 2008 - damien.carbery@sun.com
- Add Build/Requires SUNWlibsexy/-devel to fix 6725226.
* Thu May 15 2008 - jijun.yu@sun.com
- Remove the rm commands which won't useful any more.
* Thu May 15 2008 - jijun.yu@sun.com
- Remove rhthmbox upnp_coherence plugin.
* Thu May 08 2008 - jijun.yu@sun.com
- Remove 2 plugins including youtube and gromit. 
* Mon Apr 28 2008 - jijun.yu@sun.com
- Remove the 4 rm commands added on Apr.25, since the same functions will be 
  done at configuring. 
* Fri Apr 25 2008 - jijun.yu@sun.com
- Remove some plugins including libtotem-gmp, libtotem-narrowspace,
  libtotem-mully and libtotem-cone, because they are not supported on Solaris.
* Mon Mar 31 2008 - brian.cameron@sun.com
- Add SUNW_Copyright.
* Thu Mar 13 2008 - brian.cameron@sun.com
- Remove .la/.a files from totem plugin library directories.
* Fri Jan 11 2008 - damien.carbery@sun.com
- nautilus extensions go to extensions-2.0 dir. Change %files and %install.
* Wed Jan 09 2008 - damien.carbery@sun.com
- Uncomment plugins code as firefox 2 is back in the build.
* Thu Jan 03 2008 - damien.carbery@sun.com
- Comment out plugins code as firefox is not found by totem or rhythmbox and
  browser plugins not built. This is a workaround while firefox build corrected.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Mon Dec 03 2007 - brian.cameron@sun.com
- Add totem-pl-parser.
* Thu Nov 08 2007 - brian.cameron@sun.com
- Added proper totem/totem-video-thumbnailer manpages in the manpage
  tarball, so now remove the NROF ones included by totem module in the
  %install step.
* Fri Oct 12 2007 - laca@sun.com
- add /usr/X11/include to CXXFLAGS
* Thu Oct  4 2007 - laca@sun.com
- add %arch_ldadd to LDFLAGS for the libintl libs
* Tue Jul 03 2007 - damien.carbery@sun.com
- Browser plugins now installed to firefox/plugins dir.
* Wed Jun 13 2007 - damien.carbery@sun.com
- Comment out removal of 2 la/a files as they are not being installed.
* Wed May 23 2007 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-themes/-devel for gnome-icon-theme, required by
  totem.
* Tue May 15 2007 - damien.carbery@sun.com
- Add %{_libdir}/totem to %files; remove .a and .la files from there.
* Thu Apr 26 2007 - laca@sun.com
- delete some unnecessary env variables; set CXX to $CXX -norunpath because
  libtool swallows this option sometimes and leaves compiler paths in the
  binaries, fixes 6497719
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Mon Mar 12 2007 - laca@sun.com
- delete rhythmbox .la files in rhythmbox.spec
* Thu Mar 01 2007 - halton.huo@sun.com
- Remove -I%{_includedir}/mps from CXXFLAGS because it is 
  in /usr/lib/pkgconfig/firefox-xpcom.pc
* Wed Feb 28 2007 - halton.huo@sun.com
- Add -I%{_includedir}/mps into CXXFLAGS to fix build error.
* Thu Feb 22 2007 - damien.carbery@sun.com
- Add '-features=extensions' to CXXFLAGS because __func__ is used in new totem
  tarball.
* Mon Feb 12 2007 - damien.carbery@sun.com
- Remove '-I/usr/include/mps' from CFLAGS/CXXFLAGS. Make change to
  firefox-xpcom.pc file instead.
* Thu Nov 30 2006 - damien.carbery@sun.com
- Remove duplicate 'BuildRequires: SUNWfirefox-devel' line.
* Mon Nov 20 2006 - laca@sun.com
- s/Requires: SUNWfirefox-devel/Requires: SUNWfirefox/, fixes 6495619
* Fri Oct 20 2006 - damien.carbery@sun.com
- Remove SUNWhalh BuildRequires because header files are in SUNWhea in snv_51.
* Fri Oct 13 2006 - damien.carbery@sun.com
- Delete .a and .la files.
* Mon Oct 02 2006 - damien.carbery@sun.com
- Remove application-registry and mime-info dirs from %files as they are no 
  longer installed.
* Mon Sep 18 2006 - Brian.Cameron@sun.com
- Add SUNWhalh BuildRequires.
* Fri Sep 08 2006 - Matt.Keenan@sun.com
- Remove "rm" of _mandir during %install, add man page tarball for rhythmbox.1
  Deliver totem.1, totem-video-thumbnailer.1 from community, and manp
* Thu Aug 17 2006 - damien.carbery@sun.com
- Add the mozilla/plugins dir and totem-mozilla-viewer.
- Add Build/Requires SUNWfirefox/-devel for the xpidl compiler.
* Wed Aug 16 2006 - damien.carbery@sun.com
- Remove empty mozilla/plugins dir in %install.
* Sat Aug 12 2006 - laca@sun.com
- change datadir/icons permissions back to root:other since it's a stable
  interface and wasn't supposed to be changed
* Fri Aug 11 2006 - damien.carbery@sun.com
- Change SUNWhal-devel ref to SUNWhal as the former does not exist.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Update Build/Requires after check-deps.pl run.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Wed Jun 21 2006 - brian.cameron@sun.com
- Fix packaging.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 25 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Fri May 12 2006 - damien.carbery@sun.com
- Small update to dependency list after check-deps.pl run.
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Thu Mar  2 2006 - damien.carbery@sun.com
- Remove locale dir from l10n package - no files installed there.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Fri Sep 30 2005 - brian.cameron@sun.com
- Fix l10n packaging.
* Tue Sep 27 2005 - brian.cameron@sun.com
- Move back to default prefix instead of /usr/demo/jds, since we have
  decided to support this application.
* Wed Jan 19 2005 - matt.keenan@sun.com
- Deliver javahelp files for totem #6197736
* Mon Dec 13 2004 - damien.carbery@sun.com
- Move to /usr/sfw to implement ARC decision.
* Sun Nov 14 2004 - laca@sun.com
- move to /usr/demo/jds
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Fri Oct 01 2004 - takao.fujiwara@sun.com
- Added l10n package
- Added '--x-libraries' option in configure to fix bug 5081938
* Sat Sep 11 2004 - laca@sun.com
- Set LDFLAGS so Xrandr and Xrender can be found.
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Fri Jul 23 2004 - damien.carbery@sun.com
- Add SUNWgnome-media-devel as build requirement.
* Thu Jul 15 2004 - brian.cameron@sun.com
- Created.
